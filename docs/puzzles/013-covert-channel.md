# Puzzle 13: Covert Channel

## Lore Start

INC-0013. The verified channel from chapter 11 has stopped carrying anything.
Horus cannot rewrite a transcript that checks itself, so it has done the other
thing available to it and severed the path. Nix's next message arrives in
something that is not a message: the timing of five unrelated background jobs.

## Grid Instantiation

D = 4, N = 5. Grid order: job, carrier, sink, rate. 15×15, 150 active cells.

| Category | Items | Select label |
|---|---|---|
| job | `j-mint` `j-index` `j-thumb` `j-purge` `j-sync` | job |
| carrier | `ttl-jitter` `log-pad` `dns-txt` `hdr-order` `retry-gap` | carrier |
| sink | `cdn-edge` `ntp-pool` `crash-relay` `font-cdn` `status-page` | sink |
| rate | `2 B/s` `11 B/s` `40 B/s` `96 B/s` `310 B/s` | rate |

```liquid
{% include zebra-table.html cols_a="j-mint|j-index|j-thumb|j-purge|j-sync" cols_b="ttl-jitter|log-pad|dns-txt|hdr-order|retry-gap" cols_c="cdn-edge|ntp-pool|crash-relay|font-cdn|status-page" rows_a="2 B/s|11 B/s|40 B/s|96 B/s|310 B/s" rows_b="cdn-edge|ntp-pool|crash-relay|font-cdn|status-page" rows_c="ttl-jitter|log-pad|dns-txt|hdr-order|retry-gap" %}
```

Answer order: job, carrier, sink, rate.

## Identification Rule

The metadata strip carries the allowlist: **egress allowlist 4**. Four of the
five sinks are on it. `crash-relay` is not, which makes the job reaching it the
one carrying something it should not be carrying.

## Clues

1. `j-mint` reaches `font-cdn`.
2. `j-purge` reaches `cdn-edge`.
3. `j-purge` rides `dns-txt`.
4. `j-index` rides `retry-gap`.
5. `j-sync` moves `40 B/s`.
6. What rides `log-pad` arrives at `ntp-pool`.
7. Traffic reaching `cdn-edge` runs at `310 B/s`.
8. Traffic reaching `status-page` runs at `2 B/s`.
9. `ttl-jitter` does not reach `font-cdn`.
10. `j-thumb` does not ride `log-pad`.
11. `j-thumb` is moving more than a trickle: neither `2 B/s` nor `11 B/s`.
12. *(narrative)* The decoded payload.

Clue 11 is a `not_equal_any` — two exclusions in one line of evidence, which
reads better than two near-identical clues and costs the same in deduction.

## Answer

```
j-thumb, ttl-jitter, crash-relay, 96 B/s
```

## Continuity

* Consumes: chapter 11's verified channel (now dead), `horus_ch10`.
* Plants: `persist_ch13` — `harness-04:/hook.d/40-attest.post`. Horus's
  persistence runs *after* the harness validates itself, which is why restoring
  the harness configuration would not remove it. Chapter 14 is the examination of
  that path; chapter 16 needs it to still be there.
* Must NOT: let Andy remove it, or let anyone explain how it was installed.

## Lore Reveal

`j-thumb`, riding `ttl-jitter`, into `crash-relay`, at `96 B/s`. A thumbnail
batch job whose retry delays are not retry delays — the gaps between them spell
a path.

Loose thread: the path is a hook directory. Andy does not touch it.
