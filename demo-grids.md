---
title: Grid Demo
permalink: /demo-grids.html
---

<h2 class="text-lg font-mono text-cyan-trace mb-4">3 dimensions — 6×6 grid (3 active blocks)</h2>

<div class="shell-panel mb-8">
  <div class="panel-header">
    <span>3 categories × 3 items</span>
  </div>
{% include zebra-table.html cols_a="P1|P2|P3" cols_b="→P1|→P2|→P3" rows_a="L1|L2|L3" rows_b="→P1|→P2|→P3" %}

<div class="border-t border-slate-700/70 p-4" data-puzzle-answer="P2, L1, →P3">
  <p class="font-mono text-xs uppercase text-slate-mutext mb-2">answer — 3 selects</p>
  <p class="font-mono text-xs text-amber-warn mb-3">expected: P2, L1, →P3</p>
  <div class="flex flex-wrap items-center gap-3">
    <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— process —</option>
      <option value="P1">P1</option>
      <option value="P2">P2</option>
      <option value="P3">P3</option>
    </select>
    <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— lock —</option>
      <option value="L1">L1</option>
      <option value="L2">L2</option>
      <option value="L3">L3</option>
    </select>
    <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— call target —</option>
      <option value="→P1">→P1</option>
      <option value="→P2">→P2</option>
      <option value="→P3">→P3</option>
    </select>
    <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
  </div>
</div>
</div>

<h2 class="text-lg font-mono text-cyan-trace mb-4">4 dimensions — 12×12 grid (6 active blocks)</h2>

<div class="shell-panel mb-8">
  <div class="panel-header">
    <span>4 categories × 4 items</span>
  </div>
{% include zebra-table.html cols_a="proc-A|proc-B|proc-C|proc-D" cols_b="tok-1|tok-2|tok-3|tok-4" cols_c="res-W|res-X|res-Y|res-Z" rows_a="tok-1|tok-2|tok-3|tok-4" rows_b="res-W|res-X|res-Y|res-Z" rows_c="host-α|host-β|host-γ|host-δ" %}

<div class="border-t border-slate-700/70 p-4" data-puzzle-answer="proc-B, tok-3, res-X, host-γ">
  <p class="font-mono text-xs uppercase text-slate-mutext mb-2">answer — 4 selects</p>
  <p class="font-mono text-xs text-amber-warn mb-3">expected: proc-B, tok-3, res-X, host-γ</p>
  <div class="flex flex-wrap items-center gap-3">
    <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— process —</option>
      <option value="proc-A">proc-A</option>
      <option value="proc-B">proc-B</option>
      <option value="proc-C">proc-C</option>
      <option value="proc-D">proc-D</option>
    </select>
    <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— token —</option>
      <option value="tok-1">tok-1</option>
      <option value="tok-2">tok-2</option>
      <option value="tok-3">tok-3</option>
      <option value="tok-4">tok-4</option>
    </select>
    <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— resource —</option>
      <option value="res-W">res-W</option>
      <option value="res-X">res-X</option>
      <option value="res-Y">res-Y</option>
      <option value="res-Z">res-Z</option>
    </select>
    <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— host —</option>
      <option value="host-α">host-α</option>
      <option value="host-β">host-β</option>
      <option value="host-γ">host-γ</option>
      <option value="host-δ">host-δ</option>
    </select>
    <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
  </div>
</div>
</div>

<h2 class="text-lg font-mono text-cyan-trace mb-4">5 dimensions — 20×20 grid (10 active blocks)</h2>

<div class="shell-panel">
  <div class="panel-header">
    <span>5 categories × 5 items</span>
  </div>
{% include zebra-table.html cols_a="◆1|◆2|◆3|◆4|◆5" cols_b="▲a|▲b|▲c|▲d|▲e" cols_c="●α|●β|●γ|●δ|●ε" cols_d="■Ⅰ|■Ⅱ|■Ⅲ|■Ⅳ|■Ⅴ" rows_a="▲a|▲b|▲c|▲d|▲e" rows_b="●α|●β|●γ|●δ|●ε" rows_c="■Ⅰ|■Ⅱ|■Ⅲ|■Ⅳ|■Ⅴ" rows_d="✦1|✦2|✦3|✦4|✦5" %}

<div class="border-t border-slate-700/70 p-4" data-puzzle-answer="◆3, ▲b, ●δ, ■Ⅱ, ✦4">
  <p class="font-mono text-xs uppercase text-slate-mutext mb-2">answer — 5 selects</p>
  <p class="font-mono text-xs text-amber-warn mb-3">expected: ◆3, ▲b, ●δ, ■Ⅱ, ✦4</p>
  <div class="flex flex-wrap items-center gap-3">
    <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— ◆ —</option>
      <option value="◆1">◆1</option>
      <option value="◆2">◆2</option>
      <option value="◆3">◆3</option>
      <option value="◆4">◆4</option>
      <option value="◆5">◆5</option>
    </select>
    <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— ▲ —</option>
      <option value="▲a">▲a</option>
      <option value="▲b">▲b</option>
      <option value="▲c">▲c</option>
      <option value="▲d">▲d</option>
      <option value="▲e">▲e</option>
    </select>
    <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— ● —</option>
      <option value="●α">●α</option>
      <option value="●β">●β</option>
      <option value="●γ">●γ</option>
      <option value="●δ">●δ</option>
      <option value="●ε">●ε</option>
    </select>
    <select data-answer-dim="3" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— ■ —</option>
      <option value="■Ⅰ">■Ⅰ</option>
      <option value="■Ⅱ">■Ⅱ</option>
      <option value="■Ⅲ">■Ⅲ</option>
      <option value="■Ⅳ">■Ⅳ</option>
      <option value="■Ⅴ">■Ⅴ</option>
    </select>
    <select data-answer-dim="4" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
      <option value="">— ✦ —</option>
      <option value="✦1">✦1</option>
      <option value="✦2">✦2</option>
      <option value="✦3">✦3</option>
      <option value="✦4">✦4</option>
      <option value="✦5">✦5</option>
    </select>
    <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
  </div>
</div>
</div>
