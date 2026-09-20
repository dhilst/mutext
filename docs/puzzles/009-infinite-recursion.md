# Puzzle 9: Infinite Recursion

## Lore Start

INC-0009. The automated repair service treats its own repairs as defects. Four
stages in a ring, each one correcting the output of the last; one of them lost
its termination condition, so the ring never unwinds.

## Grid Instantiation

D = 4, N = 4. Grid order: frame, calls, depth, stack.

| Category | Items | Select label |
|---|---|---|
| frame | `resolve` `expand` `inline` `emit` | frame |
| calls | `→resolve` `→expand` `→inline` `→emit` | calls |
| depth | `d-128` `d-512` `d-4k` `d-∞` | depth |
| stack | `4 MB` `32 MB` `256 MB` `2 GB` | stack |

```liquid
{% include zebra-table.html cols_a="resolve|expand|inline|emit" cols_b="→resolve|→expand|→inline|→emit" cols_c="d-128|d-512|d-4k|d-∞" rows_a="4 MB|32 MB|256 MB|2 GB" rows_b="d-128|d-512|d-4k|d-∞" rows_c="→resolve|→expand|→inline|→emit" %}
```

Answer order: frame, calls, depth, stack.

## Identification Rule

The metadata strip carries the unwind budget: **d-8k**. Three frames report a
finite depth inside it. One reports `d-∞` and is still climbing, at `2 GB` of
stack. That frame is the one whose base condition no longer fires.

## Why the self-exclusion clue matters here

`calls` is a category of arrows over the same four frames, so clue 1 is the
chapter-2 `self_exclusion` pattern: no frame calls itself. At N = 3 a derangement
is forced to be a single 3-cycle, which is why chapter 6 avoided this shape — it
would have re-run chapter 2. At N = 4 the derangement can be one 4-cycle or two
2-cycles, so the clue does real work and the ring has to be reconstructed.

## Clues

1. No frame re-enters itself directly. Every call in the trace is to a different frame.
2. `resolve` bottomed out at `d-128`.
3. `resolve` calls `expand`.
4. `emit` peaked at `32 MB` of stack.
5. The frame that reached `d-4k` peaked at `256 MB`.
6. Whatever calls `inline` also peaked at `256 MB`.
7. The frame that calls `expand` did not reach `2 GB`.
8. `inline` did not stop at `d-512`.
9. *(narrative)* A fragment recovered from frame 4096 of the cascade.

## Solve Path

1. Clues 5 and 6 put `d-4k`, `256 MB` and `→inline` on one frame.
2. Clues 2, 3 and 7 fix `resolve` at `d-128`, `→expand`, and not `2 GB`; with
   clue 4 taking `32 MB` for `emit`, `resolve` is `4 MB`.
3. `256 MB` and `2 GB` remain for `expand` and `inline`. Clue 1 forbids `inline`
   from calling itself, so the `→inline` frame is `expand`: `expand` takes
   `256 MB` and `d-4k`, `inline` takes `2 GB`.
4. Clue 8 rules out `d-512`, so `inline` is `d-∞` and `emit` is `d-512`.
5. Clue 1 finishes the ring: `emit` calls `resolve`, `inline` calls `emit`.

## Answer

```
inline, →emit, d-∞, 2 GB
```

## Continuity

* Consumes: nothing.
* Plants: **Nix fragment #3** — ledger key `nx_ch9`, the source coordinate
  `harness-04`. It arrives in the cascade noise, at a stack depth nobody would
  read by hand.
* This is also the fragment that tells Andy the three belong *together*. He now
  has a stream (chapter 3), an epoch (chapter 6) and a source (chapter 9), and
  for the first time a reason to put them on the same page.
* Must NOT: say what they open, name a system, or let Andy successfully use them.
  Chapter 10 is where they resolve, and only after its own puzzle is solved.

## Lore Reveal

The ring: `resolve` → `expand` → `inline` → `emit` → `resolve`. Each stage
repairs the previous stage's output; `inline`'s base condition compared a
normalised value to an unnormalised one, so it never matched, so nothing ever
stopped.

Terminal diagram: the repair ring with the depth counters, and the base-condition
line that can never be true.

Loose thread: three fragments, written down together for the first time.
