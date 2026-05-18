from z3 import Solver


def encode_clue(solver: Solver, assign: dict, clue: dict):
    ctype = clue["type"]

    if ctype == "direct":
        s = assign[clue["subject"]["category"]][clue["subject"]["item"]]
        o = assign[clue["object"]["category"]][clue["object"]["item"]]
        solver.add(s == o)

    elif ctype == "negation":
        s = assign[clue["subject"]["category"]][clue["subject"]["item"]]
        o = assign[clue["object"]["category"]][clue["object"]["item"]]
        solver.add(s != o)

    elif ctype == "conditional":
        a = assign[clue["if"]["category"]][clue["if"]["item"]]
        b = assign[clue["then"]["category"]][clue["then"]["item"]]
        solver.add(a == b)

    elif ctype == "self_exclusion":
        cat_a = clue["category_a"]
        cat_b = clue["category_b"]
        for a_item, b_item in clue["mapping"].items():
            solver.add(assign[cat_a][a_item] != assign[cat_b][b_item])

    else:
        raise ValueError(f"Unknown clue type: {ctype}")


def encode_all_clues(solver: Solver, assign: dict, puzzle: dict):
    for clue in puzzle["clues"]:
        encode_clue(solver, assign, clue)
