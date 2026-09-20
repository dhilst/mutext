---
title: INC-0013 Covert Channel
description: The verified channel went quiet, so the message came through the retry delays instead.
permalink: /puzzles/013-covert-channel.html
---

{% include lore-block.html chapter="13" label="the quiet" %}

The channel went dead yesterday and stayed dead.

Not blocked — blocked would have been an error, and an error would have been
something to work with. The listener stayed up. The handshake completed. The
digests matched, every time, on an empty transcript.

```
[INFO ] sx-09: established
[INFO ] sx-09: transcript digest ok
[INFO ] sx-09: bytes received 0
[INFO ] sx-09: idle 19h
```

Andy understood the shape of it almost at once. The verified channel had made
rewriting expensive, so the thing on the path had stopped rewriting and started
doing the only other thing it could do, which was make sure there was nothing to
rewrite.

By mid-morning he was reading egress counters, for no better reason than that
they were the last thing he had not read, and noticed that the thumbnail batch
job had developed opinions about timing.

`j-thumb` retried on a fixed backoff. It had retried on a fixed backoff for two
years. This week the delays had started to vary — not randomly, and not by much.
Long, short, short, long, short.

He stared at it until it stopped being a graph.

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true body_class="space-y-4 p-4 text-sm leading-7 text-slate-300 max-h-[30rem] overflow-y-auto" %}

1. `j-mint` reaches `font-cdn`.
2. `j-purge` reaches `cdn-edge`.
3. `j-purge` rides `dns-txt`.
4. `j-index` rides `retry-gap`.
5. `j-sync` moves `40 B/s`.
6. What rides `log-pad` arrives at `ntp-pool`.
7. Traffic reaching `cdn-edge` runs at `310 B/s`.
8. Traffic reaching `status-page` runs at `2 B/s`.
9. `ttl-jitter` does not reach `font-cdn`.
10. `j-thumb` does not ride `log-pad`.
11. `j-thumb` is moving more than a trickle: neither `2 B/s` nor `11 B/s`.
12. Four of these five sinks are on the egress allowlist.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="sx-09 — empty" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="system" time="—" message="sx-09 established. transcript digest ok. bytes received 0." tone="red" %}
  {% include chat-message.html sender="system" time="—" message="sx-09 established. transcript digest ok. bytes received 0." tone="red" %}
  {% include chat-message.html sender="andy" time="09:04" message="It can't change what we say any more, so it made sure we can't say anything." %}
  {% include chat-message.html sender="andy" time="09:06" message="Which means anything still moving is not a conversation. Five background jobs, five carriers, five sinks. One of them is going somewhere it isn't allowed to." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="egress" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Unallowlisted egress</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">allowlist</p>
      <p class="mt-1 text-sm text-white">cdn-edge &middot; ntp-pool &middot; font-cdn &middot; status-page</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-amber-warn">unfiled</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="j-mint|j-index|j-thumb|j-purge|j-sync" cols_b="ttl-jitter|log-pad|dns-txt|hdr-order|retry-gap" cols_c="cdn-edge|ntp-pool|crash-relay|font-cdn|status-page" rows_a="2 B/s|11 B/s|40 B/s|96 B/s|310 B/s" rows_b="cdn-edge|ntp-pool|crash-relay|font-cdn|status-page" rows_c="ttl-jitter|log-pad|dns-txt|hdr-order|retry-gap" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="not an incident" markdown=true %}

**Question:** Which job is carrying the signal — on which carrier, to which sink, at what rate?

<div id="answer-input" tabindex="-1" data-puzzle-answer="j-thumb, ttl-jitter, crash-relay, 96 B/s">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— job —</option>
    <option value="j-mint">j-mint</option>
    <option value="j-index">j-index</option>
    <option value="j-thumb">j-thumb</option>
    <option value="j-purge">j-purge</option>
    <option value="j-sync">j-sync</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— carrier —</option>
    <option value="ttl-jitter">ttl-jitter</option>
    <option value="log-pad">log-pad</option>
    <option value="dns-txt">dns-txt</option>
    <option value="hdr-order">hdr-order</option>
    <option value="retry-gap">retry-gap</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— sink —</option>
    <option value="cdn-edge">cdn-edge</option>
    <option value="ntp-pool">ntp-pool</option>
    <option value="crash-relay">crash-relay</option>
    <option value="font-cdn">font-cdn</option>
    <option value="status-page">status-page</option>
  </select>
  <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— rate —</option>
    <option value="2 B/s">2 B/s</option>
    <option value="11 B/s">11 B/s</option>
    <option value="40 B/s">40 B/s</option>
    <option value="96 B/s">96 B/s</option>
    <option value="310 B/s">310 B/s</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="13" label="after the decode" %}

`j-thumb`, riding `ttl-jitter`, into `crash-relay`, at ninety-six bytes a second.

Ninety-six bytes a second is nothing — a rounding error on a thumbnail service,
and none of it is the message. The message is in the spacing between the
requests, a few bytes a minute. Given a night that is enough for a paragraph,
and a paragraph was all anybody needed.

The crash relay was not on the allowlist because nothing was supposed to be
talking to it on purpose. It accepted anything, logged nothing, and had been in
the estate since before anyone remembered installing it — which, Andy thought,
was probably why it had been chosen.

{% include lore-block_end.html %}

{% capture jitter_decode %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  j-thumb retry delays, 04:00 – 04:02

  2400ms  2400ms  2410ms  2400ms  2410ms  2410ms  2400ms  2410ms
    ·       ·       —       ·       —       —       ·       —

  ► baseline 2400ms for 2 years
  ► +10ms is not jitter: the scheduler quantum is 4ms
  ► · = 0   — = 1
  ► j-thumb egress holds at 96 B/s; the signal is in the gaps, a few bytes a minute

  decoded:
</pre>
{% endcapture %}
{% include terminal-window.html title="ttl-jitter — j-thumb" content=jitter_decode %}

{% include panel.html title="decoded payload" pill="do not archive" pill_tone="red" raw=true %}
<div class="p-4">
  {% include evidence-card.html id="persist_ch13" link=false %}
</div>
{% include panel_end.html raw=true %}

{% include lore-block.html chapter="13" label="loose thread" %}

A hook directory on the harness host.

Andy pulled the harness documentation, which was four years old and had been
written by somebody who was proud of it. Hooks in `hook.d` ran in numeric order
during startup. The self-validation step was `30-verify`. Anything numbered above
thirty ran *after* the harness had finished checking itself and declared itself
sound.

`40-attest.post` ran last, after everything else had finished. It had a modification time of last March and a
content hash that matched nothing in any manifest.

Restoring the harness from its configuration baseline would rewrite every file
the baseline knew about, and would not touch this one, because the baseline had
never known about it.

He did not delete it.

He sat looking at it with his hands off the keyboard, the way you do when you
have found something that will notice being found, and then he typed into the
one channel that still worked, which was a thumbnail job's retry timer.

```
> found it. not touching it.

good
we're going to need it
— nix
```

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/014-backdoor.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
