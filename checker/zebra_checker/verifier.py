from z3 import Solver, Or, sat
from .encoder import build_variables, add_axioms
from .clues import encode_all_clues


def verify_puzzle(puzzle: dict, verbose: bool = False) -> bool:
    n = puzzle["size"]
    name = puzzle["name"]
    d = puzzle["dimensions"]

    print(f"\n=== {name} ({d}×{n}) ===")
    cat_summary = ", ".join(
        f"{c['name']}({n})" for c in puzzle["categories"]
    )
    print(f"Categories: {cat_summary}")
    print(f"Clues: {len(puzzle['clues'])}")

    solver = Solver()
    assign = build_variables(puzzle)
    add_axioms(solver, assign, puzzle)
    encode_all_clues(solver, assign, puzzle)

    print(f"\n[1/3] Solving...", end=" ")
    result = solver.check()
    if result != sat:
        print("UNSAT")
        print("FAIL — no solution exists (puzzle is over-constrained)")
        return False
    print("SAT ✓")

    model = solver.model()

    if verbose:
        print_solution(model, assign, puzzle)

    print(f"[2/3] Answer check...", end=" ")
    answer_ok = check_answer(model, assign, puzzle)
    if not answer_ok:
        print("MISMATCH")
        print("FAIL — model does not match expected answer")
        return False
    print("MATCH ✓")

    print(f"[3/3] Uniqueness...", end=" ")
    solver.push()
    block = Or(*[
        assign[cat["name"]][item] != model.eval(assign[cat["name"]][item])
        for cat in puzzle["categories"]
        for item in cat["items"]
    ])
    solver.add(block)
    uniqueness = solver.check()

    if uniqueness == sat:
        print("NOT UNIQUE")
        alt = solver.model()
        print("FAIL — multiple solutions exist (puzzle is under-constrained)")
        if verbose:
            print("\nAlternate solution:")
            print_solution(alt, assign, puzzle)
        solver.pop()
        return False
    solver.pop()
    print("UNIQUE ✓")

    print("\nPASS")
    return True


def check_answer(model, assign: dict, puzzle: dict) -> bool:
    answer = puzzle["answer"]
    entity_numbers = {}
    for cat_name, item_name in answer.items():
        val = model.eval(assign[cat_name][item_name])
        entity_numbers[cat_name] = val.as_long()

    values = set(entity_numbers.values())
    return len(values) == 1


def print_solution(model, assign: dict, puzzle: dict):
    n = puzzle["size"]
    entities = {}
    for cat in puzzle["categories"]:
        for item in cat["items"]:
            e = model.eval(assign[cat["name"]][item]).as_long()
            if e not in entities:
                entities[e] = {}
            entities[e][cat["name"]] = item

    print()
    for e in sorted(entities):
        parts = [f"{cat}={entities[e][cat]}" for cat in entities[e]]
        label = " ANSWER" if is_answer_entity(e, assign, puzzle, model) else ""
        print(f"  Entity {e}: {', '.join(parts)}{label}")
    print()


def is_answer_entity(entity_num: int, assign: dict, puzzle: dict, model) -> bool:
    answer = puzzle["answer"]
    first_cat = next(iter(answer))
    first_item = answer[first_cat]
    return model.eval(assign[first_cat][first_item]).as_long() == entity_num
