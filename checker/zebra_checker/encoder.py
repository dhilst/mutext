from z3 import Int, Solver, Distinct


def build_variables(puzzle: dict) -> dict:
    assign = {}
    for cat in puzzle["categories"]:
        name = cat["name"]
        assign[name] = {}
        for item in cat["items"]:
            assign[name][item] = Int(f"{name}__{item}")
    return assign


def add_axioms(solver: Solver, assign: dict, puzzle: dict):
    n = puzzle["size"]
    for cat in puzzle["categories"]:
        name = cat["name"]
        variables = [assign[name][item] for item in cat["items"]]
        for v in variables:
            solver.add(v >= 0, v < n)
        solver.add(Distinct(*variables))

    # Symmetry breaking: fix first category to canonical ordering
    # Entity numbers are arbitrary labels — pin them via the first category
    first_cat = puzzle["categories"][0]
    for i, item in enumerate(first_cat["items"]):
        solver.add(assign[first_cat["name"]][item] == i)
