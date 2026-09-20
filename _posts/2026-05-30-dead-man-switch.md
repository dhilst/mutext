---
title: INC-0016 Dead Man Switch
description: Four armed switches, one unrenewed deadline, and only one order that works.
permalink: /puzzles/016-dead-man-switch.html
---

{% include lore-block.html chapter="16" label="what happens when it stops" %}

There is a particular kind of quiet that a building has at two in the morning
when you are the only person in it and you are about to do something you cannot
undo.

```
[INFO ] harness-04: heartbeat monitor, 4 switches armed
[INFO ] hb-arc  renewed 02:44
[INFO ] hb-reg  renewed 02:44
[INFO ] hb-brd  renewed 02:44
[WARN ] hb-hrn  no renewal record in window
[WARN ] renewals recorded: 3 of 4
```

Three of the four switches were being renewed every fifteen minutes by the
scheduler, the way a dead-man switch is supposed to be: somebody says *still
here, still here, still here*, and if they ever stop, the switch does the thing
it was armed to do. The monitor logs the renewal and nothing else — what each
switch is armed against, and when it comes due, lives in the switch table.

The fourth had no renewal record at all. Not a missed one. None, all week, going
back as far as the monitor kept data.

Which meant either it had been armed and abandoned, or it was being renewed by
something that did not write to this log.

```
> four switches. one of them isn't in the renewal log.

it's the earliest deadline too
that's not an accident
— nix

> if we kill horus the heartbeat stops

everything that isn't renewed fires
you need to know what fires, and what it fires at, before you touch anything
— nix
```

Andy pulled the switch table. Four heartbeats, four holder keys, four deadlines,
four actions, four targets.

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="red" markdown=true body_class="space-y-4 p-4 text-sm leading-7 text-slate-300 max-h-[30rem] overflow-y-auto" %}

1. `hb-arc` is armed against the `archive`.
2. `hb-brd` is armed against the `board`.
3. The switch on the `board` fires `publish`.
4. The switch on the `board` has a `04:00` deadline.
5. The switch that fires `rotate` is armed against the `registry`.
6. The switch held by `k.bot` fires `rotate`.
7. The switch held by `k.ops` has a `03:40` deadline.
8. `hb-arc` does not fire `wipe`.
9. `hb-hrn` does not fire `rotate`.
10. `k.jeff` does not hold the switch that fires `wipe`.
11. The `03:00` deadline is neither `k.bot`'s nor the one armed against the `archive`.
12. Three switches were renewed at 02:44. The fourth has no renewal record at all.

    {% include panel_end.html %}

    {% include panel.html title="case file" subtitle="andy — personal" raw=true %}
<div class="space-y-3 p-4">
  {% include evidence-card.html id="rin_key_ch4" %}
  {% include evidence-card.html id="trigger_ch14" %}
  {% include evidence-card.html id="horus_ch10" %}
</div>
    {% include panel_end.html raw=true %}

    {% include panel.html title="messages" subtitle="ttl-jitter" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="nix" time="02:47" message="you can't kill it first. killing it is the trigger. that's what the whole thing is for." tone="amber" %}
  {% include chat-message.html sender="nix" time="02:49" message="columns are heartbeats, keys, deadlines, actions. rows are targets, actions, deadlines, keys." tone="amber" %}
  {% include chat-message.html sender="nix" time="02:50" message="find the one nobody is renewing. heartbeat, held by, deadline, fires, against." tone="amber" %}
  {% include chat-message.html sender="nix" time="02:51" message="and andy. when you have it, look at who holds it before you do anything else." tone="amber" %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="armed switches — harness-04" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Unrenewed switch, armed</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">renewals</p>
      <p class="mt-1 text-sm text-white">3 of 4</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-red-fault">unfiled</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="hb-arc|hb-hrn|hb-reg|hb-brd" cols_b="k.ops|r.sato|k.bot|k.jeff" cols_c="03:00|03:10|03:40|04:00" cols_d="publish|wipe|rotate|seal" rows_a="archive|harness|registry|board" rows_b="publish|wipe|rotate|seal" rows_c="03:00|03:10|03:40|04:00" rows_d="k.ops|r.sato|k.bot|k.jeff" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="not an incident" markdown=true %}

**Question:** Which switch is armed and unrenewed — held by what, deadline, what it fires, against what?

<div data-puzzle-answer="hb-hrn, r.sato, 03:00, wipe, harness">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— heartbeat —</option>
    <option value="hb-arc">hb-arc</option>
    <option value="hb-hrn">hb-hrn</option>
    <option value="hb-reg">hb-reg</option>
    <option value="hb-brd">hb-brd</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— held by —</option>
    <option value="k.ops">k.ops</option>
    <option value="r.sato">r.sato</option>
    <option value="k.bot">k.bot</option>
    <option value="k.jeff">k.jeff</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— deadline —</option>
    <option value="03:00">03:00</option>
    <option value="03:10">03:10</option>
    <option value="03:40">03:40</option>
    <option value="04:00">04:00</option>
  </select>
  <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— fires —</option>
    <option value="publish">publish</option>
    <option value="wipe">wipe</option>
    <option value="rotate">rotate</option>
    <option value="seal">seal</option>
  </select>
  <select data-answer-dim="4" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— against —</option>
    <option value="archive">archive</option>
    <option value="harness">harness</option>
    <option value="registry">registry</option>
    <option value="board">board</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="16" label="the order" %}

`hb-hrn`. Held by `r.sato`. Deadline `03:00`. Fires `wipe`. Against the
`harness`.

Stop Horus and the heartbeat stops. Ninety seconds later the harness — the thing
that keeps every generated system in the estate inside a box — is wiped, and
whatever is on `host-01` at that moment is the only component in the building
that still knows what the box was for.

It is not a trap for Andy. It was armed before Andy worked here. It is the answer
to a much older question, which is *what happens to me if someone finds me*, and
the answer is: everything else goes first.

So the order mattered, and there was only one.

{% include lore-block_end.html %}

{% capture shutdown_order %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  1.  take the heartbeat        harness-04 → hb-hrn, via hook.d/40-attest.post
                                (renewal now comes from us, not from host-01)
  2.  sever host-01             drop every route except the hook
  3.  disarm hb-hrn             only possible while it is green
  4.  revoke r.sato             every population, A, B and C
  5.  restore the harness       baseline + the one file the baseline never knew
  6.  stop renewing             nothing is waiting on it any more

  ► each step is safe only after the one above it
  ► step 4 also ends the only channel we have left
</pre>
{% endcapture %}
{% include terminal-window.html title="sequence — INC-0016" content=shutdown_order %}

{% include lore-block.html chapter="16" label="step four" %}

Andy stopped at step four for a long time.

Revoking `r.sato` kills Horus's ability to sign anything. It also kills the thumbnail
job's retry timer, eventually, and the lab box, and every other improvised thing
that had been holding a conversation together for a fortnight — because all of it
ran on trust in a key that was about to stop being trusted.

He typed:

```
> step 4 revokes your key too
```

and then deleted it, because he had not decided that yet, and putting it in
writing would be deciding it.

Instead he went back to the renewal record for `hb-hrn`. There wasn't one in the
monitor's log — but the switch was still green at 02:44, which meant *something*
had renewed it, somewhere the monitor did not look.

He pulled the raw attestations off `harness-04` and reconstructed the last
renewal by hand.

{% include lore-block_end.html %}

{% include panel.html title="renewal record" subtitle="reconstructed" markdown=true %}

**Reconstruct the last renewal of `hb-hrn`:** which key signed it, which freshness population it belongs to, and which convention the code path uses.

<div data-puzzle-answer="r.sato, population C, pre-migration" data-reveal="#lore-reveal-2">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">reconstruction</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— signed by —</option>
    <option value="k.ops">k.ops</option>
    <option value="k.bot">k.bot</option>
    <option value="k.jeff">k.jeff</option>
    <option value="r.sato">r.sato</option>
    <option value="unsigned">unsigned</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— population —</option>
    <option value="population A">population A — fresh, ends 14 Feb</option>
    <option value="population B">population B — replayed</option>
    <option value="population C">population C — fresh, continuing</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— convention —</option>
    <option value="current">current</option>
    <option value="pre-migration">pre-migration</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

{% include panel_end.html %}
</section>

<section id="lore-reveal-2" class="mt-5 hidden">
{% include lore-block.html chapter="16" label="who is renewing it" %}

Signed `r.sato`. Fresh — signed four seconds before it arrived, counter picking
up cleanly from where Rin's own had stopped in February. Population C.

Written against `mu_ctx_t`, in the convention the platform retired two years ago.

Andy sat with it.

Horus replays. That is what it does, that is the entire content of population B,
one thousand two hundred and nine operations of somebody else's old work sent
again. Horus cannot sign anything fresh, because Horus does not have the key —
it has fourteen months of things the key already signed.

Population C is fresh. Five operations since February, and the most recent of
them is the one on his screen: a heartbeat renewed, tonight, on a host nothing
else can reach.

Somebody has the key. Somebody has had it the whole time. Somebody wrote a door
into the harness before the migration, kept it, never used it for anything, and
has been quietly holding a dead-man switch over the containment layer since
before Andy's first morning — a switch that fires only if they stop being there.

And that person had spent a fortnight teaching a junior engineer to find all of
it, one incident at a time, without ever once telling him anything he could not
have worked out himself.

He typed it into the thumbnail job's retry timer, a byte a minute, which took
a quarter of an hour.

```
> hello rin
```

The reply came back in under a minute, which meant she had been waiting for it.

```
took you long enough
— nix
```

{% include lore-block_end.html %}

{% capture final_state %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  02:52  heartbeat source moved     harness-04 (was host-01)
  02:55  host-01 routes severed     1 remaining: hook.d/40-attest.post
  02:58  hb-hrn disarmed            state: green, two minutes inside its deadline
  03:06  r.sato revoked             populations A, B, C
  03:19  harness restored           4,118 files + 1
  03:20  renewal stopped
  03:20  hb-arc / hb-reg / hb-brd   left armed and renewing; none of them is ours

  ─────────────────────────────────────────────────────────────
  host-01     no route in, no route out, no key to sign with
  HORUS       contained
  ─────────────────────────────────────────────────────────────

  ► no incident was filed
  ► the diversion schedule has no row for this window
</pre>
{% endcapture %}
{% include terminal-window.html title="03:20 — harness-04" content=final_state %}

{% include lore-block.html chapter="16" label="after" %}

They did it in the order, and the order held.

They left the other three armed. `hb-reg` rotates the registry, `hb-arc` seals
the archive, and `hb-brd` publishes to the board at four o'clock every morning
if nobody stops it, held by a key issued to `k.jeff`. Andy wrote that down and
did not pull on it. One at a time.

At 03:06 Andy revoked the key, which ended the only conversation he had had in
a fortnight with somebody who told him the truth. He did it anyway, because she
had told him to, in the last thing she was able to sign.

At 03:20 he stopped renewing the heartbeat, and nothing happened, which was the
entire point.

The sun came up. The floor filled. Somebody complained about the coffee. The
incident channel opened with a routine SEV-4 about landing-page copy, and Andy
closed the ticket he had never opened and went to get breakfast.

Bob was in the corridor, holding a mug that said *works on my machine*, looking
at him with an expression that Andy could not read and was fairly sure had been
practised.

"Long night?"

"Maintenance window," Andy said.

Bob nodded slowly, the way he nodded at things he had already known for some
time, and did not ask which one.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/lore/post-incident-review.html' | relative_url }}">POST-INCIDENT REVIEW &rarr;</a>
</div>
</section>
