"""Typed representation of a puzzle, built by the loader."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Endpoint:
    category: str
    item: str

    def __str__(self) -> str:
        return f"{self.category}:{self.item}"


@dataclass(frozen=True)
class Category:
    name: str
    items: tuple[str, ...]
    line: int | None = None


@dataclass
class Clue:
    index: int                      # 0-based position in the YAML clue list
    type: str                       # canonical type (aliases already resolved)
    raw: dict
    post_numbers: tuple[int, ...] = ()
    prose: tuple[str, ...] = ()
    keep_redundant: bool = False
    note: str | None = None
    line: int | None = None

    @property
    def number(self) -> int:
        return self.index + 1


@dataclass
class PostRef:
    path: str
    panel_title: str = "evidence"
    answer_order: tuple[str, ...] = ()
    narrative_only: tuple[int, ...] = ()
    line: int | None = None


@dataclass
class Puzzle:
    name: str
    dimensions: int
    size: int
    categories: tuple[Category, ...]
    answer: dict[str, str]
    clues: list[Clue]
    path: Path
    post: PostRef | None = None
    allow_duplicate_items: bool = False

    def category(self, name: str) -> Category | None:
        for c in self.categories:
            if c.name == name:
                return c
        return None

    @property
    def category_names(self) -> tuple[str, ...]:
        return tuple(c.name for c in self.categories)

    def items_of(self, name: str) -> tuple[str, ...]:
        cat = self.category(name)
        return cat.items if cat else ()

    @property
    def answer_order(self) -> tuple[str, ...]:
        if self.post and self.post.answer_order:
            return self.post.answer_order
        return tuple(self.answer.keys())

    @property
    def answer_tuple(self) -> tuple[str, ...]:
        return tuple(self.answer[c] for c in self.answer_order)
