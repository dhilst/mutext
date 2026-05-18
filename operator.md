---
title: Operator
description: Operator profile and shift status for μ-text.
---

<section class="grid gap-5 lg:grid-cols-[22rem_minmax(0,1fr)]">
  {% include operator-panel.html %}

  <div class="space-y-5">
    <section class="shell-panel">
      <div class="panel-header">
        <span>shift summary</span>
        {% include status-pill.html label="active" tone="green" %}
      </div>
      <div class="grid gap-4 p-4 md:grid-cols-3">
        <div class="metric-tile">
          <p class="font-mono text-xs uppercase text-slate-mutext">assigned incidents</p>
          <p class="mt-3 font-mono text-3xl text-cyan-trace">01</p>
          <p class="mt-2 text-sm text-slate-mutext">Training queue only, according to Bob.</p>
        </div>
        <div class="metric-tile">
          <p class="font-mono text-xs uppercase text-slate-mutext">clearance</p>
          <p class="mt-3 font-mono text-3xl text-amber-warn">T-0</p>
          <p class="mt-2 text-sm text-slate-mutext">Enough to see the problem, not enough to explain it.</p>
        </div>
        <div class="metric-tile">
          <p class="font-mono text-xs uppercase text-slate-mutext">console trust</p>
          <p class="mt-3 font-mono text-3xl text-phosphor">64%</p>
          <p class="mt-2 text-sm text-slate-mutext">The remaining percentage is under review.</p>
        </div>
      </div>
    </section>

    <section class="shell-panel">
      <div class="panel-header">
        <span>operator feed</span>
        <span>profile.log</span>
      </div>
      <div class="p-4">
        {% capture operator_logs %}08:42 badge provisioned for andy.j|08:47 workstation image restored from approved snapshot|08:58 Bob assigned mutual recursion deadlock|09:00 operator console acknowledged first shift|09:04 deadlock detector shared retained thread dump{% endcapture %}
        {% include fake-log.html lines=operator_logs prefix="operator" %}
      </div>
    </section>

    <section class="shell-panel">
      <div class="panel-header">
        <span>available actions</span>
        <span>no persistence</span>
      </div>
      <div class="flex flex-wrap gap-3 p-4">
        <a class="button-primary" href="{{ '/puzzles/001-tutorial.html' | relative_url }}">Open active incident</a>
        <a class="button-quiet" href="{{ '/lore/onboarding-memo.html' | relative_url }}">Read onboarding memo</a>
        <button class="button-quiet" type="button" data-fake-action="PING BOB">PING BOB</button>
      </div>
    </section>
  </div>
</section>
