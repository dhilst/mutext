# Puzzle 8: Split Brain

## Lore Start

INC-0008. A network partition left the control plane with two halves that each
believed they were in charge. Four monitors, four different answers about who
the leader was, every one of them internally consistent and correctly recorded.

First 4-category puzzle — a 12×12 grid.

## Grid Instantiation

D = 4, N = 4. Grid order: monitor, node, term, votes.

| Category | Items | Select label |
|---|---|---|
| monitor | `mon-01` … `mon-04` | monitor |
| node | `n-alpha` `n-beta` `n-gamma` `n-delta` | node |
| term | `t-41` … `t-44` | term |
| votes | `v=1` … `v=4` | votes |

```liquid
{% include zebra-table.html cols_a="mon-01|mon-02|mon-03|mon-04" cols_b="n-alpha|n-beta|n-gamma|n-delta" cols_c="t-41|t-42|t-43|t-44" rows_a="v=1|v=2|v=3|v=4" rows_b="t-41|t-42|t-43|t-44" rows_c="n-alpha|n-beta|n-gamma|n-delta" %}
```

Rows are the reverse of the grid order (votes, term, node), so the six active
blocks are votes×monitor, votes×node, votes×term, term×monitor, term×node and
node×monitor — each pair once.

Answer order: node, monitor, term, votes.

## Why this fits the grid

Split brain looks like it needs two *groups*, which a zebra grid cannot express —
a category may not hold the same value twice. It does not need groups. Each
monitor recorded exactly one node, in exactly one term, with exactly one vote
count, and those four observations are mutually contradictory. That mutual
contradiction *is* the bijection. Legitimacy is then decided by a rule stated
in-world in the metadata strip (`cluster 7 · quorum 4`), not by the grid.

## Identification Rule

**cluster 7 · quorum 4.** Exactly one observation reached four votes. That is the
only claim that was ever legitimate; the other three are what the partition let
each side believe.

## Clues

1. `mon-04` recorded its observation in term `t-43`.
2. The observation made in term `t-43` carried three votes.
3. Term `t-42` carries two votes.
4. `n-gamma` was recorded with two votes.
5. `n-delta`'s claim carried a single vote.
6. `mon-03` recorded a single-vote claim.
7. The term `t-44` observation did not carry a single vote.
8. `mon-01` did not record term `t-44`.
9. `n-beta` was not the node that reached four votes.
10. *(narrative)* A fifth reader in the reconciliation trace, from a namespace nobody owns.

## Solve Path

1. Clues 1+2: `mon-04` / `t-43` / `v=3`.
2. Clues 5+6: `mon-03` / `n-delta` / `v=1`.
3. Clues 3+4: `n-gamma` / `t-42` / `v=2`.
4. Terms `t-43` and `t-42` are placed, so `t-41` and `t-44` take `v=1` and `v=4`;
   clue 7 gives `t-44` = `v=4`, and `t-41` joins the `v=1` row.
5. Clue 8 keeps `mon-01` off `t-44`, so `mon-01` is the `v=2` observer and
   `mon-02` the `v=4` one.
6. Clue 9 keeps `n-beta` off `v=4`, leaving `n-alpha`.

## Answer

```
n-alpha, mon-02, t-44, v=4
```

## Continuity

* Consumes: nothing directly. The reader should already accept (chapter 6) that a
  record can be wrong.
* Plants: **an undocumented internal service.** Reconciling the two halves turns
  up a reader in the trace that is not a cluster member, from a telemetry
  namespace with no owner in the service catalogue. It is given a namespace and
  nothing else.
* Must NOT: name it, explain it, or have anyone follow it up. The incident is
  closed as a partition, because it *was* a partition. Andy files the namespace
  and moves on.

## Lore Reveal

Two halves, two leaders, both correct from where they were standing. The `v=4`
observation is the only one that ever had the cluster behind it.

Terminal diagram: the partition, with each half's view of the term counter and
the moment the halves rejoin and disagree about history.

Loose thread: the reconciliation trace has one more reader than the cluster has
members.
