---
title: INC-0008 Split Brain
description: A partition left two halves of the control plane each certain they were in charge.
permalink: /puzzles/008-split-brain.html
---

{% include lore-block.html chapter="08" label="both of them" %}

The partition lasted forty seconds. The argument lasted the rest of the day.

```
[ALERT] INC-0008 — Control plane partition, 40s
[ALERT] Two nodes accepted writes as primary
[CRITC] Divergent term history after rejoin
[INFO ] cluster size 7 · quorum 4
[INFO ] monitors reporting: 4/4
[WARN ] monitors agreeing: 0/4
```

Four monitors. Four different leaders. None of them wrong, exactly — each one
had watched an election, counted the votes it could see, and written down the
winner. Then the link came back and all four records landed in the same trace.

"Everyone's telling the truth," Andy said.

"Everyone always is." Bob had his headphones around his neck, which meant he had
been listening to the incident channel for a while before saying anything. "A
partition doesn't make anybody lie. It makes them all correct about a smaller
world."

He pointed at the header.

"Seven nodes, quorum of four. So out of those four claims, exactly one ever had
the cluster behind it. The rest are three people winning elections in rooms with
nobody in them."

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. `mon-04` recorded its observation in term `t-43`.
2. The observation made in term `t-43` carried three votes.
3. Term `t-42` carries two votes.
4. `n-gamma` was recorded with two votes.
5. `n-delta`'s claim carried a single vote.
6. `mon-03` recorded a single-vote claim.
7. The term `t-44` observation did not carry a single vote.
8. `mon-01` did not record term `t-44`.
9. `n-beta` was not the node that reached four votes.
10. The rejoin trace lists five readers. The cluster has four monitors.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="incident channel" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="Ops" time="09:52" message="Both primaries accepted writes. We are going to be reconciling ledgers until Thursday." tone="amber" %}
  {% include chat-message.html sender="Security" time="09:55" message="Treating as possible intrusion until proven otherwise." tone="red" %}
  {% include chat-message.html sender="Bob" time="09:58" message="It's a partition. Forty seconds of nobody being able to hear each other. Security can have it back when they find a packet that didn't belong." %}
  {% include chat-message.html sender="Bob" time="10:02" message="Four categories now. Columns are monitors, nodes, terms. Rows are votes, terms, nodes. One node, one term and one vote count per monitor." %}
  {% include chat-message.html sender="Bob" time="10:03" message="Find the claim that actually made quorum. Format: node, monitor, term, votes." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="election records" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Two primaries after partition</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">cluster</p>
      <p class="mt-1 text-sm text-white">7 nodes &middot; quorum 4</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-red-fault">SEV-1</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="mon-01|mon-02|mon-03|mon-04" cols_b="n-alpha|n-beta|n-gamma|n-delta" cols_c="t-41|t-42|t-43|t-44" rows_a="v=1|v=2|v=3|v=4" rows_b="t-41|t-42|t-43|t-44" rows_c="n-alpha|n-beta|n-gamma|n-delta" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which node actually held the lease — recorded by which monitor, in which term, with how many votes?

<div data-puzzle-answer="n-alpha, mon-02, t-44, v=4">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— node —</option>
    <option value="n-alpha">n-alpha</option>
    <option value="n-beta">n-beta</option>
    <option value="n-gamma">n-gamma</option>
    <option value="n-delta">n-delta</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— monitor —</option>
    <option value="mon-01">mon-01</option>
    <option value="mon-02">mon-02</option>
    <option value="mon-03">mon-03</option>
    <option value="mon-04">mon-04</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— term —</option>
    <option value="t-41">t-41</option>
    <option value="t-42">t-42</option>
    <option value="t-43">t-43</option>
    <option value="t-44">t-44</option>
  </select>
  <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— votes —</option>
    <option value="v=1">v=1</option>
    <option value="v=2">v=2</option>
    <option value="v=3">v=3</option>
    <option value="v=4">v=4</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="08" label="after the partition" %}

`n-alpha`, recorded by `mon-02`, in term `t-44`, with four votes.

Four out of seven. The only claim in the trace that a majority of the cluster
ever agreed to. The other three nodes each won an election inside a fragment of
the cluster that could not hear the rest of it, and each of those fragments went
on serving writes with complete confidence for forty seconds.

Reconciling ran into the following week. Two ledgers, one truth, and a lot of
customers who had been told different things about their own money.

{% include lore-block_end.html %}

{% capture partition_view %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
                      ── link down 09:51:04 ──

  side A (4 nodes)                     side B (3 nodes)
  ┌───────────────────────┐            ┌───────────────────────┐
  │ n-alpha  term t-44    │            │ n-beta   term t-43    │
  │ votes 4/7   QUORUM ✓  │            │ votes 3/7   no quorum │
  │ accepting writes      │            │ accepting writes      │
  └───────────────────────┘            └───────────────────────┘
       n-gamma  t-42  2/7                   n-delta  t-41  1/7

                      ── link up   09:51:44 ──

  ► both sides present a term history
  ► term counters overlap, contents differ
  ► only t-44 was ever ratified
</pre>
{% endcapture %}
{% include terminal-window.html title="rejoin-trace — INC-0008" content=partition_view %}

{% include lore-block.html chapter="08" label="loose thread" %}

Andy wrote the reconciliation script, ran it, watched it work, and then went back
to the rejoin trace because of the thing that had been bothering him since ten in
the morning.

The cluster had four monitors. The trace had five readers.

```
readers on rejoin:
  mon-01       cluster/monitor
  mon-02       cluster/monitor
  mon-03       cluster/monitor
  mon-04       cluster/monitor
  {{ site.data.evidence.obs_ch8.fragment }}
```

He looked up `tel/hrs-07` in the service catalogue. The catalogue had no entry.
He asked in the platform channel. Someone said it was probably a legacy exporter.
Someone else said everything was probably a legacy exporter.

The fifth reader had not written anything. It had only watched, from before the
link went down until after it came back, which was more than any of the actual
monitors had managed.

Andy wrote the namespace down on the same page as the other two things he had
written down and did not understand.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/009-infinite-recursion.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
