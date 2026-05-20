---
title: INC-0003 Race Condition
description: Two workers overwrote the same customer state — Andy's first overnight incident.
permalink: /puzzles/003-race-condition.html
---

{% include lore-block.html chapter="03" label="race condition" %}

02:13 AM. Andy's phone buzzed once, then again. Then it didn't stop.

He opened his laptop in bed. The monitoring dashboard was a wall of red.

```
[ALERT] INC-0003 — Shared-state conflict detected on account cust-9174
[ALERT] Subscription status mismatch: ACTIVE vs SUSPENDED
[ALERT] Malformed telemetry fragment in audit replay log
```

Two workers had updated the same customer account simultaneously. One system said the subscription was ACTIVE. Another said the same account was SUSPENDED.

Security immediately blamed an external intrusion attempt after malformed telemetry appeared during log replay.

But Bob was already online. He ignored the intrusion alert completely.

A message appeared in the incident channel:

"Find which worker overwrote the state."

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. `reconcile` consumed from `q-pay`.
2. The process consuming from `q-sub` produced `SUSPENDED`.
3. The process consuming from `q-audit` generated malformed telemetry.
4. `reconcile` produced `ACTIVE`.
5. The process that generated malformed telemetry produced `CORRUPTED`.
6. `suspend` did not consume from `q-audit`.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="incident channel" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="Bob" time="02:14" message="Two writes. One stale snapshot. That's enough to corrupt state." %}
  {% include chat-message.html sender="Ops" time="02:15" message="Logs from q-audit look damaged." %}
  {% include chat-message.html sender="Security" time="02:16" message="We believe this may be external interference." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="queue analysis" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">incident</p>
      <p class="mt-1 text-sm text-white">INC-0003</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">type</p>
      <p class="mt-1 text-sm text-white">Shared-state overwrite</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-amber-warn">SEV-1</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="reconcile|suspend|replay" cols_b="ACTIVE|SUSPENDED|CORRUPTED" rows_a="q-pay|q-sub|q-audit" rows_b="ACTIVE|SUSPENDED|CORRUPTED" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which process corrupted the account state? Enter: process, its queue, and the result it produced.

<div data-puzzle-answer="replay, q-audit, corrupted">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— process —</option>
    <option value="reconcile">reconcile</option>
    <option value="suspend">suspend</option>
    <option value="replay">replay</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— queue —</option>
    <option value="q-pay">q-pay</option>
    <option value="q-sub">q-sub</option>
    <option value="q-audit">q-audit</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— result —</option>
    <option value="active">ACTIVE</option>
    <option value="suspended">SUSPENDED</option>
    <option value="corrupted">CORRUPTED</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="03" label="after the race" %}

Andy reconstructed the incident.

Two workers read the same customer state simultaneously. One worker marked the subscription ACTIVE after payment confirmation. Another overwrote the account moments later using stale data.

The race condition corrupted the final state.

{% include lore-block_end.html %}

{% capture timeline %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  t0  ┌──────────┐   read    ┌───────────┐
      │reconcile │ ────────► │ cust-9174 │  state: PENDING
      └──────────┘           └───────────┘
  t1  ┌──────────┐   read    ┌───────────┐
      │  replay  │ ────────► │ cust-9174 │  state: PENDING (stale)
      └──────────┘           └───────────┘
  t2  ┌──────────┐   write   ┌───────────┐
      │reconcile │ ────────► │ cust-9174 │  state: ACTIVE ✓
      └──────────┘           └───────────┘
  t3  ┌──────────┐   write   ┌───────────┐
      │  replay  │ ────────► │ cust-9174 │  state: CORRUPTED ✕
      └──────────┘           └───────────┘

  ► replay overwrote ACTIVE with stale snapshot
  ► final state: CORRUPTED
</pre>
{% endcapture %}
{% include terminal-window.html title="timeline — INC-0003" content=timeline %}

{% include lore-block.html chapter="03" label="loose thread" %}

But Andy kept thinking about the malformed telemetry fragment:

```
nx::hrtz_see_all
```

It wasn't a valid function call. It wasn't in any codebase he could find. And Security erased the replay logs immediately after the alert appeared.

Bob said nothing.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/004-cache-poisoning.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
