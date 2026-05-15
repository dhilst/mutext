---
title: Shift Console
---

<section class="relative overflow-hidden border border-cyan-trace/20 bg-panel/80 p-5 shadow-terminal md:p-8">
  <div class="absolute inset-0 opacity-20" aria-hidden="true">
    <div class="h-full w-full bg-[linear-gradient(90deg,rgba(103,232,249,0.08)_1px,transparent_1px),linear-gradient(rgba(103,232,249,0.06)_1px,transparent_1px)] bg-[size:48px_48px]"></div>
  </div>
  <div class="relative grid gap-8 lg:grid-cols-[1fr_22rem] lg:items-end">
    <div>
      <div class="mb-6 inline-flex items-center gap-3 border border-cyan-trace/25 bg-cyan-trace/10 px-3 py-2 font-mono text-xs text-cyan-trace">
        <span class="status-dot"></span>
        SHIFT HANDOFF READY
      </div>
      <p class="font-mono text-sm text-slate-mutext">μ-text Systems / Troubleshooting Department</p>
      <h1 class="mt-4 max-w-3xl text-4xl font-semibold text-white sm:text-5xl lg:text-6xl">Incident reconstruction console</h1>
      <p class="mt-5 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
        Your first shift starts in the archive where generated software failures are reconstructed, sanitized, and quietly made someone else's problem.
      </p>
      <div class="mt-7 flex flex-wrap gap-3">
        <a class="button-primary" href="{{ '/puzzles/tutorial.html' | relative_url }}">BEGIN SHIFT</a>
        <a class="button-quiet" href="{{ '/lore/onboarding-memo.html' | relative_url }}">Review memo</a>
      </div>
    </div>

    <div class="border border-slate-700/70 bg-slate-950/70 p-4 font-mono text-xs text-slate-300">
      <div class="mb-3 flex items-center justify-between text-slate-mutext">
        <span>ai-gen uptime</span>
        <span class="text-phosphor">99.91%</span>
      </div>
      <div class="space-y-2">
        <div class="h-2 w-full bg-slate-800"><div class="h-full w-[91%] bg-phosphor"></div></div>
        <div class="h-2 w-full bg-slate-800"><div class="h-full w-[68%] bg-cyan-trace"></div></div>
        <div class="h-2 w-full bg-slate-800"><div class="h-full w-[37%] bg-amber-warn"></div></div>
      </div>
      <div class="mt-5 grid grid-cols-8 gap-1" aria-hidden="true">
        {% for i in (1..48) %}
          <span class="h-5 border border-cyan-trace/10 bg-cyan-trace" style="opacity: {% cycle '0.10', '0.05', '0.02', '0.16', '0.06', '0.03' %}"></span>
        {% endfor %}
      </div>
    </div>
  </div>
</section>

<section class="mt-5 grid gap-5 md:grid-cols-3">
  <div class="metric-tile">
    <p class="font-mono text-xs uppercase text-slate-mutext">active incidents</p>
    <p class="mt-3 font-mono text-3xl text-cyan-trace">07</p>
    <p class="mt-2 text-sm text-slate-mutext">Two are customer-visible. One denies existing.</p>
  </div>
  <div class="metric-tile">
    <p class="font-mono text-xs uppercase text-slate-mutext">unresolved failures</p>
    <p class="mt-3 font-mono text-3xl text-amber-warn">143</p>
    <p class="mt-2 text-sm text-slate-mutext">Down from yesterday, according to the dashboard.</p>
  </div>
  <div class="metric-tile">
    <p class="font-mono text-xs uppercase text-slate-mutext">generation uptime</p>
    <p class="mt-3 font-mono text-3xl text-phosphor">99.91%</p>
    <p class="mt-2 text-sm text-slate-mutext">The missing 0.09% has been archived.</p>
  </div>
</section>

<section class="mt-5 grid gap-5 xl:grid-cols-[1.1fr_0.9fr]">
  <div class="shell-panel">
    <div class="panel-header">
      <span>incident queue</span>
      {% include status-pill.html label="triage open" tone="amber" %}
    </div>
    <div class="grid gap-3 p-4 md:grid-cols-2">
      {% include incident-card.html id="INC-0001" severity="SEV-3" tone="amber" time="08:17" title="Mutual recursion deadlock" body="Invoice reconciliation and ledger rollup now wait on each other's locks after the retry checksum patch." env="training" owner="@andy" %}
      {% include incident-card.html id="INC-0417" severity="SEV-2" tone="red" time="08:44" title="Payroll helper hallucinated a department" body="The org chart now contains a floor that Facilities says is not in the building." env="corp-prod" owner="@bob" %}
      {% include incident-card.html id="INC-0520" severity="SEV-4" tone="cyan" time="09:02" title="Marketing copy loop" body="Landing page regenerates the same sentence with increasing confidence and fewer verbs." env="public" owner="@marta" %}
      {% include incident-card.html id="INC-0713" severity="SEV-3" tone="amber" time="09:31" title="Log timestamps moved backward" body="Monitoring insists the deployment failed tomorrow. SRE asked us to stop saying that." env="observability" owner="@queue" %}
    </div>
  </div>

  <div class="shell-panel">
    <div class="panel-header">
      <span>archive preview</span>
      <span class="text-slate-mutext">restricted</span>
    </div>
    <div class="p-5">
      <blockquote class="border-l-2 border-cyan-trace/60 pl-4 font-mono text-lg leading-8 text-white terminal-cursor">
        We don't write the code anymore.<br>
        We only clean up after it.
      </blockquote>
      <p class="mt-5 text-sm leading-6 text-slate-mutext">
        Internal audits describe incident reconstruction as "low-risk interpretive maintenance." Bob says that phrase means the company lawyers won.
      </p>
      <div class="mt-5">
        {% capture log_lines %}08:59 deploy train/onboarding accepted by generator|09:01 Bob approved incident simulation|09:03 contradiction surfaced in seating matrix|09:04 archive observer joined without credentials{% endcapture %}
        {% include fake-log.html lines=log_lines prefix="memo" %}
      </div>
    </div>
  </div>
</section>
