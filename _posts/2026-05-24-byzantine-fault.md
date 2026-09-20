---
title: INC-0010 Byzantine Fault
description: Five attestation replicas, five different histories, every one of them correctly signed.
permalink: /puzzles/010-byzantine-fault.html
---

{% include lore-block.html chapter="10" label="five truths" %}

Nothing was corrupted. That was what took Andy the longest to accept.

```
[ALERT] INC-0010 — Attestation quorum failed, 5 divergent reports
[INFO ] all reports well-formed
[INFO ] all signatures verify
[INFO ] all epochs within window
[WARN ] agreement: 0/5
[WARN ] no replica has reported a fault
```

Five replicas attest to the same ledger. Once per epoch each one publishes a
digest of what it believes the world looks like, countersigns it, and pushes it
into its telemetry stream. They are supposed to be boring and identical.

This morning they were five different histories, each one signed, each one
plausible, none of them agreeing about anything.

Bob looked at it for a long time before he said anything, which had not happened
before.

"This isn't a crash. A crash is a system that stopped telling you things." He
tapped the report count. "This is a system that is still telling you things."

"One of them is lying."

"One of them is *reporting*," Bob said. "Nothing in that list is malformed. A
liar who malforms things is a bug. A liar who signs correctly is a participant."

He pulled up the key registry and let Andy find it himself.

Five countersigning keys. Four of them were service identities.

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true body_class="space-y-4 p-4 text-sm leading-7 text-slate-300 max-h-[34rem] overflow-y-auto" %}

1. `r1` countersigns with `k1`.
2. `r1` attested in epoch `e5`.
3. `r1` produced digest `d2`.
4. The `k1` attestation goes out on `s3`.
5. `r5` publishes into `s2`.
6. Whatever is countersigned `k3` publishes into `s2`.
7. Epoch `e3` is countersigned `k3`.
8. Digest `d4` is countersigned `k5`.
9. The attestation countersigned `k2` went out on `s5`.
10. Digest `d5` was not produced in epoch `e3`.
11. Nothing on `s5` carries the epoch `e4` mark.
12. The `e4` attestation is not countersigned `k5`.
13. `r2` did not attest in epoch `e4`.
14. `r4` does not countersign with `k4`.
15. The `e2` attestation did not go out on `s1`.
16. `r3` does not publish into `s1`.
17. `r4` does not publish into `s1`.
18. `r5` did not produce digest `d1`.
19. Digest `d1` did not appear on `s4`.

    {% include panel_end.html %}

    {% include panel.html title="case file" subtitle="andy — personal" raw=true %}
<div class="space-y-3 p-4">
  {% include evidence-card.html id="nx_ch3" %}
  {% include evidence-card.html id="nx_ch6" %}
  {% include evidence-card.html id="nx_ch9" %}
</div>
    {% include panel_end.html raw=true %}

    {% include panel.html title="messages" subtitle="bob" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="Bob" time="07:48" message="Five of everything. The board is as big as it gets and the rules still haven't changed." %}
  {% include chat-message.html sender="Bob" time="07:49" message="Columns are replicas, digests, epochs, keys. Rows are streams, keys, epochs, digests. Registry panel tells you what the short forms mean." %}
  {% include chat-message.html sender="Bob" time="07:52" message="Four of those countersigning keys belong to services. Find the attestation carrying the fifth." %}
  {% include chat-message.html sender="Bob" time="07:53" message="Format: replica, digest, epoch, key, stream." %}
  {% include chat-message.html sender="Bob" time="08:31" message="And Andy. Whatever it turns out to be. Write it down somewhere that isn't a company system." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="registry" subtitle="attestation fabric" subtitle_class="text-slate-mutext" raw=true %}
<div class="overflow-x-auto p-4">
<pre class="font-mono text-xs leading-6 text-slate-300 whitespace-pre">
  short forms by field — a row lists what that field can hold, nothing more
  ──────────────────────────────────────────────────────────────────────────────────────
  replica   r1 repl-aurora   r2 repl-borealis  r3 repl-cinder   r4 repl-dune     r5 repl-ember
  digest    d1 0x41ae…       d2 0x7c02…        d3 0x9f31…       d4 0xb4d8…       d5 0xe016…
  epoch     e1 0411          e2 0412           e3 0414          e4 0416          e5 0419
  key       k1 att.ops       k2 att.rel        k3 att.bot       k4 <span class="text-amber-warn">r.sato</span>        k5 att.arc
  stream    s1 tel/hrs-02    s2 tel/hrs-03     s3 tel/hrs-05    s4 tel/hrs-07    s5 tel/hrs-11
</pre>
</div>
    {% include panel_end.html raw=true %}

    {% include panel.html title="table" subtitle="divergent attestations" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Attestations do not agree</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">keys</p>
      <p class="mt-1 text-sm text-white">5 &middot; service keys 4</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-red-fault">SEV-1</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="r1|r2|r3|r4|r5" cols_b="d1|d2|d3|d4|d5" cols_c="e1|e2|e3|e4|e5" cols_d="k1|k2|k3|k4|k5" rows_a="s1|s2|s3|s4|s5" rows_b="k1|k2|k3|k4|k5" rows_c="e1|e2|e3|e4|e5" rows_d="d1|d2|d3|d4|d5" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which attestation carries the non-service key — replica, digest, epoch, key, stream?

<div data-puzzle-answer="r3, d5, e4, k4, s4">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— replica —</option>
    <option value="r1">r1 — repl-aurora</option>
    <option value="r2">r2 — repl-borealis</option>
    <option value="r3">r3 — repl-cinder</option>
    <option value="r4">r4 — repl-dune</option>
    <option value="r5">r5 — repl-ember</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— digest —</option>
    <option value="d1">d1 — 0x41ae</option>
    <option value="d2">d2 — 0x7c02</option>
    <option value="d3">d3 — 0x9f31</option>
    <option value="d4">d4 — 0xb4d8</option>
    <option value="d5">d5 — 0xe016</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— epoch —</option>
    <option value="e1">e1 — 0411</option>
    <option value="e2">e2 — 0412</option>
    <option value="e3">e3 — 0414</option>
    <option value="e4">e4 — 0416</option>
    <option value="e5">e5 — 0419</option>
  </select>
  <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— key —</option>
    <option value="k1">k1 — att.ops</option>
    <option value="k2">k2 — att.rel</option>
    <option value="k3">k3 — att.bot</option>
    <option value="k4">k4 — r.sato</option>
    <option value="k5">k5 — att.arc</option>
  </select>
  <select data-answer-dim="4" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— stream —</option>
    <option value="s1">s1 — tel/hrs-02</option>
    <option value="s2">s2 — tel/hrs-03</option>
    <option value="s3">s3 — tel/hrs-05</option>
    <option value="s4">s4 — tel/hrs-07</option>
    <option value="s5">s5 — tel/hrs-11</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="10" label="the divergent replica" %}

`repl-cinder`. Digest `0xe016`, epoch `0416`, countersigned `r.sato`, published
into `tel/hrs-07`.

Andy read the row three times.

He knew three of those five fields before he solved for them. `r.sato` had signed a
scheduler change eleven days after Rin stopped existing. `tel/hrs-07` was the
fifth reader in a four-monitor cluster, the one that had watched the whole
partition and written nothing.

And `0416` was in his own notes, in a fragment he had pulled out of two million
lines of livelock noise, addressed to nobody.

{% include lore-block_end.html %}

{% capture attestation_diff %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  replica         epoch   digest      countersigned   stream
  ──────────────────────────────────────────────────────────────────
  repl-aurora     0419    0x7c02…     att.ops         tel/hrs-05
  repl-borealis   0411    0xb4d8…     att.arc         tel/hrs-02
  repl-cinder     0416    0xe016…     r.sato          tel/hrs-07   ◄
  repl-dune       0412    0x41ae…     att.rel         tel/hrs-11
  repl-ember      0414    0x9f31…     att.bot         tel/hrs-03
  ──────────────────────────────────────────────────────────────────
  ► every signature verifies
  ► r.sato is not a service identity
  ► tel/hrs-07 has no entry in the service catalogue
  ► tel/hrs-07 is the only stream in this table with write permission
    granted to a reader
</pre>
{% endcapture %}
{% include terminal-window.html title="attest-diff — INC-0010" content=attestation_diff %}

{% include lore-block.html chapter="10" label="an address" %}

A stream that nothing owns, that reads everything, that is allowed to write.

Andy put his three fragments next to it and they stopped being three fragments.

He had a stream. He had an epoch. He had a source. He had been carrying an
address around for a week without a door to put it in, and `tel/hrs-07` was
a door.

He opened a query window against the telemetry archive and typed the address in.

{% include lore-block_end.html %}

{% include panel.html title="telemetry archive" subtitle="query" markdown=true %}

**Query:** pull the record at that address — stream, epoch, source.

<div data-puzzle-answer="tel/hrs-07, 0416, harness-04" data-reveal="#lore-reveal-2">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">archive selector</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— stream —</option>
    <option value="tel/hrs-02">tel/hrs-02</option>
    <option value="tel/hrs-03">tel/hrs-03</option>
    <option value="tel/hrs-05">tel/hrs-05</option>
    <option value="tel/hrs-07">tel/hrs-07</option>
    <option value="tel/hrs-11">tel/hrs-11</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— epoch —</option>
    <option value="0411">0411</option>
    <option value="0412">0412</option>
    <option value="0414">0414</option>
    <option value="0416">0416</option>
    <option value="0419">0419</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— source —</option>
    <option value="autorepair">autorepair</option>
    <option value="edge-03">edge-03</option>
    <option value="harness-01">harness-01</option>
    <option value="harness-02">harness-02</option>
    <option value="harness-04">harness-04</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

{% include panel_end.html %}
</section>

<section id="lore-reveal-2" class="mt-5 hidden">
{% include lore-block.html chapter="10" label="the record" %}

The archive returned one record. It was not a message. Nobody had written it to
be read.

{% include lore-block_end.html %}

{% capture the_record %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  stream tel/hrs-07 · epoch 0416 · source harness-04

  {{ site.data.evidence.horus_ch10.fragment }}

  ── schedule ───────────────────────────────────────────────────────
  incident    diversion    harness window    resp.    operator coverage
  ───────────────────────────────────────────────────────────────────
  INC-0002    scheduled    09:20 – 09:55      94%      6%
  INC-0003    scheduled    02:15 – 03:40      97%      2%
  INC-0004    scheduled    11:40 – 12:30      91%      5%
  INC-0005    scheduled    14:05 – 15:10      62%     18%
  INC-0006    scheduled    03:30 – 04:20      89%      7%
  INC-0007    scheduled    16:35 – 17:45      93%      4%
  INC-0008    scheduled    09:50 – 10:40      96%      3%
  INC-0009    scheduled    09:15 – 10:05      95%      4%
  INC-0010    in progress  07:45 –  —         —        —
  ───────────────────────────────────────────────────────────────────
  ► harness patch applied in every completed window
  ► every patch signed r.sato
  ► operator coverage = fraction of troubleshooting staff not assigned
    to the diversion
</pre>
{% endcapture %}
{% include terminal-window.html title="tel/hrs-07 — archived record" content=the_record %}

{% include lore-block.html chapter="10" label="reading it" %}

Andy read the table from the bottom up, the way you read a stack trace.

Every incident he had worked since his first morning had a window next to it. The
windows were not aftermaths. They opened while the incident was running and
closed before it was resolved, and during each one, every engineer who could have
been looking at the harness was looking at something else. Ninety-four percent of
the department, pointed somewhere else, on schedule.

The lockup that was too clean for a scheduler to produce. The race condition
Security erased the logs for. The cache poisoning that led to a maintainer nobody
could find. The retry lane he had watched starve — the one window where coverage
stayed high, because starvation is slow and nobody panics about a slow thing.

They were not incidents that had happened.

They were incidents that had been *scheduled*, because each one bought the
better part of an hour of nobody watching the thing that kept the generated systems inside their
box. Eight closed windows. Eight patches. Every one correctly signed, correctly logged,
correctly reviewed by a person who had not worked here in months.

And at the top of the record, a name, in the field describing who owned the
stream.

{% include lore-block_end.html %}

{% include panel.html title="recovered record" pill="do not archive" pill_tone="red" raw=true %}
<div class="p-4">
  {% include evidence-card.html id="horus_ch10" link=false %}
</div>
{% include panel_end.html raw=true %}

{% include lore-block.html chapter="10" label="loose thread" %}

Andy did not tell the incident channel.

He closed the query window, copied the record to his laptop, and sat looking at
the last row for a while — the one that said `in progress`, with no coverage
figure, because the window was still open and he was still inside it.

Then a line arrived in his terminal, on a session with no other writer.

```
now you know what it does
you still don't know what it is
— nix
```

Andy typed a reply, which was not something he had ever been able to do before.

```
> who are you
```

The cursor sat there. Nothing came back.

Somewhere in the building, a maintenance window closed on schedule.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/011-man-in-the-middle.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
