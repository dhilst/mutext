# μ-text

A narrative troubleshooting simulator. You are an entry-level engineer in the
Troubleshooting Department, reconstructing AI-generated software failures after
they have already reached customers. Each incident is a deduction grid and a
story, and the incidents are not as unrelated as they look.

**Play it: <https://dhilst.github.io/mutext/>**

Sixteen chapters, starting with the interview. Deadlocks, race conditions,
starvation, split brain, and worse. No account, no backend, nothing to install.

---

## Running it locally

Jekyll runs from the vendored bundle path and Tailwind from the local npm
dependency:

```bash
npm run serve        # http://127.0.0.1:4000/
```

`npm run build` is for the GitHub Pages deploy only — it writes production
paths into `_site/` and will break a running dev server. Restart `serve`
instead if you need to rebuild Tailwind.

## Verifying the puzzles

Every puzzle is verified offline by a Z3 solver before it ships. A puzzle
passes only when it has exactly one solution, that solution is the declared
answer, every clue is load-bearing, and the page the player reads agrees with
the model the solver checked.

```bash
npm run check        # what CI runs
```

That is three things:

| Command | Checks |
|---|---|
| `npm run check:puzzles` | solvable, unique, correct — and no vacuous, duplicate or removable clue |
| `npm run check:continuity` | the evidence ledger, the chapter link chain, no meta-language in player-facing prose |
| `npm run test:puzzles` | the checker's own test suite |

Both CI workflows run all three, so a puzzle with a dead clue or a chapter that
breaks the evidence chain cannot reach the site.

Authoring a new puzzle starts from the intended solution:

```bash
cd checker
uv run make_puzzle.py specs/017-something.yaml --prefer-direct 0.2
```

It returns a minimal sufficient clue set — no clue you could delete without
making the puzzle ambiguous.

## Layout

```
_posts/            one chapter per file, each paired with a checker input
_lore/             free-standing in-world artifacts
_data/evidence.yml strings more than one chapter has to agree on
_includes/         the grid, panels, terminal windows, evidence cards
checker/           the offline solver and linters (never shipped to the site)
docs/              specs and design notes (excluded from the build)
```

`docs/puzzle-spec.md` covers the grid and the authoring order,
`docs/sat-checker.md` the clue grammar and the quality rules. Both `checker/`
and `docs/` are excluded from the build, because they contain answers.

> [!NOTE]
> `docs/` contains the full design notes for all sixteen chapters, including
> solutions and the story outline. It is worth not reading before playing.
