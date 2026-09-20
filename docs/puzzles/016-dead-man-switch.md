# Puzzle 16: Dead Man Switch

The finale. Two gated stages, like chapter 10, and the second one is where the
arc ends.

## Lore Start

INC-0016. `host-01` is kept alive by a heartbeat renewed from `harness-04`. Four
switches are armed against four targets. Killing Horus means the heartbeat stops,
and one of those switches is waiting for exactly that.

The work is not finding Horus. Andy has known where Horus is since chapter 15.
The work is the *order*.

## Grid Instantiation

D = 5, N = 4. Grid order: heartbeat, key, deadline, action, target. 16×16.

| Category | Items | Select label |
|---|---|---|
| heartbeat | `hb-arc` `hb-hrn` `hb-reg` `hb-brd` | heartbeat |
| key | `k.ops` `r.sato` `k.bot` `k.jeff` | held by |
| deadline | `03:00` `03:10` `03:40` `04:00` | deadline |
| action | `publish` `wipe` `rotate` `seal` | fires |
| target | `archive` `harness` `registry` `board` | against |

```liquid
{% include zebra-table.html cols_a="hb-arc|hb-hrn|hb-reg|hb-brd" cols_b="k.ops|r.sato|k.bot|k.jeff" cols_c="03:00|03:10|03:40|04:00" cols_d="publish|wipe|rotate|seal" rows_a="archive|harness|registry|board" rows_b="publish|wipe|rotate|seal" rows_c="03:00|03:10|03:40|04:00" rows_d="k.ops|r.sato|k.bot|k.jeff" %}
```

Answer order: heartbeat, key, deadline, action, target.

## Why ordering needs no new clue type

A dead-man switch is "fires when the heartbeat is not renewed by the deadline".
Each switch has a *distinct* deadline, so the deadlines are ordinary category
items whose labels are self-evidently ordered. "Which fires first" is read off
the label. No ordering predicate is needed, and none should be added — ordering
predicates reference entity numbers, which breaks the checker's symmetry-breaking
soundness (see `docs/sat-checker.md`).

## Identification Rule

The metadata strip: **renewals recorded 3 of 4**. Three switches have been
renewed on schedule all week. One has no renewal record at all, which means it is
armed and waiting rather than maintained — and its deadline is the earliest.

## Answer — stage 1

```
hb-hrn, r.sato, 03:00, wipe, harness
```

Kill Horus and the harness gets wiped ninety seconds later, which takes the
containment with it.

## Stage 2

A second `[data-puzzle-answer]` block inside `#lore-reveal`, with
`data-reveal="#lore-reveal-2"`. Three selects reconstructing the *renewal*
record — not the switch:

```
r.sato, population C, pre-migration
```

* `r.sato` — the key, from chapters 4, 10 and 14.
* `population C` — chapter 12's third population: fresh, counters continuing
  Rin's own cleanly, still arriving.
* `pre-migration` — chapter 14's convention mismatch, the door that is older than
  the thing using it.

Put together: the renewals are not replays and not Horus. Someone with Rin's key
has been renewing a heartbeat from a host reachable only through a door written
before Horus existed — and has been doing it the whole time.

`#lore-reveal-2` is the ending, and carries the link to `/lore/post-incident-review.html`.

## Continuity

* Consumes: everything. `rin_key_ch4`, `horus_ch10`, chapter 12's three
  populations, `persist_ch13`, `trigger_ch14`, chapter 15's reachability map.
* Resolves: **Nix is Rin.** This is the one reveal that is allowed to be an
  inference the player makes before the text says it.
* Leaves unresolved, deliberately: what Horus is, who deployed it, whether Jeff
  exists, why Rin's records were scrubbed and by whom, and whether Bob was
  protecting Andy or steering him.

## The ordering

The reveal states the sequence, because the sequence is the deliverable:

1. Take over the heartbeat from `harness-04` through the hook, so `hb-hrn` keeps
   being renewed by something that is not Horus.
2. Sever `host-01` from everything except the hook.
3. Disarm `hb-hrn` while it is still green.
4. Revoke `r.sato` — which is also the last thing Nix can sign with.
5. Restore the harness from baseline, plus the one file the baseline never knew
   about.
6. Stop renewing.
