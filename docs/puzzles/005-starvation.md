# Puzzle 5: Starvation

## Lore Start

INC-0005. A retry lane has stopped moving. Nothing has crashed, nothing is
deadlocked, and every consumer is reported healthy — one of them simply never
gets scheduled, and its work has been ageing out into the dead-letter lane for
most of a day.

Bob's framing: starvation is not a failure, it is an outcome. Something is always
more urgent.

## Grid Instantiation

D = 3, N = 3. Grid order: consumer, ack, lane.

| Category | Items | Select label |
|---|---|---|
| consumer | `ingest` `settle` `notify` | consumer |
| ack | `14s` `9m` `19h` | last ack |
| lane | `q-hot` `q-warm` `q-dead` | lane |

```liquid
{% include zebra-table.html cols_a="ingest|settle|notify" cols_b="14s|9m|19h" rows_a="q-hot|q-warm|q-dead" rows_b="14s|9m|19h" %}
```

Rows are the reverse of the grid order (G3, G2), so the active blocks are
lane×consumer, lane×ack and ack×consumer — each pair once, no self-block.

Answer order: consumer, lane, ack.

## Identification Rule

The metadata strip carries the SLA: **ack budget 30m**. Exactly one
acknowledgement in the grid is outside it, so the starved consumer is the one
holding `19h`. The grid supplies which consumer that is and which lane it is
stuck on.

## Puzzle Entities

* Consumers: `ingest`, `settle`, `notify`
* Last acknowledgement: `14s`, `9m`, `19h`
* Lanes: `q-hot`, `q-warm`, `q-dead`

## Clues

1. The consumer whose last acknowledgement was `14s` is the one attached to `q-dead`.
2. `notify` did not record the `19h` acknowledgement.
3. No consumer on `q-hot` has been silent for `19h`.
4. `ingest` consumes from `q-dead`.

## Solve Path

1. Clues 4 and 1 put `ingest` on `q-dead` with a `14s` ack.
2. That leaves `9m` and `19h` for `settle` and `notify`; clue 2 gives `notify` = `9m`,
   so `settle` = `19h`.
3. `19h` is not `q-hot` (clue 3) and not `q-dead` (that is `ingest`), so `settle`
   is on `q-warm` and `notify` on `q-hot`.
4. `19h` is the only ack outside the 30-minute budget: `settle` is starving.

## Answer

```
settle, q-warm, 19h
```

## Continuity

* Consumes: nothing.
* Plants: the maintenance-window timeline in the reveal — every maintenance slot
  in the last three weeks was interrupted by an incident. Chapter 10 needs the
  player to already find that pattern unremarkable before it turns out to be the
  whole point.
* Must NOT: name Horus, imply the incidents are deliberate, or give Bob any
  insight he could not have from twenty years of on-call.

## Lore Reveal

`settle` is runnable and has been runnable all day. It loses every scheduling
round to incident traffic on `q-hot`, and its work ages into `q-dead` behind it.

Terminal diagram: the scheduler round, showing `settle` eligible and passed over
on every pass.

Loose thread: Andy pulls the maintenance calendar. Twenty-one scheduled windows
in three weeks. Twenty-one incidents. He assumes it is what it looks like —
a team too busy to maintain anything.
