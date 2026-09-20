---
title: INC-0005 Starvation
description: A retry consumer that never crashes, never blocks, and never runs.
permalink: /puzzles/005-starvation.html
---

{% include lore-block.html chapter="05" label="dead letter" %}

The ticket had been open for nineteen hours before anyone opened it.

```
[ALERT] INC-0005 — Dead-letter depth above threshold (retry fabric)
[WARN ] q-dead: 41,207 messages, oldest 19h04m
[WARN ] All consumers report healthy
[WARN ] No consumer has been restarted in 6 days
[INFO ] SLA: acknowledgement budget 30m
```

Andy read it twice. Nothing had crashed. Nothing was blocked. Every consumer was
answering its health probe on time and reporting itself ready for work.

One of them had not done any.

Bob appeared with a second coffee he did not offer.

"Three consumers, three lanes. One of them is starving."

"Starving."

"It's eligible every round. It just never wins." Bob tapped the depth graph, which
had been climbing in a perfectly straight line since Tuesday. "Nothing is broken.
That's the part people can't hold in their heads. Something has to be more
urgent, forever, and it is."

Andy pulled the scheduler's acknowledgement table. Two of the three numbers were
inside the budget. The third was not close.

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. The consumer whose last acknowledgement was `14s` is the one attached to `q-dead`.
2. `notify` did not record the `19h` acknowledgement.
3. No consumer on `q-hot` has been silent for `19h`.
4. `ingest` consumes from `q-dead`.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="bob" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="Bob" time="14:06" message="Don't restart anything. A restart makes the graph look better and tells you nothing." %}
  {% include chat-message.html sender="Bob" time="14:07" message="The budget is 30 minutes. Exactly one acknowledgement in that table is outside it. Start there and work outward." %}
  {% include chat-message.html sender="Bob" time="14:09" message="Left columns are consumers and acknowledgements. Rows are lanes and acknowledgements. Each consumer holds one lane and one acknowledgement." %}
  {% include chat-message.html sender="Bob" time="14:11" message="Tell me which consumer starved, which lane it is stuck behind, and when it last got a word in. Format: consumer, lane, last ack." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="retry fabric" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Consumer never scheduled</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">ack budget</p>
      <p class="mt-1 text-sm text-white">30m</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-amber-warn">SEV-3</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="ingest|settle|notify" cols_b="14s|9m|19h" rows_a="q-hot|q-warm|q-dead" rows_b="14s|9m|19h" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which consumer starved, on which lane, and when did it last acknowledge?

<div data-puzzle-answer="settle, q-warm, 19h">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— consumer —</option>
    <option value="ingest">ingest</option>
    <option value="settle">settle</option>
    <option value="notify">notify</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— lane —</option>
    <option value="q-hot">q-hot</option>
    <option value="q-warm">q-warm</option>
    <option value="q-dead">q-dead</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— last ack —</option>
    <option value="14s">14s</option>
    <option value="9m">9m</option>
    <option value="19h">19h</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="05" label="after the starvation" %}

`settle` had been ready for nineteen hours.

Every scheduling round it declared itself eligible. Every scheduling round the
incident traffic on `q-hot` arrived first, took the worker, and released it a
moment before `settle` was polled again. Its own backlog aged past the retry
ceiling and fell through into `q-dead`, where `ingest` dutifully filed it.

Nothing failed. The system did exactly what it was told to do, continuously, for
most of a day.

{% include lore-block_end.html %}

{% capture scheduler_round %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  round   eligible                     granted     reason
  ─────────────────────────────────────────────────────────────
  4471    settle, notify               notify      q-hot first
  4472    settle, notify               notify      q-hot first
  4473    settle, ingest, notify       notify      q-hot first
  4474    settle, notify               notify      q-hot first
   ...    (11,904 rounds omitted)
  16378   settle, notify               notify      q-hot first
  ─────────────────────────────────────────────────────────────
  ► settle eligible in 16,378 of 16,378 rounds
  ► settle granted in 0
  ► no error raised: starvation is not a failure state
</pre>
{% endcapture %}
{% include terminal-window.html title="sched-trace — retry fabric" content=scheduler_round %}

{% include lore-block.html chapter="05" label="loose thread" %}

Andy wrote up the incident, marked it resolved, and then did the thing he always
did, which was keep reading after the answer.

He pulled the maintenance calendar for the last three weeks.

```
scheduled maintenance windows   21
windows completed                0
windows interrupted by incident 21
```

Twenty-one for twenty-one. He looked at it for a while and decided it was the
least surprising number he had seen all week. Of course they were interrupted.
Nobody on this team had finished anything in a month.

He closed the calendar.

Bob, already leaving: "Congratulations. You've found the part of the job nobody
writes a runbook for."

"Which part?"

"The part where nothing is wrong."

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/006-livelock.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
