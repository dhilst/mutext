# Puzzle Framework Specification

## Overview

Each puzzle is a zebra-logic deduction grid with D categories of N items each.
The player solves by elimination and cross-referencing, then submits a D-tuple answer via select boxes.

---

## Dimensions

| Difficulty | Categories (D) | Items (N) | Grid size         | Active blocks | Active cells |
|------------|----------------|-----------|-------------------|---------------|--------------|
| Easy       | 3              | 3         | 6×6               | 3             | 27           |
| Medium     | 4              | 4         | 12×12             | 6             | 96           |
| Hard       | 5              | 5         | 20×20             | 10            | 250          |

### 5D compact labels

With 20 columns, items need short labels (≤3 chars). Use a shape prefix per category:

| Category | Prefix | Items                     |
|----------|--------|---------------------------|
| Service  | ◆      | ◆1  ◆2  ◆3  ◆4  ◆5       |
| Token    | ▲      | ▲a  ▲b  ▲c  ▲d  ▲e       |
| Resource | ●      | ●α  ●β  ●γ  ●δ  ●ε       |
| Host     | ■      | ■Ⅰ  ■Ⅱ  ■Ⅲ  ■Ⅳ  ■Ⅴ       |
| Error    | ✦      | ✦1  ✦2  ✦3  ✦4  ✦5       |

Formula: grid is `(D-1)×N` rows by `(D-1)×N` columns.

---

## Grid Topology

The grid is divided into `(D-1)²` blocks, each of size `N×N`.

### 3 dimensions (6×6)

```
 A | B
---+---
 C | .
```

- Active blocks: A, B, C (3 = C(3,2))
- Disabled blocks: 1 (bottom-right corner)

### 4 dimensions (12×12)

```
 A | B | C
---+---+---
 D | E | .
---+---+---
 F | . | .
```

- Active blocks: A, B, C, D, E, F (6 = C(4,2))
- Disabled blocks: 3 (lower-right triangle)

### 5 dimensions (20×20)

```
 A | B | C | D
---+---+---+---
 E | F | G | .
---+---+---+---
 H | I | . | .
---+---+---+---
 J | . | . | .
```

- Active blocks: A–J (10 = C(5,2))
- Disabled blocks: 6 (lower-right triangle)

### Disable rule

A block at position `(row_idx, col_idx)` (0-indexed) is disabled when:

```
row_idx + col_idx >= D - 1
```

Disabled blocks render as dark empty cells with no interaction.

---

## Category-to-Block Mapping

Given D categories numbered 1 through D:

- **Column groups** (left to right): Category 1, Category 2, ..., Category D-1
- **Row groups** (top to bottom): Category 2, Category 3, ..., Category D

Each active block represents a pairwise relationship between two different categories.
The disabled blocks sit where a category would cross itself.

### Example: 3 categories (Process, Token, Resource)

- Columns: Process (group 0), Token (group 1)
- Rows: Token (group 0), Resource (group 1)
- Block (0,0): Token × Process — active
- Block (0,1): Token × Token — disabled
- Block (1,0): Resource × Process — active
- Block (1,1): Resource × Token — active

### Example: 4 categories (Process, Token, Resource, Host)

- Columns: Process (0), Token (1), Resource (2)
- Rows: Token (0), Resource (1), Host (2)
- Disabled: (0,1) Token×Token, (1,2) Resource×Resource, (2,2+) out of bounds — but using the formula: disabled at (0,1), (1,2), (2,1), (2,2)... 

Correction using the formula `row_idx + col_idx >= D-1 = 3`:
- (0,0)=0 active, (0,1)=1 active, (0,2)=2 active
- (1,0)=1 active, (1,1)=2 active, (1,2)=3 **disabled**
- (2,0)=2 active, (2,1)=3 **disabled**, (2,2)=4 **disabled**

Active blocks: 6 ✓

---

## Cell States

Each active cell cycles through 3 states on click:

| State | Class      | Label | Meaning      |
|-------|------------|-------|--------------|
| 0     | (none)     | (empty) | Unknown    |
| 1     | `is-x`    | ✕     | Eliminated   |
| 2     | `is-check` | ✓    | Confirmed    |

Cell state is persisted in localStorage keyed by `mutext-grid-{pathname}`.

---

## Answer Input Component

The answer is a D-tuple. Each dimension is a `<select>` element populated with that category's items.

### Structure

```html
<div data-puzzle-answer="parser, token-beta, /models">
  <div class="flex flex-wrap items-center gap-3">
    <select data-answer-dim="0">
      <option value="">— process —</option>
      <option value="parser">parser</option>
      <option value="crawler">crawler</option>
      <option value="renderer">renderer</option>
    </select>
    <select data-answer-dim="1">
      <option value="">— token —</option>
      <option value="token-alpha">token-alpha</option>
      <option value="token-beta">token-beta</option>
      <option value="token-gamma">token-gamma</option>
    </select>
    <select data-answer-dim="2">
      <option value="">— resource —</option>
      <option value="/cache">/cache</option>
      <option value="/logs">/logs</option>
      <option value="/models">/models</option>
    </select>
    <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
  </div>
</div>
```

### Validation logic

The JS iterates all `[data-puzzle-answer]` elements on the page, wiring each independently:

```js
document.querySelectorAll("[data-puzzle-answer]").forEach((answerEl) => {
  const expected = answerEl.getAttribute("data-puzzle-answer")
    .split(",").map(s => s.trim().toLowerCase());
  const submitBtn = answerEl.querySelector('[data-fake-action="SUBMIT"]');
  const selects = answerEl.querySelectorAll("select[data-answer-dim]");
});
```

Validation is **exact positional match** against the select values:

```js
const selected = Array.from(selects).map(s => s.value.trim().toLowerCase());
const correct = expected.length === selected.length
  && expected.every((val, i) => val === selected[i]);
```

### Behavior

- On correct: button shows "CORRECT" with `button-correct` class, confetti fires, `#lore-reveal` unhides
- On incorrect: button shows "INCORRECT" with `button-incorrect` class for 3s, then resets
- Multiple answer sections per page are supported independently

---

## Page Layout

### Small screens (stacked, single column)

```
┌─────────────────────────────┐
│           LORE              │
├─────────────────────────────┤
│           CLUES             │
├─────────────────────────────┤
│          MESSAGES           │
├─────────────────────────────┤
│        PUZZLE GRID          │
│                             │
│                             │
│              [clear board]  │
├─────────────────────────────┤
│       ANSWER INPUT          │
│   [select] [select] [...]   │
│   [submit]                  │
├─────────────────────────────┤
│    LORE END (after solve)   │
└─────────────────────────────┘
```

### Large screens (two-column)

```
┌──────────────────────────────────────────────┐
│                    LORE                       │
├──────────────┬───────────────────────────────┤
│              │                               │
│   CLUES      │        PUZZLE GRID            │
│              │                               │
├──────────────┤                               │
│              │                               │
│  MESSAGES    ├───────────────────────────────┤
│              │       ANSWER INPUT            │
│              │   [select] [select] [...]     │
│              │   [submit]                    │
├──────────────┴───────────────────────────────┤
│              LORE END (after solve)          │
└──────────────────────────────────────────────┘
```

### Implementation

The layout uses existing includes:

```liquid
{% include lore-block.html %}
  ...narrative...
{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}
    (clues panel)
    (messages panel)
  {% include puzzle-col_end.html %}
  {% include puzzle-col.html %}
    (grid panel with zebra-table include)
    (answer input panel)
  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
  ...post-solve content...
</section>
```

- `puzzle-grid.html` = `<section class="grid gap-5 lg:grid-cols-[minmax(14rem,0.7fr)_minmax(0,1.3fr)]">`
- `puzzle-col.html` = `<div class="space-y-5">`
- On mobile: columns stack vertically (left column first, then right)
- On `lg:` breakpoint: side-by-side with left column narrower

---

## Zebra Table Include

File: `_includes/zebra-table.html`

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `cols_a`  | yes      | Pipe-delimited items for column group 1 |
| `cols_b`  | yes      | Pipe-delimited items for column group 2 |
| `cols_c`  | no       | Pipe-delimited items for column group 3 (4D+) |
| `rows_a`  | yes      | Pipe-delimited items for row group 1 |
| `rows_b`  | yes      | Pipe-delimited items for row group 2 |
| `rows_c`  | no       | Pipe-delimited items for row group 3 (4D+) |

### Usage

3D puzzle:
```liquid
{% include zebra-table.html
   cols_a="parser|crawler|renderer"
   cols_b="/cache|/logs|/models"
   rows_a="token-alpha|token-beta|token-gamma"
   rows_b="/cache|/logs|/models"
%}
```

4D puzzle:
```liquid
{% include zebra-table.html
   cols_a="proc-A|proc-B|proc-C|proc-D"
   cols_b="tok-1|tok-2|tok-3|tok-4"
   cols_c="res-W|res-X|res-Y|res-Z"
   rows_a="tok-1|tok-2|tok-3|tok-4"
   rows_b="res-W|res-X|res-Y|res-Z"
   rows_c="host-α|host-β|host-γ|host-δ"
%}
```

### Disabled block rendering

- Active cells: `<button class="zebra-cell" data-grid-cell>` — interactive
- Disabled cells: empty `<td>` with `bg-slate-950/80` — no button, no interaction
- Group separators: `border-l-2 border-l-slate-600` (vertical) and `border-t-2 border-t-slate-600` (horizontal)

### 5D support

The include accepts `cols_d`/`rows_d` for 5D grids. The disable rule generalizes: disabled when `row_group_idx + col_group_idx >= num_col_groups`.

5D example (compact labels):
```liquid
{% include zebra-table.html
   cols_a="◆1|◆2|◆3|◆4|◆5"
   cols_b="▲a|▲b|▲c|▲d|▲e"
   cols_c="●α|●β|●γ|●δ|●ε"
   cols_d="■Ⅰ|■Ⅱ|■Ⅲ|■Ⅳ|■Ⅴ"
   rows_a="▲a|▲b|▲c|▲d|▲e"
   rows_b="●α|●β|●γ|●δ|●ε"
   rows_c="■Ⅰ|■Ⅱ|■Ⅲ|■Ⅳ|■Ⅴ"
   rows_d="✦1|✦2|✦3|✦4|✦5"
%}
```

---

## Puzzle Post Data Format

Each puzzle is a Jekyll post in `_posts/` with this structure:

### Front matter

```yaml
---
title: "INC-XXXX Title"
description: "One-line description for meta tags"
permalink: /puzzles/slug.html
---
```

### Required sections

1. **Lore intro** — narrative framing (chapter, label)
2. **Clues panel** — numbered evidence list
3. **Messages panel** — 2–3 chat messages from Bob explaining the grid
4. **Grid panel** — incident metadata + `zebra-table.html` include + clear button
5. **Answer panel** — question text + select boxes + submit button
6. **Lore reveal** — hidden section shown after correct answer

### Answer encoding

The correct answer is stored as a `data-puzzle-answer` attribute on a wrapper div.
Value is comma-separated, positional, case-insensitive:

```html
<div data-puzzle-answer="parser, token-beta, /models">
```

---

## JavaScript Contract

File: `assets/js/main.js`

### Grid system (already generic)

- Queries all `[data-grid-cell]` on the page
- State cycles: 0 → 1 → 2 → 0 (empty → ✕ → ✓)
- Persistence: `localStorage["mutext-grid-" + pathname]` — array of state integers
- Clear: `[data-clear-grid]` button resets all cells with confirmation

### Answer validation

- Iterates all `[data-puzzle-answer]` elements, wires each independently
- Validates `select[data-answer-dim]` values by exact positional match
- On correct: adds `button-correct` class, fires `spawnConfetti()`, unhides `#lore-reveal`
- On incorrect: shows `button-incorrect` for 3s, then resets

### No puzzle-specific code

The JS is fully generic. All puzzle-specific data lives in the HTML (grid structure, answer value, category items in selects).

---

## Constraints

- No note-taking required — all deduction must be trackable on the grid alone
- No backend — all validation is client-side
- Answer is visible in page source (acceptable for prototype)
- Grid state persists across page reloads via localStorage
- Each puzzle page must be self-contained (no shared state between puzzles)

---

## Axioms

### Axiom I — One match per row and column in every block

For each N×N block, exactly one ✓ must appear in every row and exactly one ✓ in every column. All other cells are ✕.

Valid (3×3 block):

```
✓ | ✕ | ✕
--+---+---
✕ | ✕ | ✓
--+---+---
✕ | ✓ | ✕
```

Valid (3×3 block):

```
✕ | ✕ | ✓
--+---+---
✓ | ✕ | ✕
--+---+---
✕ | ✓ | ✕
```

Invalid — row 1 has two ✓:

```
✓ | ✓ | ✕
--+---+---
✕ | ✕ | ✓
--+---+---
✕ | ✕ | ✕
```

Invalid — column 1 has two ✓:

```
✓ | ✕ | ✕
--+---+---
✓ | ✕ | ✕
--+---+---
✕ | ✕ | ✓
```

Invalid — row 3 has no ✓:

```
✓ | ✕ | ✕
--+---+---
✕ | ✓ | ✕
--+---+---
✕ | ✕ | ✕
```

Invalid — column 2 has no ✓:

```
✓ | ✕ | ✕
--+---+---
✕ | ✕ | ✓
--+---+---
✕ | ✕ | ✕
```

This constraint holds for every active block independently. A valid solution is a permutation matrix in each block.

### Axiom II — Answer dimensionality matches puzzle dimensionality

The answer is always a D-tuple for a D-dimensional puzzle:

- 3D puzzle → 3 selects (one value per category)
- 4D puzzle → 4 selects (one value per category)
- 5D puzzle → 5 selects (one value per category)

---

## Examples

### 3D puzzle (tutorial)

- Categories: Process (parser, crawler, renderer), Token (alpha, beta, gamma), Resource (/cache, /logs, /models)
- Grid: 6×6, 27 active cells
- Answer: 3 selects (process, token, resource)
- Clues: 6 (direct + relational)

### 3D puzzle (the lockup)

- Categories: Process (P1, P2, P3), Lock (L1, L2, L3), Call Target (→P1, →P2, →P3)
- Grid: 6×6, 27 active cells
- Answer: 3 selects (process, lock, call target)
- Clues: 5

### 4D puzzle (future)

- Categories: Process, Token, Resource, Host — each with 4 items
- Grid: 12×12, 96 active cells
- Answer: 4 selects (one per category)
- Clues: 8–12
