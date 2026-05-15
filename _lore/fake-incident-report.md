---
title: Fake Incident Report
description: A static sample μ-text incident report.
---

<article class="shell-panel">
  <div class="panel-header">
    <span>archive / incident report</span>
    {% include status-pill.html label="INC-0417" tone="red" %}
  </div>
  <div class="grid gap-5 p-5 lg:grid-cols-[1fr_18rem]">
    <div>
      <h1 class="text-2xl font-semibold text-white">Payroll Helper Hallucinated a Department</h1>
      <p class="mt-3 text-sm leading-6 text-slate-300">The payroll assistant created recurring budget lines for a department named Continuity. Finance denied ownership. HR recognized three employees. Facilities confirmed the floor number but not the building.</p>
      <div class="mt-5">
        {% capture report_logs %}07:12 generated department accepted by payroll helper|07:13 org chart rendered Continuity beneath Executive Operations|07:17 employee count changed from 0 to 3 without write event|07:30 Bob requested quiet escalation|07:31 quiet escalation produced alert noise{% endcapture %}
        {% include fake-log.html lines=report_logs prefix="report" %}
      </div>
    </div>
    <aside class="border border-slate-700/70 bg-slate-950/55 p-4">
      <p class="font-mono text-xs uppercase text-slate-mutext">metadata</p>
      <dl class="mt-4 space-y-3 text-sm">
        <div class="flex justify-between gap-3"><dt class="text-slate-mutext">Severity</dt><dd class="font-mono text-red-fault">SEV-2</dd></div>
        <div class="flex justify-between gap-3"><dt class="text-slate-mutext">Owner</dt><dd class="font-mono text-cyan-trace">@bob</dd></div>
        <div class="flex justify-between gap-3"><dt class="text-slate-mutext">Deployment</dt><dd class="font-mono text-amber-warn">partial</dd></div>
        <div class="flex justify-between gap-3"><dt class="text-slate-mutext">Status</dt><dd class="font-mono text-phosphor">contained</dd></div>
      </dl>
    </aside>
  </div>
</article>
