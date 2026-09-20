# Puzzle 12: Replay

## Lore Start

INC-0012. Four authorisation requests, all correctly signed, all accepted. One of
them was signed ten minutes earlier for a different purpose and sent again.
Authenticity does not separate them; freshness does.

## Grid Instantiation

D = 4, N = 4. Grid order: request, nonce, accepted, age.

| Category | Items | Select label |
|---|---|---|
| request | `rq-01` … `rq-04` | request |
| nonce | `nc-11` … `nc-14` | nonce |
| accepted | `08:02` `08:05` `08:09` `08:14` | accepted |
| age | `0.4s` `1.1s` `2.0s` `611s` | age on arrival |

```liquid
{% include zebra-table.html cols_a="rq-01|rq-02|rq-03|rq-04" cols_b="nc-11|nc-12|nc-13|nc-14" cols_c="08:02|08:05|08:09|08:14" rows_a="0.4s|1.1s|2.0s|611s" rows_b="08:02|08:05|08:09|08:14" rows_c="nc-11|nc-12|nc-13|nc-14" %}
```

Answer order: request, nonce, accepted, age.

**Quote the times in the YAML.** Bare `08:05` is parsed as an integer by PyYAML
and the item lookup then fails silently; the loader now rejects non-string items
(`E101`) rather than letting that through.

## Why this fits the grid

Nonce *reuse* cannot be modelled — a category may not hold the same value twice.
It does not need to be. Two time-like categories do the work: when the request
was accepted, and how old it already was when it arrived. Exactly one request is
outside the skew budget, and that is a checkable, faithful statement of what a
replay is.

## Identification Rule

The metadata strip: **max skew 5s**. Three requests arrive inside it. One arrives
`611s` old and is accepted anyway, because the signature is perfectly good — it
was perfectly good ten minutes ago too.

## Clues

1. `rq-01` was accepted at `08:05`.
2. `rq-01` carried nonce `nc-13`.
3. `rq-02` was accepted at `08:14`.
4. `rq-02` was `0.4s` old when it was accepted.
5. The request carrying `nc-11` was `0.4s` old on arrival.
6. The request carrying `nc-12` was `2.0s` old on arrival.
7. The request carrying `nc-13` was `1.1s` old on arrival.
8. `rq-03` was not `2.0s` old when it was accepted.
9. `rq-03` was not the request accepted at `08:09`.
10. *(narrative)* The counter split of Rin's history.

## Answer

```
rq-03, nc-14, 08:02, 611s
```

## Continuity

* Consumes: chapter 7's "a signature proves possession of a key, not the presence
  of a person", and `rin_key_ch4`.
* Plants, for chapter 16: applying the freshness test to everything `r.sato` has
  ever signed splits that history into **three** parts, not two — Rin's original
  work, Horus's replays of it, and a small residue that is neither: fresh,
  correctly countered, still arriving.
* Andy notices the residue and explicitly does not draw a conclusion. Nix changes
  the subject. Neither of those may read as a confirmation.
* Must NOT: let Andy or Nix say the residue is a person, or connect it to Nix.

## Lore Reveal

`rq-03`: nonce `nc-14`, accepted at `08:02`, `611s` old. A revocation approval
signed at 07:51 for a key rotation that was cancelled, re-sent at 08:02 against a
different resource, and accepted because everything about it verified.

Terminal diagram: the four requests on a timeline with the skew window drawn, and
`rq-03` sitting far outside it.

Loose thread: the same test, run across `r.sato`'s entire signing history. Three
populations. Andy stops writing.
