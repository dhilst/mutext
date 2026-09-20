# Puzzle 11: Man in the Middle

The deliberate reset. Back to three categories after chapter 10's 20×20, because
the story has just turned over and the player should be spending their attention
on that.

## Lore Start

INC-0011. Andy tries to reach Nix directly. What he sends and what arrives are
not the same thing, and the difference is polite enough that both ends believe
they are talking to each other.

## Grid Instantiation

D = 3, N = 4. Grid order: session, fingerprint, hop.

| Category | Items | Select label |
|---|---|---|
| session | `sx-01` … `sx-04` | session |
| fingerprint | `fp-3a` `fp-7c` `fp-b1` `fp-e9` | presented |
| hop | `hop-ams` `hop-fra` `hop-sfo` `hop-nrt` | exit hop |

```liquid
{% include zebra-table.html cols_a="sx-01|sx-02|sx-03|sx-04" cols_b="fp-3a|fp-7c|fp-b1|fp-e9" rows_a="hop-ams|hop-fra|hop-sfo|hop-nrt" rows_b="fp-3a|fp-7c|fp-b1|fp-e9" %}
```

Answer order: session, fingerprint, hop.

## Identification Rule

The metadata strip carries the pin set: **pinned fingerprints 3**. The registry
holds `fp-3a`, `fp-7c` and `fp-e9`. The fourth fingerprint in the grid is not
pinned to anything, which makes the session that was shown it the intercepted one.

## Clues

1. `sx-01` terminated at `hop-fra`.
2. `sx-01` was presented `fp-7c`.
3. `sx-04` was presented `fp-3a`.
4. The session shown `fp-e9` exited through `hop-ams`.
5. `fp-3a` was not presented on the `hop-nrt` path.
6. `sx-03` did not exit through `hop-nrt`.
7. *(narrative)* Two transcripts of the same exchange that do not match.

## Answer

```
sx-02, fp-b1, hop-nrt
```

## Continuity

* Consumes: `horus_ch10` — Andy knows the name and what it does.
* Plants: a channel whose integrity both ends can check. Chapters 12 and 13 need
  Andy and Nix to have *some* way of agreeing on what was said, without that way
  being a secret Horus cannot see.
* Plants: Nix is now an active correspondent rather than a voice in a log. Andy
  still has no idea who Nix is, and the chapter must not narrow the field.
* Must NOT: let Nix say anything that only Rin would know; let Andy conclude the
  interceptor is Horus by assertion rather than by the fingerprint evidence.

## Lore Reveal

`sx-02` was presented `fp-b1` — a fingerprint pinned to nothing — on the
`hop-nrt` path. Both ends of that session believed they had a direct line. The
interception is verifiable without knowing who did it: the pin registry says the
key is not one of theirs.

Fix, such as it is: stop trusting transport. Andy and Nix start exchanging a
digest of the conversation so far, so that the next altered message is the last
one that goes unnoticed.
