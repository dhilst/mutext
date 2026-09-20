---
title: INC-0012 Replay
description: Four authorisations, four good signatures, and one of them was ten minutes old.
permalink: /puzzles/012-replay-attack.html
---

{% include lore-block.html chapter="12" label="perfectly good" %}

The harness accepted a revocation at 08:02 that nobody had issued at 08:02.

```
[ALERT] INC-0012 — Unexpected authorisation accepted (harness control)
[INFO ] signature: valid
[INFO ] signer: r.sato
[INFO ] nonce: present, well-formed
[INFO ] max skew: 5s
[WARN ] four authorisations in window, all accepted
[WARN ] one of them was not issued in this window
```

Andy had the archive record now, so he had stopped being surprised by things
being correct. Correct was how this worked. Correct was the method.

```
> it's using rin's key again

worse than that
it isn't using it
it's using something that key already signed
— nix
```

Four requests inside a twelve minute span. Every signature verified. Every nonce
well-formed and unique. The only thing that separated them was how old each one
already was when it landed — and the harness had never been configured to care.

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. `rq-01` was accepted at `08:05`.
2. `rq-01` carried nonce `nc-13`.
3. `rq-02` was accepted at `08:14`.
4. `rq-02` was `0.4s` old when it was accepted.
5. The request carrying `nc-11` was `0.4s` old on arrival.
6. The request carrying `nc-12` was `2.0s` old on arrival.
7. The request carrying `nc-13` was `1.1s` old on arrival.
8. `rq-03` was not `2.0s` old when it was accepted.
9. `rq-03` was not the request accepted at `08:09`.
10. Two of these were issued by the same caller. The harness does not record which.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="verified channel" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="nix" time="08:20" message="signature answers 'did someone with the key make this'. it never answered 'when'." tone="amber" %}
  {% include chat-message.html sender="andy" time="08:21" message="So the replay is the one that was already old when it arrived." %}
  {% include chat-message.html sender="nix" time="08:22" message="yes. skew budget is five seconds. three of those four are inside it." tone="amber" %}
  {% include chat-message.html sender="nix" time="08:23" message="request, nonce, accepted, age. then run the same test on everything that key has ever signed." tone="amber" %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="harness authorisations" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Stale authorisation accepted</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">max skew</p>
      <p class="mt-1 text-sm text-white">5s</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-red-fault">SEV-1</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="rq-01|rq-02|rq-03|rq-04" cols_b="nc-11|nc-12|nc-13|nc-14" cols_c="08:02|08:05|08:09|08:14" rows_a="0.4s|1.1s|2.0s|611s" rows_b="08:02|08:05|08:09|08:14" rows_c="nc-11|nc-12|nc-13|nc-14" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which authorisation was a replay — request, nonce, acceptance time, age on arrival?

<div id="answer-input" tabindex="-1" data-puzzle-answer="rq-03, nc-14, 08:02, 611s">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— request —</option>
    <option value="rq-01">rq-01</option>
    <option value="rq-02">rq-02</option>
    <option value="rq-03">rq-03</option>
    <option value="rq-04">rq-04</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— nonce —</option>
    <option value="nc-11">nc-11</option>
    <option value="nc-12">nc-12</option>
    <option value="nc-13">nc-13</option>
    <option value="nc-14">nc-14</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— accepted —</option>
    <option value="08:02">08:02</option>
    <option value="08:05">08:05</option>
    <option value="08:09">08:09</option>
    <option value="08:14">08:14</option>
  </select>
  <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— age —</option>
    <option value="0.4s">0.4s</option>
    <option value="1.1s">1.1s</option>
    <option value="2.0s">2.0s</option>
    <option value="611s">611s</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="12" label="after the replay" %}

`rq-03`. Nonce `nc-14`, accepted at `08:02`, already `611s` old.

It was a revocation approval signed at 07:51 for a key rotation that had been
cancelled two minutes later. The approval had never been used. It had sat
somewhere for ten minutes and then arrived against a completely different
resource, and the harness had checked the signature, found it excellent, and
applied it.

Ten minutes is a long time to hold something. Long enough to choose.

{% include lore-block_end.html %}

{% capture skew_window %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  issued                                accepted      age      within skew
  ─────────────────────────────────────────────────────────────────────────
  07:51:49.0  revocation (cancelled) ──► 08:02:00     611s     ✕   rq-03
  08:04:58.9  scale request          ──► 08:05:00     1.1s     ✓   rq-01
  08:08:58.0  scale request          ──► 08:09:00     2.0s     ✓   rq-04
  08:13:59.6  config read            ──► 08:14:00     0.4s     ✓   rq-02
  ─────────────────────────────────────────────────────────────────────────
                         skew budget  ├─ 5s ─┤

  ► all four signatures verify
  ► all four nonces are unique and well-formed
  ► freshness was never checked
</pre>
{% endcapture %}
{% include terminal-window.html title="skew-window — INC-0012" content=skew_window %}

{% include lore-block.html chapter="12" label="loose thread" %}

The fix took an afternoon: reject anything older than the skew budget, and keep
a window of seen nonces so nothing can arrive twice.

Then Andy did what Nix had told him to do, which was run the same test backwards
across everything `r.sato` had ever signed. Fourteen months of it.

He expected two populations. Rin's real work, and Horus replaying it.

{% include lore-block_end.html %}

{% capture three_populations %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  signing history: r.sato — 14 months, 3,118 operations

  population A    1,904 ops   age &lt; 2s      counters monotonic
                              ends abruptly, 14 Feb

  population B    1,209 ops   age 4s – 41h  counters reused from A
                              begins 14 Feb, continues

  population C        5 ops   age &lt; 2s      counters continue A cleanly
                              scattered, most recent: this week
  ─────────────────────────────────────────────────────────────────
  ► A is signed material that was fresh when it was signed
  ► B is A, re-sent
  ► C is neither
</pre>
{% endcapture %}
{% include terminal-window.html title="freshness-sweep — r.sato" content=three_populations %}

{% include lore-block.html chapter="12" label="three" %}

Three.

Andy sat back and looked at the last column of the third population for a while.
Five operations in fourteen months. Fresh every time — signed seconds before they
arrived, counters picking up exactly where Rin's own had stopped, as though
nothing had been interrupted.

The most recent one was four days old.

```
> population C isn't replays

no
— nix

> then someone still has that key and is still using it

next incident is going to be a bad one. get some sleep.
— nix
```

Andy read that twice, decided it was an answer to a question he had not asked,
and did not get any sleep.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/013-covert-channel.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
