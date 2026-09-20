# Puzzle 7: Priority Inversion

## Lore Start

INC-0007. The release gate has been blocked for two hours on a mutex held by the
lowest-priority task in the system, and a middle-priority task keeps preempting
the holder before it can finish and let go. Three priorities, one lock, and a
scheduler doing exactly what it was configured to do.

First puzzle at four items per category — an 8×8 grid.

## Grid Instantiation

D = 3, N = 4. Grid order: task, priority, mutex.

| Category | Items | Select label |
|---|---|---|
| task | `t-audit` `t-render` `t-billing` `t-gc` | task |
| priority | `P0` `P1` `P2` `P3` | priority |
| mutex | `m-io` `m-db` `m-log` `m-tmp` | holds |

```liquid
{% include zebra-table.html cols_a="t-audit|t-render|t-billing|t-gc" cols_b="P0|P1|P2|P3" rows_a="m-io|m-db|m-log|m-tmp" rows_b="P0|P1|P2|P3" %}
```

Answer order: task, priority, mutex.

## Identification Rule

The metadata strip carries the wait edge: **blocked: P0 → m-db**. So the culprit
row is whoever *holds* `m-db`. The grid supplies which task that is and what
priority it runs at — and the fact that the priority turns out to be `P3` is the
finding, not an input.

## Clues

1. The task running at `P1` holds `m-tmp`.
2. `m-log` is not held by the `P0` task.
3. `t-render` holds `m-io`.
4. `t-audit` does not run at `P3`.
5. Whatever holds `m-log`, it is not running at `P3`.
6. `t-billing` runs at `P1`.
7. The `P0` task does not hold `m-db` — it is waiting on it.

## Solve Path

1. Clues 6 and 1: `t-billing` = `P1` = `m-tmp`.
2. Clue 3 gives `t-render` = `m-io`; clues 2 and 7 leave `P0` only `m-io`, so
   `t-render` is the blocked release gate.
3. Clue 5 and the taken locks leave `P3` = `m-db`.
4. Clue 4 rules `t-audit` out of `P3`, and `t-render`/`t-billing` are placed, so
   `t-gc` holds `m-db` at `P3`. `t-audit` takes `P2` and `m-log`.

## Answer

```
t-gc, P3, m-db
```

## Continuity

* Consumes: `rin_key_ch4` — Rin's key, introduced in chapter 4 as a scrubbed
  maintainer record.
* Plants, and this is the load-bearing one for chapter 16: **a signature proves
  possession of a key, not the presence of a person.** Andy says it as a flat
  technical fact while explaining how the scheduler class was changed. He does
  not treat it as a suspicion, and nobody argues.
* Plants: the scheduler class change was committed after Rin's last day, signed
  correctly, reviewed by nobody.
* Must NOT: suggest the key was stolen, suggest Rin is alive and active, or let
  Bob say anything that implies he knows who is using it.

## Lore Reveal

`t-gc` holds `m-db` at `P3`. `t-render` at `P0` waits. `t-billing` at `P1`
preempts `t-gc` every time it becomes runnable, so the lowest-priority task can
never finish and release, and the highest-priority task waits on the
lowest-priority task by way of the middle one.

Terminal diagram: the three-priority timeline showing P3 preempted mid-section
while P0 waits.

Loose thread: `t-gc` was moved from `P1` to `P3` in a commit signed with Rin's
key, dated eleven days after Rin's last recorded activity.
