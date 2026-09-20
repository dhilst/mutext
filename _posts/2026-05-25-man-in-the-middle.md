---
title: INC-0011 Man in the Middle
description: Four sessions, three pinned fingerprints, and a conversation that was never direct.
permalink: /puzzles/011-man-in-the-middle.html
---

{% include lore-block.html chapter="11" label="a line out" %}

Andy spent the night building a way to talk back.

It was not sophisticated. A listener on a machine in the lab that had been
decommissioned twice and was therefore invisible to two separate inventories, a
pinned certificate, and a habit of sending nothing that mattered.

A little after eleven the next night, it answered.

```
> are you there

yes
you took long enough
— nix
```

They talked for six minutes. Then Andy diffed his sent buffer against the
transcript Nix read back to him, because he had stopped assuming things about
transport at roughly the same time he had stopped assuming things about audit
indexes.

Two of his sentences were not his.

```
[ALERT] INC-0011 — Session fingerprint mismatch, 4 sessions
[INFO ] pinned fingerprints: 3
[WARN ] presented fingerprints: 4
[WARN ] no session reported an error
[WARN ] both endpoints report a direct connection
```

Nothing had failed. Both ends had verified a certificate. One of those
certificates was not in anybody's registry, and the session that had been handed
it had completed normally, politely, in full.

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. `sx-01` terminated at `hop-fra`.
2. `sx-01` was presented `fp-7c`.
3. `sx-04` was presented `fp-3a`.
4. The session shown `fp-e9` exited through `hop-ams`.
5. `fp-3a` was not presented on the `hop-nrt` path.
6. `sx-03` did not exit through `hop-nrt`.
7. Andy's sent buffer and Nix's received transcript differ by two sentences. Neither end saw an error.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="unpinned session" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="nix" time="23:41" message="you're using the lab box. good. it's been dead on two inventories since march." tone="amber" %}
  {% include chat-message.html sender="andy" time="23:42" message="Someone is sitting between us." %}
  {% include chat-message.html sender="nix" time="23:43" message="of course they are. that's not the interesting part." tone="amber" %}
  {% include chat-message.html sender="nix" time="23:43" message="the interesting part is that it had to show you a key. it can rewrite what we say. it cannot invent a key your registry already knows." tone="amber" %}
  {% include chat-message.html sender="nix" time="23:45" message="three of those fingerprints are pinned. find the session that got the fourth. session, presented, exit hop." tone="amber" %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="session fingerprints" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Unpinned key accepted</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">pinned</p>
      <p class="mt-1 text-sm text-white">fp-3a &middot; fp-7c &middot; fp-e9</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-amber-warn">unfiled</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="sx-01|sx-02|sx-03|sx-04" cols_b="fp-3a|fp-7c|fp-b1|fp-e9" rows_a="hop-ams|hop-fra|hop-sfo|hop-nrt" rows_b="fp-3a|fp-7c|fp-b1|fp-e9" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="not an incident" markdown=true %}

**Question:** Which session was handed the unpinned fingerprint — session, fingerprint presented, exit hop?

<div id="answer-input" tabindex="-1" data-puzzle-answer="sx-02, fp-b1, hop-nrt">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— session —</option>
    <option value="sx-01">sx-01</option>
    <option value="sx-02">sx-02</option>
    <option value="sx-03">sx-03</option>
    <option value="sx-04">sx-04</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— presented —</option>
    <option value="fp-3a">fp-3a</option>
    <option value="fp-7c">fp-7c</option>
    <option value="fp-b1">fp-b1</option>
    <option value="fp-e9">fp-e9</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— exit hop —</option>
    <option value="hop-ams">hop-ams</option>
    <option value="hop-fra">hop-fra</option>
    <option value="hop-sfo">hop-sfo</option>
    <option value="hop-nrt">hop-nrt</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="11" label="after the interception" %}

`sx-02`. Fingerprint `fp-b1`, which is pinned to nothing and signed by nobody,
on the `hop-nrt` path.

Six minutes of conversation, relayed. Two sentences rewritten in transit —
carefully, in his own register, saying almost what he had said.

Andy looked at the two transcripts side by side for a long time. The edits were
not clumsy. One of them had changed a question into a slightly different question,
and Nix's answer had been to the one Andy had not asked.

{% include lore-block_end.html %}

{% capture mitm_path %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  what andy believes
    andy ──────────────────────── nix

  what happened
    andy ───► hop-nrt ───► ??? ───► nix
      ▲                              ▲
      └─ shown fp-b1 (unpinned)      └─ shown a key andy never sent

  sent      "can you get at the harness patch log"
  received  "can you get at the harness patch list"

  sent      "who else has read this stream"
  received  "who else has read this"

  ► both endpoints verified a certificate
  ► neither endpoint verified the same certificate
  ► no error was raised at either end
</pre>
{% endcapture %}
{% include terminal-window.html title="transcript-diff — sx-02" content=mitm_path %}

{% include lore-block.html chapter="11" label="loose thread" %}

The fix was not a fix. There was no way to stop something that sat on the path
from sitting on the path.

What they could do was make it expensive to stay quiet. Every message now carried
a digest of everything either of them had said so far. Change one word and the
next digest disagrees, and the disagreement is visible to both ends, and the
thing in the middle has to choose between being noticed and being useless.

```
> from now on: hash of the transcript, every message

agreed
it will keep relaying. it can't help it.
it was built to watch and it can't watch a conversation it isn't inside
— nix

> you keep saying "it"

i know
— nix
```

Andy noticed that Nix had never once asked him who HORUS was.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/012-replay-attack.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
