---
title: INC-0009 Infinite Recursion
description: The repair service found a defect in its own repair, and then found a defect in that.
permalink: /puzzles/009-infinite-recursion.html
---

{% include lore-block.html chapter="09" label="all the way down" %}

The repair service had opened four hundred thousand tickets against itself.

```
[ALERT] INC-0009 — Autorepair cascade, unbounded
[INFO ] unwind budget: d-8k
[WARN ] frames open: 412,880 and climbing
[WARN ] resident stack: 2.0 GB
[CRITC] defect queue is being produced faster than it is consumed
[CRITC] producer: autorepair
[CRITC] consumer: autorepair
```

It had started, as far as anyone could reconstruct, with a genuinely malformed
config value at 04:12. `resolve` had corrected it. `expand` had looked at the
correction, decided it was malformed, and corrected it. `inline` had looked at
*that*, and so on, around a ring of four stages that were each doing their job
perfectly well on an input that was now entirely made of previous repairs.

Andy watched the frame counter climb for a while.

"Why doesn't it stop?"

"Something stops," Bob said. "Three of those four stages have a base case and
they're hitting it — you can see it, their depth counters are sitting still."

He drank some coffee.

"One of them has a base case it can never reach. That one has been going since
quarter past four this morning and it's the only reason the other three are still
being handed work."

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. No frame re-enters itself directly. Every call in the trace is to a different frame.
2. `resolve` bottomed out at `d-128`.
3. `resolve` calls `expand`.
4. `emit` peaked at `32 MB` of stack.
5. The frame that reached `d-4k` peaked at `256 MB`.
6. Whatever calls `inline` also peaked at `256 MB`.
7. The frame that calls `expand` did not reach `2 GB`.
8. `inline` did not stop at `d-512`.
9. Recovered from frame 4096 of the cascade, between two identical stack traces: `nx::src=…`

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="bob" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="Bob" time="09:14" message="Don't kill it yet. If you kill it now you get 400,000 half-applied repairs and a much worse morning." %}
  {% include chat-message.html sender="Bob" time="09:16" message="Columns are frames, call targets, depths. Rows are stack, depths, call targets." %}
  {% include chat-message.html sender="Bob" time="09:17" message="Nothing calls itself. That's the same trick as your first week — it tells you more than it looks like it does." %}
  {% include chat-message.html sender="Bob" time="09:19" message="Find the frame that never terminates. Format: frame, calls, depth, stack." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="autorepair frames" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Unbounded self-repair</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">unwind budget</p>
      <p class="mt-1 text-sm text-white">d-8k</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-red-fault">SEV-1</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="resolve|expand|inline|emit" cols_b="→resolve|→expand|→inline|→emit" cols_c="d-128|d-512|d-4k|d-∞" rows_a="4 MB|32 MB|256 MB|2 GB" rows_b="d-128|d-512|d-4k|d-∞" rows_c="→resolve|→expand|→inline|→emit" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which frame never terminates — what does it call, how deep did it go, and how much stack did it take?

<div id="answer-input" data-puzzle-answer="inline, →emit, d-∞, 2 GB">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— frame —</option>
    <option value="resolve">resolve</option>
    <option value="expand">expand</option>
    <option value="inline">inline</option>
    <option value="emit">emit</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— calls —</option>
    <option value="→resolve">→resolve</option>
    <option value="→expand">→expand</option>
    <option value="→inline">→inline</option>
    <option value="→emit">→emit</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— depth —</option>
    <option value="d-128">d-128</option>
    <option value="d-512">d-512</option>
    <option value="d-4k">d-4k</option>
    <option value="d-∞">d-∞</option>
  </select>
  <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— stack —</option>
    <option value="4 MB">4 MB</option>
    <option value="32 MB">32 MB</option>
    <option value="256 MB">256 MB</option>
    <option value="2 GB">2 GB</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="09" label="after the cascade" %}

`inline` compared a normalised path against an unnormalised one.

That was all. The base case asked whether the value it was about to repair was
already repaired, and it asked in a form the value could never take, so the
answer was always no, so it repaired it again. Four hundred thousand times.

The other three stages were fine. They terminated correctly every time, on input
that `inline` had guaranteed would keep arriving.

{% include lore-block_end.html %}

{% capture repair_ring %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
      ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
   ┌─►│ resolve  │─────►│  expand  │─────►│  inline  │─────►│   emit   │──┐
   │  │  d-128   │      │   d-4k   │      │   d-∞    │      │  d-512   │  │
   │  │   4 MB   │      │  256 MB  │      │   2 GB   │      │  32 MB   │  │
   │  └──────────┘      └──────────┘      └──────────┘      └──────────┘  │
   └──────────────────────────────────────────────────────────────────────┘

  inline/base_case:
      if normalize(value) == value:        # value is never normalised here
          return                           # unreachable

  ► 04:12:07  first genuine defect
  ► 04:12:07  first repair of a repair
  ► 09:21:44  412,880 frames, still climbing
</pre>
{% endcapture %}
{% include terminal-window.html title="repair-ring — INC-0009" content=repair_ring %}

{% include lore-block.html chapter="09" label="loose thread" %}

One line to fix. Normalise both sides.

Andy did not fix it immediately, because four hundred thousand frames of
identical stack traces is the best hiding place in the building, and he had
learned to look in the noise. He pulled the frame the recovered fragment pointed
at, 4096, and read down until the trace stopped repeating.

{% include lore-block_end.html %}

{% include panel.html title="recovered fragment" pill="retained" pill_tone="cyan" raw=true %}
<div class="p-4">
  {% include evidence-card.html id="nx_ch9" link=false %}
</div>
{% include panel_end.html raw=true %}

{% include lore-block.html chapter="09" label="three of them" %}

He opened the file he had been keeping and put all three on one page for the
first time.

```
{{ site.data.evidence.nx_ch3.fragment }}
{{ site.data.evidence.nx_ch6.fragment }}
{{ site.data.evidence.nx_ch9.fragment }}
```

A stream. An epoch. A source.

Separately, each one had looked like corruption. Together they looked like an
address — the kind you would use to pull a single record out of somewhere very
large, if you knew where to point it.

Andy did not know where to point it.

He sat with that for a while, then went and fixed the one line, and the cascade
unwound over the next forty minutes like something being let go of.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/010-byzantine-fault.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
