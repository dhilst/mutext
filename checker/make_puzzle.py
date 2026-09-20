#!/usr/bin/env python3
"""Authoring aid: turn a solution into a minimal, sufficient clue set.

Input is a spec YAML holding the categories and the intended solution:

    name: "INC-0008 Split Brain"
    dimensions: 4
    size: 4
    categories:
      - name: monitor
        items: ["mon-01", "mon-02", "mon-03", "mon-04"]
      ...
    solution:                      # one row per entity
      - { monitor: mon-01, node: n-alpha, term: t-41, votes: "v=1" }
      ...
    answer: { monitor: mon-02, node: n-beta, term: t-43, votes: "v=3" }
    pool:                          # optional: hand-written candidate clues
      - { type: negation, subject: {...}, object: {...} }

It builds a candidate pool (the hand-written one, plus every direct/negation
pair consistent with the solution unless --no-auto), picks clues until the
solution is unique, then deletes every clue it can while keeping uniqueness.
Prints a clue list ready to paste into a puzzle YAML.
"""

import argparse
import random
import sys
from pathlib import Path

import yaml
from z3 import Distinct, Int, Not, Or, Solver, sat, unsat

sys.path.insert(0, str(Path(__file__).parent))

from zebra_checker.clues import constraint  # noqa: E402
from zebra_checker.model import Clue  # noqa: E402


def build(spec):
    cats = spec["categories"]
    n = spec["size"]
    assign = {c["name"]: {i: Int(f"{c['name']}__{i}") for i in c["items"]} for c in cats}
    ax = []
    for c in cats:
        vs = [assign[c["name"]][i] for i in c["items"]]
        ax += [v >= 0 for v in vs] + [v < n for v in vs] + [Distinct(*vs)]
    first = cats[0]
    for idx, item in enumerate(first["items"]):
        ax.append(assign[first["name"]][item] == idx)
    return assign, ax


def entity_of(spec):
    """item -> entity number, from the declared solution rows."""
    first = spec["categories"][0]["name"]
    order = {row[first]: i for i, row in enumerate(spec["solution"])}
    # the first category is pinned to declaration order
    canonical = {item: idx for idx, item in enumerate(spec["categories"][0]["items"])}
    mapping = {}
    for row in spec["solution"]:
        entity = canonical[row[first]]
        for cat, item in row.items():
            mapping[(cat, item)] = entity
    return mapping


def auto_pool(spec, ent):
    """Every consistent direct/negation pair, minus anything the spec forbids.

    `avoid_direct` keeps positive clues off the named items, so the answer row
    has to be reached by elimination instead of being handed over.  Without it
    the minimiser happily picks "settle = 19h" and the puzzle solves itself.
    """
    cats = [c["name"] for c in spec["categories"]]
    items = {c["name"]: c["items"] for c in spec["categories"]}
    avoid = set(spec.get("avoid_direct") or [])
    if spec.get("avoid_direct_answer"):
        avoid |= set(spec["answer"].values())
    pool = []
    for ai in range(len(cats)):
        for bi in range(ai + 1, len(cats)):
            a, b = cats[ai], cats[bi]
            for x in items[a]:
                for y in items[b]:
                    same = ent[(a, x)] == ent[(b, y)]
                    if same and (x in avoid or y in avoid):
                        continue
                    pool.append({
                        "type": "direct" if same else "negation",
                        "subject": {"category": a, "item": x},
                        "object": {"category": b, "item": y},
                    })
    return pool


def as_clue(raw, index):
    return Clue(index=index, type=raw["type"], raw=raw)


def unique(ax, formulas, assign, spec):
    s = Solver()
    s.add(*ax, *formulas)
    if s.check() != sat:
        return "unsat", None
    model = s.model()
    block = Or(*[
        assign[c["name"]][i] != model.eval(assign[c["name"]][i])
        for c in spec["categories"] for i in c["items"]
    ])
    s.add(block)
    return ("unique" if s.check() == unsat else "multi"), model


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="spec YAML with categories + solution")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-auto", action="store_true",
                    help="use only the hand-written pool")
    ap.add_argument("--prefer-direct", type=float, default=0.35,
                    help="share of positive clues to try first (default 0.35)")
    ap.add_argument("--tries", type=int, default=24,
                    help="restarts; the smallest clue set wins")
    args = ap.parse_args()

    spec = yaml.safe_load(Path(args.spec).read_text())
    assign, ax = build(spec)
    ent = entity_of(spec)

    pool = list(spec.get("pool") or [])
    if not args.no_auto:
        pool += auto_pool(spec, ent)

    formulas = [constraint(as_clue(raw, i), assign) for i, raw in enumerate(pool)]
    status, _ = unique(ax, formulas, assign, spec)
    if status != "unique":
        print(f"the whole candidate pool is {status} — check the solution rows",
              file=sys.stderr)
        return 1

    best: list[int] | None = None
    for attempt in range(args.tries):
        rng = random.Random(args.seed + attempt)
        positive = [i for i in range(len(pool)) if pool[i]["type"] == "direct"]
        negative = [i for i in range(len(pool)) if pool[i]["type"] != "direct"]
        rng.shuffle(positive)
        rng.shuffle(negative)
        order = []
        while positive or negative:
            take_pos = positive and (not negative or rng.random() < args.prefer_direct)
            order.append(positive.pop() if take_pos else negative.pop())

        chosen: list[int] = []
        for i in order:
            chosen.append(i)
            if unique(ax, [formulas[j] for j in chosen], assign, spec)[0] == "unique":
                break
        else:
            continue
        for i in list(chosen):
            trial = [j for j in chosen if j != i]
            if unique(ax, [formulas[j] for j in trial], assign, spec)[0] == "unique":
                chosen = trial
        if best is None or len(chosen) < len(best):
            best = chosen

    assert best is not None
    print(f"# minimal sufficient clue set: {len(best)} clues "
          f"(pool of {len(pool)}, {args.tries} restarts)")
    print("clues:")
    for pos, i in enumerate(best, start=1):
        raw = pool[i]
        print(f"  - type: {raw['type']}")
        print(f"    post_number: {pos}")
        print(f"    prose: \"TODO\"")
        if raw["type"] in ("direct", "negation"):
            s, o = raw["subject"], raw["object"]
            print(f"    subject: {{ category: {s['category']}, item: \"{s['item']}\" }}")
            print(f"    object:  {{ category: {o['category']}, item: \"{o['item']}\" }}")
        else:
            body = yaml.safe_dump({k: v for k, v in raw.items() if k != "type"},
                                  default_flow_style=True).strip()
            print(f"    # {body}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
