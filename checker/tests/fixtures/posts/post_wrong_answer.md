---
title: FX Fixture
permalink: /puzzles/post_wrong_answer.html
---

{% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. `p1` ran with `t1`.
2. `p2` ran with `t2`.
3. `p1` touched `r1`.
4. `p2` touched `r2`.

{% include panel_end.html %}

{% include zebra-table.html cols_a="p1|p2|p3" cols_b="t1|t2|t3" rows_a="r1|r2|r3" rows_b="t1|t2|t3" %}

<div data-puzzle-answer="p3, t2, r2">
<select data-answer-dim="0">
  <option value="">— proc —</option>
  <option value="p1">p1</option>
  <option value="p2">p2</option>
  <option value="p3">p3</option>
</select>
<select data-answer-dim="1">
  <option value="">— tok —</option>
  <option value="t1">t1</option>
  <option value="t2">t2</option>
  <option value="t3">t3</option>
</select>
<select data-answer-dim="2">
  <option value="">— res —</option>
  <option value="r1">r1</option>
  <option value="r2">r2</option>
  <option value="r3">r3</option>
</select>
<button data-fake-action="SUBMIT">SUBMIT</button>
</div>
