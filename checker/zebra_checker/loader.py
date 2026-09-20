"""YAML -> Puzzle, with full validation and file:line on every finding."""

from pathlib import Path

import yaml

from . import clues as clue_grammar
from .errors import PuzzleSchemaError, suggest
from .findings import Finding, Severity, finding
from .model import Category, Clue, PostRef, Puzzle

TOP_LEVEL = {
    "name", "dimensions", "size", "categories", "answer", "clues",
    "post", "allow_duplicate_items",
}
CLUE_META = {"type", "post_number", "prose", "keep_redundant", "note"}


class _LineDict(dict):
    """dict that remembers the source line it was parsed from."""
    line: int | None = None


class _LineLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        out = _LineDict(mapping)
        out.line = node.start_mark.line + 1
        return out


def _line(value) -> int | None:
    return getattr(value, "line", None)


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


class _Validator:
    def __init__(self, path: Path, doc: dict):
        self.path = path
        self.doc = doc
        self.findings: list[Finding] = []
        self.rel = str(path)

    def add(self, code: str, message: str, *, line=None, hint=None, clue_index=None, **data):
        self.findings.append(
            finding(code, message, file=self.rel, line=line, hint=hint,
                    clue_index=clue_index, data=data)
        )

    # -- structure ---------------------------------------------------------

    def check_top_level(self) -> bool:
        ok = True
        for key in ("name", "dimensions", "size", "categories", "answer", "clues"):
            if key not in self.doc:
                self.add("E101", f"missing required key: {key}", line=_line(self.doc))
                ok = False
        for key in self.doc:
            if key not in TOP_LEVEL:
                self.add("E101", f"unknown top-level key: {key}", line=_line(self.doc),
                         hint=f"known keys: {', '.join(sorted(TOP_LEVEL))}")
                ok = False
        return ok

    def build_categories(self) -> tuple[Category, ...]:
        cats: list[Category] = []
        raw_cats = self.doc.get("categories") or []
        for raw in raw_cats:
            if not isinstance(raw, dict) or "name" not in raw or "items" not in raw:
                self.add("E101", "category needs 'name' and 'items'", line=_line(raw))
                continue
            items = list(raw["items"])
            seen: set[str] = set()
            for item in items:
                if not isinstance(item, str):
                    self.add("E101",
                             f"category '{raw['name']}' item {item!r} is not a string",
                             line=_line(raw),
                             hint="quote every item; PyYAML turns 08:05 into an int "
                                  "and no/on/off into booleans")
                elif "," in item:
                    self.add("E112",
                             f"item '{item}' contains a comma",
                             line=_line(raw),
                             hint="data-puzzle-answer is comma-split, so commas break "
                                  "answer matching")
                if item in seen:
                    self.add("E103",
                             f"duplicate item '{item}' in category '{raw['name']}'",
                             line=_line(raw))
                seen.add(item)
            cats.append(Category(raw["name"], tuple(items), _line(raw)))
        return tuple(cats)

    def check_counts(self, cats: tuple[Category, ...]) -> None:
        d, n = self.doc.get("dimensions"), self.doc.get("size")
        if isinstance(d, int) and len(cats) != d:
            self.add("E102", f"expected {d} categories, got {len(cats)}", line=_line(self.doc))
        if isinstance(n, int):
            for cat in cats:
                if len(cat.items) != n:
                    self.add("E102",
                             f"category '{cat.name}' has {len(cat.items)} items, expected {n}",
                             line=cat.line)

    def check_cross_category_items(self, cats: tuple[Category, ...]) -> None:
        if self.doc.get("allow_duplicate_items"):
            return
        owner: dict[str, str] = {}
        for cat in cats:
            for item in cat.items:
                if item in owner and owner[item] != cat.name:
                    self.add("E104",
                             f"item '{item}' appears in both '{owner[item]}' and '{cat.name}'",
                             line=cat.line,
                             hint="ambiguous in prose and in the answer tuple; rename one, "
                                  "or set allow_duplicate_items: true")
                owner[item] = cat.name

    def check_answer(self, cats: tuple[Category, ...]) -> None:
        answer = self.doc.get("answer") or {}
        names = {c.name: c for c in cats}
        for key, value in answer.items():
            cat = names.get(key)
            if cat is None:
                self.add("E105", f"answer references unknown category: {key}",
                         line=_line(answer), hint=suggest(key, names) and
                         f"did you mean: {suggest(key, names)}?")
                continue
            if value not in cat.items:
                hint = suggest(value, cat.items)
                self.add("E106",
                         f"answer value '{value}' is not an item of '{key}'",
                         line=_line(answer),
                         hint=f"did you mean: {hint}?" if hint else
                              f"known items: {', '.join(cat.items)}")
        for cat in cats:
            if cat.name not in answer:
                self.add("E105", f"answer is missing category '{cat.name}'",
                         line=_line(answer))

    # -- clues -------------------------------------------------------------

    def _check_endpoint(self, spec, cats, idx, label):
        names = {c.name: c for c in cats}
        if not isinstance(spec, dict) or "category" not in spec or "item" not in spec:
            self.add("E109", f"clue {idx + 1}: {label} needs 'category' and 'item'",
                     line=_line(spec), clue_index=idx)
            return
        cat = names.get(spec["category"])
        if cat is None:
            hint = suggest(spec["category"], names)
            self.add("E108", f"clue {idx + 1}: unknown category '{spec['category']}'",
                     line=_line(spec), clue_index=idx,
                     hint=f"did you mean: {hint}?" if hint else
                          f"known categories: {', '.join(names)}")
            return
        if spec["item"] not in cat.items:
            hint = suggest(spec["item"], cat.items)
            self.add("E108",
                     f"clue {idx + 1}: unknown item '{spec['item']}' in category "
                     f"'{cat.name}'",
                     line=_line(spec), clue_index=idx,
                     hint=f"did you mean: {hint}?" if hint else
                          f"known items: {', '.join(cat.items)}")

    def _check_fact(self, spec, cats, idx, label):
        if not isinstance(spec, dict) or "subject" not in spec or "object" not in spec:
            self.add("E109",
                     f"clue {idx + 1}: {label} needs 'subject' and 'object' "
                     f"(and optionally 'negated')",
                     line=_line(spec), clue_index=idx)
            return
        self._check_endpoint(spec["subject"], cats, idx, f"{label}.subject")
        self._check_endpoint(spec["object"], cats, idx, f"{label}.object")

    def _check_shape(self, clue_raw, ctype, cats, idx):
        names = {c.name: c for c in cats}
        for field, kind in clue_grammar.REQUIRED_FIELDS[ctype].items():
            if field not in clue_raw:
                self.add("E109", f"clue {idx + 1}: '{ctype}' requires field '{field}'",
                         line=_line(clue_raw), clue_index=idx)
                continue
            value = clue_raw[field]
            if kind == "ep":
                self._check_endpoint(value, cats, idx, field)
            elif kind == "ep[]":
                if not isinstance(value, list) or not value:
                    self.add("E109", f"clue {idx + 1}: '{field}' must be a non-empty list",
                             line=_line(clue_raw), clue_index=idx)
                else:
                    for entry in value:
                        self._check_endpoint(entry, cats, idx, field)
            elif kind == "fact":
                self._check_fact(value, cats, idx, field)
            elif kind == "fact[]":
                if not isinstance(value, list) or not value:
                    self.add("E109", f"clue {idx + 1}: '{field}' must be a non-empty list",
                             line=_line(clue_raw), clue_index=idx)
                else:
                    for entry in value:
                        self._check_fact(entry, cats, idx, field)
            elif kind == "cat":
                if value not in names:
                    hint = suggest(value, names)
                    self.add("E108", f"clue {idx + 1}: unknown category '{value}'",
                             line=_line(clue_raw), clue_index=idx,
                             hint=f"did you mean: {hint}?" if hint else None)
            elif kind == "map":
                if not isinstance(value, dict) or not value:
                    self.add("E109", f"clue {idx + 1}: 'mapping' must be a non-empty mapping",
                             line=_line(clue_raw), clue_index=idx)
                    continue
                ca, cb = clue_raw.get("category_a"), clue_raw.get("category_b")
                for a_item, b_item in value.items():
                    if ca in names:
                        self._check_endpoint({"category": ca, "item": a_item}, cats, idx,
                                             "mapping key")
                    if cb in names:
                        self._check_endpoint({"category": cb, "item": b_item}, cats, idx,
                                             "mapping value")
        if ctype == "either_or" and isinstance(clue_raw.get("facts"), list) \
                and len(clue_raw["facts"]) != 2:
            self.add("E109", f"clue {idx + 1}: 'either_or' takes exactly 2 facts",
                     line=_line(clue_raw), clue_index=idx)

    def build_clues(self, cats: tuple[Category, ...]) -> list[Clue]:
        out: list[Clue] = []
        for idx, raw in enumerate(self.doc.get("clues") or []):
            if not isinstance(raw, dict) or "type" not in raw:
                self.add("E101", f"clue {idx + 1}: missing 'type'", line=_line(raw))
                continue
            declared = raw["type"]
            ctype = clue_grammar.ALIASES.get(declared, declared)
            if ctype != declared:
                self.add("W315",
                         f"clue {idx + 1}: clue type '{declared}' is deprecated, "
                         f"use '{ctype}'",
                         line=_line(raw), clue_index=idx)
            if ctype not in clue_grammar.ENCODERS:
                hint = suggest(declared, clue_grammar.ENCODERS)
                self.add("E107", f"clue {idx + 1}: unknown clue type '{declared}'",
                         line=_line(raw), clue_index=idx,
                         hint=f"did you mean: {hint}?" if hint else
                              f"known types: {', '.join(sorted(clue_grammar.ENCODERS))}")
                continue
            self._check_shape(raw, ctype, cats, idx)
            if ctype == "self_exclusion" and raw.get("category_a") == raw.get("category_b"):
                self.add("E313",
                         f"clue {idx + 1}: self_exclusion within a single category "
                         f"('{raw.get('category_a')}')",
                         line=_line(raw), clue_index=idx,
                         hint="every distinct pair is already forced by the grid rules")

            numbers = _as_list(raw.get("post_number"))
            prose = _as_list(raw.get("prose"))
            if any(not isinstance(v, int) for v in numbers):
                self.add("E110", f"clue {idx + 1}: post_number must be an int or a list of ints",
                         line=_line(raw), clue_index=idx)
                numbers = [v for v in numbers if isinstance(v, int)]
            if prose and numbers and len(prose) != len(numbers):
                self.add("E110",
                         f"clue {idx + 1}: prose has {len(prose)} entries but post_number "
                         f"has {len(numbers)}",
                         line=_line(raw), clue_index=idx)
            out.append(Clue(index=idx, type=ctype, raw=raw,
                            post_numbers=tuple(numbers),
                            prose=tuple(str(p) for p in prose),
                            keep_redundant=bool(raw.get("keep_redundant")),
                            note=raw.get("note"), line=_line(raw)))
        return out

    def build_post(self, cats: tuple[Category, ...]) -> PostRef | None:
        raw = self.doc.get("post")
        if raw is None:
            return None
        if isinstance(raw, str):
            raw = {"path": raw}
        if "path" not in raw:
            self.add("E101", "post block needs 'path'", line=_line(raw))
            return None
        order = tuple(raw.get("answer_order") or ())
        names = {c.name for c in cats}
        for name in order:
            if name not in names:
                self.add("E105", f"post.answer_order references unknown category '{name}'",
                         line=_line(raw))
        if order and set(order) != names:
            self.add("E105", "post.answer_order must list every category exactly once",
                     line=_line(raw))
        # narrative_only may be a list of numbers, or a mapping of
        # number -> prose so those items are checked against the post too
        raw_flavour = raw.get("narrative_only")
        flavour_prose: dict[int, str] = {}
        if isinstance(raw_flavour, dict):
            numbers = []
            for key, text in raw_flavour.items():
                if not isinstance(key, int) or isinstance(key, bool):
                    self.add("E110", f"narrative_only key {key!r} is not a number",
                             line=_line(raw)); continue
                numbers.append(key)
                flavour_prose[key] = str(text)
        else:
            numbers = _as_list(raw_flavour)

        return PostRef(
            path=raw["path"],
            panel_title=raw.get("panel_title", "evidence"),
            answer_order=order,
            narrative_only=tuple(numbers),
            narrative_prose=flavour_prose,
            line=_line(raw),
        )


def load_puzzle(path: Path) -> Puzzle:
    """Parse and validate.  Raises PuzzleSchemaError carrying every finding."""
    path = Path(path)
    with open(path) as handle:
        doc = yaml.load(handle, Loader=_LineLoader)
    if not isinstance(doc, dict):
        raise PuzzleSchemaError([
            finding("E101", "puzzle file is not a YAML mapping", file=str(path))
        ])

    v = _Validator(path, doc)
    v.check_top_level()
    cats = v.build_categories()
    v.check_counts(cats)
    v.check_cross_category_items(cats)
    v.check_answer(cats)
    clue_list = v.build_clues(cats)
    post = v.build_post(cats)

    errors = [f for f in v.findings if f.severity is Severity.ERROR]
    if errors:
        raise PuzzleSchemaError(v.findings)

    puzzle = Puzzle(
        name=doc.get("name", path.stem),
        dimensions=doc.get("dimensions", len(cats)),
        size=doc.get("size", len(cats[0].items) if cats else 0),
        categories=cats,
        answer=dict(doc.get("answer") or {}),
        clues=clue_list,
        path=path,
        post=post,
        allow_duplicate_items=bool(doc.get("allow_duplicate_items")),
    )
    puzzle.schema_findings = v.findings  # type: ignore[attr-defined]
    return puzzle
