---
title: INC-0002 The Lockup
description: Andy's first real incident — three processes deadlocked in a dependency cycle.
permalink: /puzzles/002-the-lockup.html
---

{% include lore-block.html chapter="02" label="the first morning" %}

Andy arrived on Monday at 8:47. Fourth floor, last desk on the left, next to the vending machine that dispensed only error codes.

He sat down. The chair squeaked. The monitor was already on.

Before he could type his password, the terminal flashed red.

```
[ALERT] INC-0002 — Process freeze detected, P1 unresponsive for 5min
[ALERT] Three processes unresponsive since 09:17:33
[ALERT] Lock contention cycle suspected
```

Bob materialized behind him. Andy had not heard him approach.

"Don't log in yet." Bob set his coffee on the desk. "Your first ticket just came in."

He leaned over Andy's shoulder and pointed at the screen.

"Three processes. Each one grabbed a lock and then tried to call another process. Now they're all waiting. Nothing moves."

Andy stared at the alert. "A deadlock?"

"A perfect one. Three processes, three locks, one cycle. Figure out which process completes the loop — that's the one we kill to break the freeze."

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. No process calls itself.
2. The process holding L1 calls P3.
3. P2 does not hold L3.
4. P3 does not call P1.
5. The process calling P1 holds L2.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="bob" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="Bob" time="09:18" message="Three processes froze. Each one grabbed a lock and then tried to call another process. Now they're all waiting on each other. Classic circular wait." %}
  {% include chat-message.html sender="Bob" time="09:19" message="P1 was the last process called before the hang. Whatever called P1 is the one we kill to break the cycle." %}
  {% include chat-message.html sender="Bob" time="09:20" message="Left columns are processes. Right columns are call targets. Top rows are locks, bottom rows are call targets. The blacked-out corner is where call targets cross themselves — ignore it. Each process holds one lock and calls one other process." %}
  {% include chat-message.html sender="Bob" time="09:21" message="Find the process that called P1. Enter it as: process, lock, called process." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="lock analysis" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Process deadlock — circular lock dependency</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">scenario</p>
      <p class="mt-1 text-sm text-white">prod / first incident</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">freeze time</p>
      <p class="mt-1 text-sm text-amber-warn">09:17:33</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="P1|P2|P3" cols_b="→P1|→P2|→P3" rows_a="L1|L2|L3" rows_b="→P1|→P2|→P3" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which process closes the deadlock cycle? Enter: process, its lock, and the process it calls.

<div data-puzzle-answer="P2, L2, →P1">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— process —</option>
    <option value="P1">P1</option>
    <option value="P2">P2</option>
    <option value="P3">P3</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— lock —</option>
    <option value="L1">L1</option>
    <option value="L2">L2</option>
    <option value="L3">L3</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— calls —</option>
    <option value="→P1">→P1</option>
    <option value="→P2">→P2</option>
    <option value="→P3">→P3</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="02" label="after the lockup" %}

Bob looked at the screen and nodded slowly.

"P2. Holding L2, calling P1. P1 holds L1, waiting on P3. P3 holds L3, calling P2. And P2 is waiting on P1. Round and round."

He took a sip of coffee.

"In production we'd kill P2 and let the others untangle. Here we just log it and move on."

{% include lore-block_end.html %}

{% capture dep_graph %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  ┌────┐  calls   ┌────┐  calls   ┌────┐
  │ P1 │ ───────► │ P3 │ ───────► │ P2 │
  └────┘          └────┘          └────┘
    ▲                                │
    │              calls             │
    └────────────────────────────────┘

  P1 holds L1  ─  calls P3 (needs L3, held by P3)
  P3 holds L3  ─  calls P2 (needs L2, held by P2)
  P2 holds L2  ─  calls P1 (needs L1, held by P1)

  ► Cycle: P1 → P3 → P2 → P1
  ► Kill target: P2 (closes the cycle)
</pre>
{% endcapture %}
{% include terminal-window.html title="dependency-graph — INC-0002" content=dep_graph %}

{% include lore-block.html chapter="02" label="loose thread" %}

Andy leaned back. His first incident, solved before lunch.

But something nagged at him. He looked at the dependency graph again.

Three processes. Three locks. Each one holding exactly what the next one needs. The cycle was perfect — clean, circular, almost elegant.

Bob was already walking away.

"Bob?" Andy called. "The lock assignment. It's too clean. The scheduler shouldn't produce a pattern like this randomly."

Bob stopped. He didn't turn around.

"No," he said quietly. "It shouldn't."

He kept walking.

{% include lore-block_end.html %}
</section>
