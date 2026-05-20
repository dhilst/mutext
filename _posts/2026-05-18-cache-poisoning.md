---
title: INC-0004 Cache Poisoning
description: Edge caches return tenant data to the wrong clients — isolation failure or something worse.
permalink: /puzzles/004-cache-poisoning.html
---

{% include lore-block.html chapter="04" label="cache poisoning" %}

The alert hit every channel at once.

```
[ALERT] INC-0004 — Tenant isolation failure on edge cache layer
[ALERT] Company helios receiving orion dashboard widgets
[ALERT] API sessions returning mismatched tenant contexts
[ALERT] Invalid feature flags propagating globally
[CRITC] /session endpoint: poisoned data detected
```

Andy stared at the dashboard. Three different tenants were receiving each other's configuration data. Sessions appeared swapped. Feature flags meant for one company were activating inside another.

Security posted within minutes: external intrusion. Cache poisoning. Credential compromise.

But Bob sent a direct message before the all-hands even started.

"Ignore Security's thread. Look at which infrastructure routes are affected."

Andy pulled the cache topology. The corruption wasn't random. It followed specific routes — `/config`, `/session`, `/feature` — across specific edge nodes.

All of them had been maintained by someone named Rin.

Andy searched for Rin in the company directory. No results.

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. The poisoned `/session` route did not originate from `edge-01`.
2. `atlas` was not affected through `/feature`.
3. A recovered fragment from Rin's maintenance log: `node=edge-03 route=/config — invalidated`. Bob: "Funny how nobody can explain when exactly Rin left."
4. `edge-03` only served corrupted data to `helios`.
5. A partial audit fragment recovered from backup: `tenant=orion route=/feature`
6. A malformed telemetry line appears in the edge-03 log: `cache.invalidate("truth")`. Bob dismisses it as junk data. Andy does not.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="bob" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="Bob" time="11:42" message="Don't use internal search for Rin. Half the records are gone." %}
  {% include chat-message.html sender="Bob" time="11:44" message="Someone is cleaning logs faster than Security can archive them." %}
  {% include chat-message.html sender="Bob" time="11:47" message="If this were an external breach, they'd already have announced it." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="cache topology" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Tenant data cross-contamination</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">type</p>
      <p class="mt-1 text-sm text-white">Cache isolation failure</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-amber-warn">SEV-1</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="helios|orion|atlas" cols_b="/config|/session|/feature" rows_a="edge-01|edge-02|edge-03" rows_b="/config|/session|/feature" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which tenant received poisoned data, through which edge node, on which route?

<div data-puzzle-answer="atlas, edge-02, /session">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— tenant —</option>
    <option value="helios">helios</option>
    <option value="orion">orion</option>
    <option value="atlas">atlas</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— edge node —</option>
    <option value="edge-01">edge-01</option>
    <option value="edge-02">edge-02</option>
    <option value="edge-03">edge-03</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— route —</option>
    <option value="/config">/config</option>
    <option value="/session">/session</option>
    <option value="/feature">/feature</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="04" label="after the poison" %}

Andy traced the corruption back through the cache invalidation logs.

Every affected route had the same pattern: a valid cache entry replaced by a stale replica. Not random. Surgical. Someone had rewritten the cache layer from the inside.

He searched for the original maintainer records. Every reference to Rin had been replaced:

```
[REDACTED BY POLICY]
```

But the cache diagnostic snapshots used a different index. Andy pulled the archived version.

{% include lore-block_end.html %}

{% capture cache_snapshot %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  CACHE DIAGNOSTIC SNAPSHOT — edge-03
  ────────────────────────────────────
  route        maintainer       status
  ────────────────────────────────────
  /config      [REDACTED]       invalidated
  /session     [REDACTED]       invalidated
  /feature     [REDACTED]       invalidated
  ────────────────────────────────────
  last_deploy  [REDACTED]
  maintainer_key=r.sato
  ────────────────────────────────────
  ► all maintainer fields scrubbed
  ► key survived in legacy index
</pre>
{% endcapture %}
{% include terminal-window.html title="cache-diag — edge-03 (archived)" content=cache_snapshot %}

{% include lore-block.html chapter="04" label="loose thread" %}

Rin had root-level infrastructure access. And someone was actively scrubbing every trace of that access from the system.

Andy closed the diagnostic window. A new telemetry fragment appeared in his terminal before he could log out:

```
you are being monitored too
— nix
```

He stared at it for a long time.

Then he closed his laptop.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/005-deadletter.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
