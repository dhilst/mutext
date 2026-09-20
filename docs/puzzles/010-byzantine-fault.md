# Puzzle 10: Byzantine Fault

The peak. 5 categories × 5 items, 20×20 grid, 19 clues — and two gated stages.

## Lore Start

INC-0010. Five attestation replicas are supposed to agree on one digest per
epoch. They do not. Every report is internally consistent, correctly formatted
and correctly countersigned, and they describe five different histories. Nothing
is corrupted; one participant is simply saying something else, carefully.

## Grid Instantiation

D = 5, N = 5. Grid order: replica, digest, epoch, key, stream.

Tokens are two characters so they fit a 20-column grid, and they are reused
verbatim as `<option value>` attributes so the grid and the answer widget cannot
drift. The readable name lives in the option text and in the registry panel.

| Category | Tokens | Registry |
|---|---|---|
| replica | `r1`–`r5` | repl-aurora, repl-borealis, repl-cinder, repl-dune, repl-ember |
| digest | `d1`–`d5` | 0x41ae, 0x7c02, 0x9f31, 0xb4d8, 0xe016 |
| epoch | `e1`–`e5` | 0411, 0412, 0414, 0416, 0419 |
| key | `k1`–`k5` | att.ops, att.rel, att.bot, **r.sato**, att.arc |
| stream | `s1`–`s5` | tel/hrs-02, tel/hrs-03, tel/hrs-05, **tel/hrs-07**, tel/hrs-11 |

```liquid
{% include zebra-table.html cols_a="r1|r2|r3|r4|r5" cols_b="d1|d2|d3|d4|d5" cols_c="e1|e2|e3|e4|e5" cols_d="k1|k2|k3|k4|k5" rows_a="s1|s2|s3|s4|s5" rows_b="k1|k2|k3|k4|k5" rows_c="e1|e2|e3|e4|e5" rows_d="d1|d2|d3|d4|d5" %}
```

Rows are the reverse of the grid order (stream, key, epoch, digest): ten active
blocks, ten category pairs, no self-block. 250 active cells.

Answer order: replica, digest, epoch, key, stream.

## Identification Rule

The metadata strip: **keys 5 · service keys 4**. The registry panel shows why —
four of the countersigning keys are service identities, and one is a person's
name. The divergent attestation is the one carrying `k4`.

## Why this fits the grid

Byzantine faults look like they need agreement counts, which a zebra grid cannot
hold (a category may not repeat a value). They do not: the *interesting* case is
the one where five participants report five different things, and mutual
disagreement is exactly a bijection. Which report was legitimate is decided by a
rule stated in-world, not by the grid.

## Clues

Nineteen, all load-bearing. See `checker/puzzles/010-byzantine-fault.yaml` for
the prose, which the post carries verbatim.

## Answer — stage 1

```
r3, d5, e4, k4, s4
```

repl-cinder, digest 0xe016, epoch 0416, countersigned r.sato, published into
tel/hrs-07.

Three things land at once, and all three are things the player has already seen:

* the key is Rin's, last seen in chapter 4 and again on chapter 7's commit;
* the epoch is `0416`, which is Nix's chapter 6 coordinate;
* the stream is `tel/hrs-07`, which is the undocumented fifth reader from
  chapter 8 and the `s07` in chapter 3's fragment.

## Stage 2

A second `[data-puzzle-answer]` block, inside `#lore-reveal`, with
`data-reveal="#lore-reveal-2"` and no grid: three selects for stream, epoch and
source.

```
tel/hrs-07, 0416, harness-04
```

Those are chapters 3, 6 and 9's fragments. The three evidence cards are rendered
on the page from `_data/evidence.yml`, so the deduction is "combine what you were
given", not "remember what you read six chapters ago".

`#lore-reveal-2` holds the diversion schedule, names HORUS, and carries the NEXT
INCIDENT link — so the chapter genuinely gates on both stages.

## The record

The record must **not** say Horus did it. It is a scheduling table, repeated for
nine incidents:

```
incident              INC-0002
diversion             scheduled
harness window        09:20 - 09:55
expected response     94%
operator coverage     6%
```

The player derives the conclusion: the incidents were generated to create the
windows, and every window carries a harness patch signed with Rin's key.

## Continuity

* Consumes: `nx_ch3`, `nx_ch6`, `nx_ch9`, `obs_ch8`, `rin_key_ch4`, and chapter
  7's "a signature proves possession, not presence".
* Plants: `horus_ch10` — the name, the diversion schedule, and the fact that
  Horus has write permission on a stream it was only ever meant to observe.
* Must NOT: explain what Horus is, say who deployed it, connect it to Jeff, or
  give Nix an identity. Andy learns what has been happening and nothing about who.
