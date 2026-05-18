import yaml
from pathlib import Path


def load_puzzle(path: Path) -> dict:
    with open(path) as f:
        puzzle = yaml.safe_load(f)

    required = ["name", "dimensions", "size", "categories", "answer", "clues"]
    for key in required:
        if key not in puzzle:
            raise ValueError(f"Missing required key: {key}")

    d = puzzle["dimensions"]
    n = puzzle["size"]

    if len(puzzle["categories"]) != d:
        raise ValueError(f"Expected {d} categories, got {len(puzzle['categories'])}")

    for cat in puzzle["categories"]:
        if len(cat["items"]) != n:
            raise ValueError(
                f"Category '{cat['name']}' has {len(cat['items'])} items, expected {n}"
            )

    if len(puzzle["answer"]) != d:
        raise ValueError(f"Answer must have {d} entries, got {len(puzzle['answer'])}")

    cat_names = {cat["name"] for cat in puzzle["categories"]}
    for cat_name in puzzle["answer"]:
        if cat_name not in cat_names:
            raise ValueError(f"Answer references unknown category: {cat_name}")

    return puzzle
