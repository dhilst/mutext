---
title: Incident Archive
permalink: /archive.html
---

<section class="shell-panel">
  <div class="panel-header">
    <span>incident archive</span>
    {% include status-pill.html label="chronological" tone="cyan" %}
  </div>
  <div class="divide-y divide-slate-700/70">
    {% assign puzzles = site.posts | sort: "date" %}
    {% for post in puzzles %}
    {% assign slug = post.url | split: "/" | last | remove: ".html" %}
    <a href="{{ post.url | relative_url }}" data-chapter="{{ slug }}" class="archive-row flex items-baseline gap-4 px-5 py-4 transition hover:bg-cyan-trace/[0.04]">
      <span class="font-mono text-xs text-slate-mutext whitespace-nowrap">{{ post.date | date: "%Y-%m-%d" }}</span>
      <span class="font-mono text-sm text-cyan-trace">{{ post.title }}</span>
      <span class="hidden sm:inline text-sm text-slate-mutext truncate">{{ post.description }}</span>
      <span class="ml-auto font-mono text-[0.68rem] uppercase text-phosphor whitespace-nowrap" data-solved-badge></span>
    </a>
    {% endfor %}
  </div>
</section>
