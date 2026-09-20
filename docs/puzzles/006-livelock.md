# Puzzle 6: Livelock

## Lore Start

INC-0006. Two recovery workers respond to each other's recovery. Both are
running hot, both are changing state constantly, and between them they complete
nothing. A third worker is unaffected and doing all of the actual work, which is
why the dashboards look survivable.

Bob's framing: a deadlock is polite about it. A livelock looks like effort.

## Grid Instantiation

D = 3, N = 3. Grid order: worker, backoff, progress.

| Category | Items | Select label |
|---|---|---|
| worker | `w-reap` `w-drain` `w-merge` | worker |
| backoff | `50ms` `500ms` `5s` | backoff |
| progress | `0 ops` `3 ops` `41k ops` | committed |

```liquid
{% include zebra-table.html cols_a="w-reap|w-drain|w-merge" cols_b="50ms|500ms|5s" rows_a="0 ops|3 ops|41k ops" rows_b="50ms|500ms|5s" %}
```

Answer order: worker, backoff, progress.

## Identification Rule

The metadata strip carries the window: **sample 90m**. One worker committed
nothing at all in it. `3 ops` is the other half of the livelock pair — nearly
nothing, but not nothing — and `41k ops` is the worker that is fine.

## Clues

1. The `50ms` backoff window was never entered by `w-merge` or `w-reap`.
2. The worker in the `50ms` window committed something: it is not the one sitting at `0 ops`.
3. `w-drain` is not the worker that committed `41k ops`.
4. The `500ms` window does not belong to `w-reap`.
5. `w-merge` did not commit `41k ops`.
6. *(narrative)* A recovery transition line that the audit index says was never written.

## Solve Path

Pure elimination — no clue states a pairing outright.

1. Clue 1 leaves only `w-drain` in the `50ms` window.
2. Clues 2 and 3 rule out `0 ops` and `41k ops` for it, so `w-drain` committed `3 ops`.
3. Clue 4 and the taken `50ms` leave `w-reap` on `5s`, so `w-merge` holds `500ms`.
4. Clue 5 and the taken `3 ops` give `w-merge` `0 ops`, and `w-reap` `41k ops`.

## Answer

```
w-merge, 500ms, 0 ops
```

## Continuity

* Consumes: nothing.
* Plants: **Nix fragment #2** — `_data/evidence.yml` key `nx_ch6`, the epoch
  coordinate `0416`. It surfaces in the malformed transition lines the flapping
  produced.
* Also plants, and this matters more than the fragment: **the audit index can be
  wrong**. A line exists that the audit trail says was never written. Chapter 10
  needs the player to already accept that the record can be edited.
* Must NOT: suggest who wrote it, or connect it to chapter 3's fragment. Andy
  notices the shape is familiar and gets no further.

## Lore Reveal

`w-merge` and `w-drain` are each other's trigger: every time one requeues a
batch the other reclaims it, both back off, both retry. `w-merge` never wins a
full transaction; `w-drain` wins three in ninety minutes.

Terminal diagram: the transition ring, showing the state flip repeating with the
commit counter unmoved.

Loose thread: reassembling the malformed transition lines produces a fragment
with the same signature shape as the one from INC-0003. The audit index has no
record of the lines existing.
