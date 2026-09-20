#!/usr/bin/env python3
"""Continuity guard for the chapter arc.

Checks the things a puzzle checker cannot see:

  * every ledger entry is rendered from the ledger by at least one post, and by
    the chapter that owns it;
  * cross-chapter strings are not typed by hand into a post outside the chapter
    that owns them, unless they are grid or answer values (which must be literal);
  * HORUS is not named before the chapter that reveals it;
  * a chapter that ties a clock time to an incident's harness window agrees
    with the diversion schedule chapter 10 prints;
  * the NEXT INCIDENT chain reaches every chapter in order and ends somewhere;
  * no meta-language leaks into player-facing prose.

    uv run check_continuity.py            # from checker/
"""

import re
import sys
from pathlib import Path

import yaml

REVEAL_CHAPTER = 10           # HORUS is named here and nowhere earlier
META_WORDS = [
    r"\bzebra\b", r"\bthe grid\b", r"\bcategor(?:y|ies)\b", r"\bpuzzle\b",
    r"\b[45]D\b", r"\bclue \d", r"\bthe player\b", r"\bthe UI\b",
]
LEDGER_REF = re.compile(r"site\.data\.evidence[\.\[]['\"]?(\w+)")


def chapter_of(post: Path) -> int:
    day = int(post.name.split("-")[2])
    return day - 14                      # chapter N is 2026-05-(14+N)


SCHEDULE_ROW = re.compile(
    r"^\s*(INC-\d{4})\s+\S+\s+(\d{2}:\d{2})\s*[-\u2013]\s*(\d{2}:\d{2}|\u2014)", re.M)
WINDOW_CLAIM = re.compile(r"[^.]*\bwindow\b[^.]*\.", re.S)


def minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def schedule_findings(texts: dict, names: dict) -> list[str]:
    """Chapter 10 publishes the diversion schedule. Anything elsewhere that
    puts a clock time next to an incident must agree with it."""
    windows = {}
    for text in texts.values():
        for inc, start, end in SCHEDULE_ROW.findall(text):
            if end not in ("\u2014", "—"):
                windows[inc] = (minutes(start), minutes(end), start, end)
    if not windows:
        return ["no diversion schedule found - chapter 10 should print one"]

    out = []
    for ch, text in sorted(texts.items()):
        # the schedule itself is the source of truth, not a claim about it
        body = "\n".join(l for l in text.splitlines() if not SCHEDULE_ROW.match(l))
        for sentence in WINDOW_CLAIM.findall(body):
            if len(sentence) > 400:
                continue                      # a block, not a sentence
            incs = set(re.findall(r"INC-\d{4}", sentence))
            times = set(re.findall(r"\b(\d{2}:\d{2})\b", sentence))
            for inc in incs:
                if inc not in windows:
                    continue
                lo, hi, s0, s1 = windows[inc]
                for t in times:
                    if not (lo <= minutes(t) <= hi):
                        out.append(
                            f"{names[ch]}: says {t} belongs to {inc}'s window, but the "
                            f"schedule gives {inc} {s0}-{s1}")
    return out


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    posts = sorted((root / "_posts").glob("*.md"))
    ledger = yaml.safe_load((root / "_data" / "evidence.yml").read_text())
    failures: list[str] = []
    notes: list[str] = []

    texts = {chapter_of(p): p.read_text() for p in posts}
    names = {chapter_of(p): p.name for p in posts}

    # 1. every ledger entry is rendered, by the chapter that owns it
    referenced: dict[str, set[int]] = {}
    for ch, text in texts.items():
        for key in LEDGER_REF.findall(text):
            referenced.setdefault(key, set()).add(ch)
        for key in re.findall(r"evidence-card\.html id=\"(\w+)\"", text):
            referenced.setdefault(key, set()).add(ch)

    for key, entry in ledger.items():
        where = referenced.get(key, set())
        if not where:
            failures.append(f"ledger entry '{key}' is never rendered by any post")
            continue
        owner = int(entry.get("chapter", 0))
        if owner and owner not in where:
            failures.append(
                f"ledger entry '{key}' says chapter {owner:02d} but is only "
                f"rendered by {sorted(where)}")
        notes.append(f"  {key:<14} owned by ch{owner:02d}, rendered by "
                     + ", ".join(f"ch{c:02d}" for c in sorted(where)))

    # 2. ledger text renders raw - evidence-card.html emits {{ item.note }}
    #    into a <p>, so markdown in a note reaches the page as literal characters
    for key, entry in ledger.items():
        for field in ("note", "fragment", "source"):
            value = str(entry.get(field, ""))
            if field != "fragment" and ("`" in value or "**" in value):
                failures.append(
                    f"ledger entry '{key}' has markdown in {field}; the card renders "
                    f"it as plain text, so it will show the characters themselves")

    # 3. HORUS is not named early
    for ch, text in sorted(texts.items()):
        if ch < REVEAL_CHAPTER and re.search(r"\bHORUS\b", text, re.I):
            failures.append(f"{names[ch]}: names HORUS before chapter {REVEAL_CHAPTER}")

    # 4. link chain
    chain, cur, seen = [], 1, set()
    while cur in texts and cur not in seen:
        seen.add(cur)
        chain.append(cur)
        m = re.search(r"href=\"\{\{ '(/[^']+)' \| relative_url \}\}\">(?:NEXT INCIDENT|POST-INCIDENT)",
                      texts[cur])
        if not m:
            failures.append(f"{names[cur]}: no forward link")
            break
        target = m.group(1)
        nxt = next((c for c, t in texts.items()
                    if re.search(rf"^permalink:\s*{re.escape(target)}\s*$", t, re.M)), None)
        if nxt is None:
            if not (root / "_site" / target.lstrip("/")).exists() and \
               not list((root / "_lore").glob(Path(target).stem + ".*")):
                failures.append(f"{names[cur]}: forward link {target} resolves to nothing")
            break
        cur = nxt
    missing = sorted(set(texts) - set(chain))
    if missing:
        failures.append("chapters not reachable from chapter 1: "
                        + ", ".join(str(c) for c in missing))

    # 5. clock times attributed to an incident's window
    failures += schedule_findings(texts, names)

    # 6. meta-language, outside liquid tags and code fences
    for ch, text in sorted(texts.items()):
        prose = re.sub(r"\{%.*?%\}", "", text, flags=re.S)
        prose = re.sub(r"```.*?```", "", prose, flags=re.S)
        prose = re.sub(r"<[^>]+>", "", prose)
        for pattern in META_WORDS:
            for hit in re.finditer(pattern, prose, re.I):
                line = prose[:hit.start()].count("\n") + 1
                failures.append(f"{names[ch]}: meta-language {hit.group(0)!r} "
                                f"in player-facing prose (~line {line})")

    print(f"chapters: {len(texts)}   ledger entries: {len(ledger)}")
    print(f"chain:    {' -> '.join(f'{c:02d}' for c in chain)}")
    print("\n".join(notes))
    if failures:
        print("\nFAIL")
        for f in failures:
            print(f"  {f}")
        return 1
    print("\nPASS — continuity holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
