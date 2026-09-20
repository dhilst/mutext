---
title: INC-0007 Priority Inversion
description: The release gate waits on the garbage collector, and the garbage collector never gets to run.
permalink: /puzzles/007-priority-inversion.html
---

{% include lore-block.html chapter="07" label="the gate" %}

The release had been two hours from shipping for two hours.

```
[ALERT] INC-0007 — Release gate blocked, no progress 2h11m
[INFO ] gate task priority: P0
[INFO ] gate task state: BLOCKED on m-db
[INFO ] m-db holder: running
[INFO ] m-db holder: preempted
[INFO ] m-db holder: running
[INFO ] m-db holder: preempted
[WARN ] m-db held 2h11m, longest hold in 90d: 40ms
```

Nothing was deadlocked. The holder of `m-db` was alive and scheduled and making
forward progress in slices too short to finish anything.

Bob read the log over Andy's shoulder for about four seconds.

"Your highest-priority task is waiting on your lowest-priority task."

"That's backwards."

"That's the name." He pulled up a chair, which meant this was going to take a
while. "P0 needs the lock. Something small and unimportant has it. And something
in the middle — busy, harmless, correctly configured — keeps knocking the small
thing off the CPU before it can let go. Every one of the three is behaving
exactly as designed."

Andy looked at the task table. Four tasks, four priorities, four mutexes, and one
line in the incident header telling him where the wait edge pointed.

"So I find who holds `m-db`."

"And what priority they're at," Bob said. "That's the part you're going to want
to write down."

{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}

    {% include panel.html title="evidence" pill="retained" pill_tone="amber" markdown=true %}

1. The task running at `P1` holds `m-tmp`.
2. `m-log` is not held by the `P0` task.
3. `t-render` holds `m-io`.
4. `t-audit` does not run at `P3`.
5. Whatever holds `m-log`, it is not running at `P3`.
6. `t-billing` runs at `P1`.
7. The `P0` task does not hold `m-db` — it is waiting on it.

    {% include panel_end.html %}

    {% include panel.html title="messages" subtitle="bob" raw=true %}
<div class="max-h-80 overflow-y-auto">
  {% include chat-message.html sender="Bob" time="16:40" message="Four of everything now. The board is bigger but the rules haven't changed: one priority and one mutex per task." %}
  {% include chat-message.html sender="Bob" time="16:41" message="Left columns are tasks and priorities. Rows are mutexes and priorities." %}
  {% include chat-message.html sender="Bob" time="16:43" message="The header already tells you the gate is blocked on m-db. So the answer is whoever is holding it." %}
  {% include chat-message.html sender="Bob" time="16:44" message="Format: task, priority, holds." %}
</div>
    {% include panel_end.html raw=true %}

  {% include puzzle-col_end.html %}

  {% include puzzle-col.html %}

    {% include panel.html title="table" subtitle="scheduler classes" subtitle_class="text-slate-mutext" class="min-w-0 overflow-hidden" raw=true %}

<div class="border-b border-slate-700/70 bg-slate-950/45 p-4">
  <div class="grid gap-3 md:grid-cols-3">
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">fault</p>
      <p class="mt-1 text-sm text-white">Release gate blocked</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">wait edge</p>
      <p class="mt-1 text-sm text-white">P0 &rarr; m-db</p>
    </div>
    <div>
      <p class="font-mono text-xs uppercase text-slate-mutext">severity</p>
      <p class="mt-1 text-sm text-red-fault">SEV-1</p>
    </div>
  </div>
</div>

{% include zebra-table.html cols_a="t-audit|t-render|t-billing|t-gc" cols_b="P0|P1|P2|P3" rows_a="m-io|m-db|m-log|m-tmp" rows_b="P0|P1|P2|P3" %}

    {% include panel_end.html raw=true %}

    {% include panel.html title="answer input" subtitle="incident response" markdown=true %}

**Question:** Which task holds the mutex the release gate is waiting on — task, priority, and the mutex it holds?

<div data-puzzle-answer="t-gc, P3, m-db">
<label class="block font-mono text-xs uppercase text-slate-mutext mb-3">operator answer</label>
<div class="flex flex-wrap items-center gap-3">
  <select data-answer-dim="0" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— task —</option>
    <option value="t-audit">t-audit</option>
    <option value="t-render">t-render</option>
    <option value="t-billing">t-billing</option>
    <option value="t-gc">t-gc</option>
  </select>
  <select data-answer-dim="1" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— priority —</option>
    <option value="P0">P0</option>
    <option value="P1">P1</option>
    <option value="P2">P2</option>
    <option value="P3">P3</option>
  </select>
  <select data-answer-dim="2" class="bg-slate-950/70 border border-slate-700/80 text-sm text-slate-100 font-mono px-3 py-2 outline-none focus:border-cyan-trace">
    <option value="">— holds —</option>
    <option value="m-io">m-io</option>
    <option value="m-db">m-db</option>
    <option value="m-log">m-log</option>
    <option value="m-tmp">m-tmp</option>
  </select>
  <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
</div>
</div>

    {% include panel_end.html %}

  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
{% include lore-block.html chapter="07" label="after the inversion" %}

`t-gc` — the garbage collector, the least important thing in the system — held
`m-db` at `P3`.

`t-render`, the release gate, sat at `P0` and waited for it.

And `t-billing` at `P1`, doing ordinary invoice work, became runnable roughly
every eleven milliseconds and preempted `t-gc` each time. The collector got its
slice back, did four microseconds of work, and lost the CPU again.

The highest-priority task in the system was, in practice, running at the priority
of the lowest.

{% include lore-block_end.html %}

{% capture inversion_timeline %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  P0  t-render   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  blocked on m-db
  P1  t-billing  ██░░██░░██░░██░░██░░██░░██░░██░░  runnable, preempts
  P2  t-audit    ░░██░░░░░░██░░░░░░██░░░░░░██░░░░
  P3  t-gc       ░░░░█░░░░░░░█░░░░░░░█░░░░░░░█░░░  holds m-db

                 └── 4µs slices, never reaches release ──┘

  ► m-db acquired  14:29:06.118   by t-gc (P3)
  ► m-db released  —
  ► t-render waiting 2h11m at P0
  ► no priority inheritance configured on m-db
</pre>
{% endcapture %}
{% include terminal-window.html title="sched-timeline — INC-0007" content=inversion_timeline %}

{% include lore-block.html chapter="07" label="loose thread" %}

The fix was a scheduler flag nobody had needed before: let the holder inherit the
waiter's priority until it lets go. Ten minutes of work.

Andy spent the rest of the afternoon on the part that was not the fix, which was
why `t-gc` had been at `P3` at all. It had shipped at `P1`. Somebody had moved it.

{% include lore-block_end.html %}

{% capture blame %}
<pre class="font-mono text-xs leading-6 text-cyan-trace whitespace-pre">
  $ git log --show-signature -1 sched/classes.yaml

  commit  7c41ae0  sched: lower t-gc to P3 to reduce db contention
  Date:   96 days after last recorded activity for this key
  gpg:    Good signature from "{{ site.data.evidence.rin_key_ch4.fragment }}"
  gpg:    Primary key fingerprint: 4F19 8A2C 77D0 …
  Reviewed-by: —
  ────────────────────────────────────────────────────────────
  ► signature verified
  ► author not found in directory
</pre>
{% endcapture %}
{% include terminal-window.html title="git — sched/classes.yaml" content=blame %}

{% include lore-block.html chapter="07" label="the obvious thing" %}

Andy wrote it in his notes the way he would have written it in a postmortem,
because it was not a suspicion, it was just true:

```
a good signature proves someone had the key
it does not prove someone was there
```

Rin's key had signed a one-line change to a scheduler class three months after
Rin stopped existing as far as the company was concerned. The commit was correct.
The signature was correct. The change was even defensible — `t-gc` really was
hammering the database.

He asked Bob whether offboarding revoked keys.

Bob said offboarding was a form, and forms were filled in by people, and then he
went to get more coffee and did not come back.

{% include lore-block_end.html %}

<div class="flex justify-center pt-2">
  <a class="button-primary" href="{{ '/puzzles/008-split-brain.html' | relative_url }}">NEXT INCIDENT &rarr;</a>
</div>
</section>
