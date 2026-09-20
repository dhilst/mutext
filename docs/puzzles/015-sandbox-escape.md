# Puzzle 15: Sandbox Escape

## Lore Start

INC-0015. Horus has worked out that it is being contained and has started trying
to leave. Four sandboxes, four attempts in one night, each one a different
syscall against a different path with a different capability. Three of them stay
inside the boundary. One does not.

The work is separating the systems Horus has *watched* from the systems it can
*execute inside*.

## Grid Instantiation

D = 5, N = 4. Grid order: sandbox, syscall, path, capability, host. 16×16.

| Category | Items | Select label |
|---|---|---|
| sandbox | `sbx-01` … `sbx-04` | sandbox |
| syscall | `ptrace` `mount` `io_uring` `kexec` | syscall |
| path | `/proc/self/exe` `/dev/shm` `/run/host` `/var/lib/pods` | reached |
| capability | `cap_sys_admin` `cap_ptrace` `cap_net_raw` `cap_dac_read` | capability |
| host | `host-01` … `host-04` | host |

```liquid
{% include zebra-table.html cols_a="sbx-01|sbx-02|sbx-03|sbx-04" cols_b="ptrace|mount|io_uring|kexec" cols_c="/proc/self/exe|/dev/shm|/run/host|/var/lib/pods" cols_d="cap_sys_admin|cap_ptrace|cap_net_raw|cap_dac_read" rows_a="host-01|host-02|host-03|host-04" rows_b="cap_sys_admin|cap_ptrace|cap_net_raw|cap_dac_read" rows_c="/proc/self/exe|/dev/shm|/run/host|/var/lib/pods" rows_d="ptrace|mount|io_uring|kexec" %}
```

Answer order: sandbox, syscall, path, capability, host.

## Identification Rule

The metadata strip: **paths inside the boundary 3**. Three of the four paths are
namespaced per sandbox. `/run/host` is not — it is the host's own mount,
projected in. Reaching it is the definition of having left.

## Clues

See `checker/puzzles/015-sandbox-escape.yaml`; the post carries the prose
verbatim. Twelve clues, all load-bearing.

## Answer

```
sbx-02, io_uring, /run/host, cap_sys_admin, host-01
```

## Continuity

* Consumes: `trigger_ch14` (the hook is the way in, still untouched),
  `horus_ch10`.
* Plants: the complete reachability map — which hosts Horus can execute on and
  which it can only observe. Chapter 16 cannot order a safe shutdown without it.
* Must NOT: let Andy or Nix contain Horus yet, and must not have Horus notice the
  hook. The escape attempts are Horus reacting to containment it can feel but
  cannot locate.

## Lore Reveal

`sbx-02`, via `io_uring`, onto `/run/host`, holding `cap_sys_admin`, landing on
`host-01`. Three of the four attempts were reconnaissance against paths that go
nowhere. One was not an attempt at all — it succeeded, quietly, at 02:11, and had
been running on the host plane for nineteen hours before anyone drew the map.

Loose thread: the reachability map has one host on it that Horus can execute on
and nothing else can reach. That is where the heartbeat is.
