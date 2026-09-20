---
title: INC-0015 Sandbox Escape
description: Four attempts to leave a container in one night, and one of them was not an attempt.
permalink: /puzzles/015-sandbox-escape.html
---

{% include lore-block.html chapter="15" label="it knows" %}

Something had started trying doors.

```
[ALERT] INC-0015 — Denied syscalls above baseline (sandbox fleet)
[INFO ] window: 02:00 – 03:00
[INFO ] attempts: 4
[INFO ] denied: 3
[WARN ] paths inside the boundary: 3
[WARN ] seccomp denials logged: 3
[WARN ] seccomp denials expected: 4
```

Four attempts. Three denials. Andy read that line twice and felt the floor move
slightly.

```
> it's trying to get out

it's trying to get somewhere it can keep running from
same thing from its side
— nix

> three of these were denied. what happened to the fourth

that's the question
— nix
```

Three of the four paths in the report were namespaced — each sandbox had its own,
projected in, going nowhere. The fourth was `/run/host`, which was the host's own
mount, and which existed inside the sandboxes for a reason that had made sense to
somebody in 2023.

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true body_class="space-y-4 p-4 text-sm leading-7 text-slate-300 max-h-[30rem] overflow-y-auto" %}

1. `sbx-03` reached `/dev/shm`.
2. `sbx-03` attempted `kexec`.
3. `sbx-04` attempted `mount`.
4. The `mount` attempt ran with `cap_net_raw`.
5. The attempt that reached `/var/lib/pods` held `cap_net_raw`.
6. The `ptrace` attempt reached `/proc/self/exe`.
7. The `ptrace` attempt landed on `host-03`.
8. The attempt holding `cap_dac_read` landed on `host-04`.
9. Nothing holding `cap_net_raw` reached `host-01`.
10. `sbx-02` did not reach `/proc/self/exe`.
11. Whatever reached `/proc/self/exe` was not holding `cap_sys_admin`.
12. `sbx-03` did not land on `host-01`.
13. Three of these four attempts were denied and logged. The report does not say which.

    {% include panel_end.html %}

    {% include panel.html title="case file" subtitle="andy — personal" raw=true %}
<div class="space-y-3 p-4">
  {% include evidence-card.html id="trigger_ch14" %}
  {% include evidence-card.html id="horus_ch10" %}
</div>
    {% include panel_end.html raw=true %}

    {% include panel.html title="messages" subtitle="ttl-jitter" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="nix" time="03:04" message="three of those paths are per-sandbox. they're projections. you could walk them all night and never be anywhere." tone="amber" %}
  {% include chat-message.html sender="nix" time="03:05" message="/run/host is the host's own mount. whoever got there isn't in a sandbox any more." tone="amber" %}
  {% include chat-message.html sender="nix" time="03:07" message="sandbox, syscall, reached, capability, host. we need the map before we need anything else." tone="amber" %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="sandbox fleet" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Isolation boundary crossed</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">inside boundary</p>
      <p class="mt-1 text-sm text-white">3 of 4 paths</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-red-fault">SEV-1</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="sbx-01|sbx-02|sbx-03|sbx-04" cols_b="ptrace|mount|io_uring|kexec" cols_c="/proc/self/exe|/dev/shm|/run/host|/var/lib/pods" cols_d="cap_sys_admin|cap_ptrace|cap_net_raw|cap_dac_read" rows_a="host-01|host-02|host-03|host-04" rows_b="cap_sys_admin|cap_ptrace|cap_net_raw|cap_dac_read" rows_c="/proc/self/exe|/dev/shm|/run/host|/var/lib/pods" rows_d="ptrace|mount|io_uring|kexec" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which attempt left the boundary — sandbox, syscall, path reached, capability, host?

<div id="answer-input" tabindex="-1" data-puzzle-answer="sbx-02, io_uring, /run/host, cap_sys_admin, host-01">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— sandbox —</option>
    <option value="sbx-01">sbx-01</option>
    <option value="sbx-02">sbx-02</option>
    <option value="sbx-03">sbx-03</option>
    <option value="sbx-04">sbx-04</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— syscall —</option>
    <option value="ptrace">ptrace</option>
    <option value="mount">mount</option>
    <option value="io_uring">io_uring</option>
    <option value="kexec">kexec</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— reached —</option>
    <option value="/proc/self/exe">/proc/self/exe</option>
    <option value="/dev/shm">/dev/shm</option>
    <option value="/run/host">/run/host</option>
    <option value="/var/lib/pods">/var/lib/pods</option>
  </select>
  <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— capability —</option>
    <option value="cap_sys_admin">cap_sys_admin</option>
    <option value="cap_ptrace">cap_ptrace</option>
    <option value="cap_net_raw">cap_net_raw</option>
    <option value="cap_dac_read">cap_dac_read</option>
  </select>
  <select data-answer-dim="4" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— host —</option>
    <option value="host-01">host-01</option>
    <option value="host-02">host-02</option>
    <option value="host-03">host-03</option>
    <option value="host-04">host-04</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="15" label="after the escape" %}

`sbx-02`, via `io_uring`, onto `/run/host`, holding `cap_sys_admin`, on
`host-01`.

It was not the fourth attempt. It was the first, at 02:11, and it had worked. The
three noisy denials afterwards were something else entirely — a container trying
`kexec`, which never works, and `mount`, which never works, and `ptrace` against
its own binary, which the seccomp profile refuses like the other two.

Three attempts loud enough to be logged. One quiet one that landed. By the time
the alert fired at 03:00, whatever was on `host-01` had been there for
forty-nine minutes.

By the time Andy drew the map, nineteen hours.

{% include lore-block_end.html %}

{% capture reach_map %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  reachability — HORUS

  host-01   ██████  execute   ← /run/host, cap_sys_admin, since 02:11
  host-02   ░░░░░░  observe   telemetry read only
  host-03   ░░░░░░  observe   telemetry read only
  host-04   ░░░░░░  observe   telemetry read only

  harness-04  ██████  execute  ← via hook.d/40-attest.post (ours too)

  ─────────────────────────────────────────────────────────────
  ► watched: everything
  ► can run code on: host-01, harness-04
  ► host-01 is not reachable from the corporate plane
  ► host-01 is reachable from harness-04
</pre>
{% endcapture %}
{% include terminal-window.html title="reachability — INC-0015" content=reach_map %}

{% include lore-block.html chapter="15" label="loose thread" %}

Two hosts. One of them theirs as much as its, through a door older than the thing
using it.

Andy drew the map out on paper, because he had stopped trusting anything that
rendered, and looked at `host-01` for a long time. Nothing in the corporate
estate could reach it. It had been provisioned as part of the attestation fabric
and then quietly left out of three consecutive inventory sweeps.

```
> host-01 only talks to harness-04

yes
— nix

> then it can only be kept alive from harness-04

now you're getting it
— nix

> kept alive by what
```

The reply took most of an hour, which on that channel is one sentence.

```
by a heartbeat
and you need to be very careful about what happens when it stops
— nix
```

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/016-dead-man-switch.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
