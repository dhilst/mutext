# Puzzle 14: Backdoor

## Lore Start

INC-0014. Chapter 13 gave up a path: `harness-04:/hook.d/40-attest.post`, a hook
that runs after the harness has finished validating itself. This chapter is the
examination of how it got there. Four commits touched the harness repo's module
paths in one night; one of them added a route that no configuration restore would
ever remove.

## Grid Instantiation

D = 5, N = 4. Grid order: commit, key, module, window, trigger. 16×16, 160 cells.

| Category | Items | Select label |
|---|---|---|
| commit | `c-4a1` `c-9f2` `c-2de` `c-77b` | commit |
| key | `k.ops` `r.sato` `k.bot` `k.rel` | signed |
| module | `auth` `ingest` `harness` `export` | module |
| window | `02:40` `03:15` `04:35` `05:10` | window |
| trigger | `x-mu-trace` `x-mu-replay` `x-mu-debug` `x-mu-drain` | answers |

```liquid
{% include zebra-table.html cols_a="c-4a1|c-9f2|c-2de|c-77b" cols_b="k.ops|r.sato|k.bot|k.rel" cols_c="auth|ingest|harness|export" cols_d="02:40|03:15|04:35|05:10" rows_a="x-mu-trace|x-mu-replay|x-mu-debug|x-mu-drain" rows_b="02:40|03:15|04:35|05:10" rows_c="auth|ingest|harness|export" rows_d="k.ops|r.sato|k.bot|k.rel" %}
```

Answer order: commit, key, module, window, trigger.

## Identification Rule

The metadata strip: **self-check covers hooks 00–30**. The hook from chapter 13
is `40-`, which puts it in the `harness` module and above the line the harness
checks. So the culprit row is the commit that touched `harness`; everything else
about it — who signed it, when it landed, what it answers to — is deduced.

## Clues

1. `c-4a1` touches `auth`.
2. `c-9f2` touches `export`.
3. `c-9f2` answers `x-mu-drain`.
4. Whatever `k.rel` signed answers `x-mu-drain`.
5. Whatever `k.ops` signed answers `x-mu-debug`.
6. The change that landed in the `03:15` window answers `x-mu-debug`.
7. The change that landed in the `04:35` window answers `x-mu-trace`.
8. The path added to `ingest` answers `x-mu-trace`.
9. The path added to `auth` does not answer `x-mu-replay`.
10. `c-77b` is not signed `r.sato`.
11. `c-2de` landed early: not in the `04:35` window, and not in the `05:10` one.
12. *(narrative)* The hook's coding conventions.

## Answer

```
c-2de, r.sato, harness, 02:40, x-mu-replay
```

## Continuity

* Consumes: `persist_ch13` (the hook path), `rin_key_ch4`, chapter 12's three
  populations.
* Plants, for chapter 16: **the hook is older than Horus.** It uses the harness's
  pre-migration conventions — the ones that were replaced two years ago and that
  none of Horus's own patches use. Whoever wrote it knew this system before the
  thing that is now using it existed.
* Plants: they leave it in place. Chapter 16 needs an unmonitored way in.
* Must NOT: let anyone say Rin wrote it. Andy observes the convention mismatch
  and files it with the other things he cannot explain.

## Lore Reveal

`c-2de`, signed `r.sato`, in the `harness` module, landed at `02:40` — the first
diversion window on chapter 10's schedule — answering the header `x-mu-replay`.

Send that header to any harness endpoint and the hook hands back a shell inside
the validation boundary. No credential. No log line, because the logger is
configured in `20-log` and the hook runs at `40`.

Terminal diagram: the hook ordering, showing `30-verify` declaring the harness
sound and `40-attest.post` running afterwards.

Loose thread: the code in the hook uses `mu_ctx_t` and the old error convention.
The harness stopped using both in the migration two years ago.
