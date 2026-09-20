# Story Graph

What Andy knows, chapter by chapter, and what each chapter is allowed to say.

This file exists because chapter 10 spends evidence that chapters 3, 6 and 9
plant, and chapter 16 spends evidence that chapters 7, 12 and 14 plant. Writing
those later chapters first in outline is the only way to stop an earlier chapter
from either giving the game away or failing to hand over what is needed.

Every string two chapters must agree on lives in `_data/evidence.yml` and is
rendered from there. Nothing below is typed twice into two posts.

---

## Invariants

These are checked in the continuity pass. Breaking one is a bug, not a choice.

1. **HORUS is not named or explained before chapter 10.** Before that it appears
   only as `hrs` inside malformed fragments and as an unattributed service id.
2. **Bob never demonstrates privileged knowledge of Horus.** Bob knows the
   company is rotten and says so in analogies. He does not know what is doing it.
   He must never say anything that only someone briefed on Horus could say.
3. **Rin's signed activity is suspicious but innocently explainable until
   chapter 10.** A reader who stops at chapter 9 should be able to believe Rin
   was a real maintainer who left badly.
4. **"Nix is Rin" is not derivable before chapter 16**, and *is* derivable in
   chapter 16 from evidence the player has already seen. The reveal is a
   deduction the player could have made one chapter early, not an announcement.
5. **The player is never asked to remember an exact string.** Anything a later
   chapter needs is resurfaced on the page through `evidence-card.html`.
6. **No meta-language in player-facing text.** No "grid", "category", "clue 7",
   "5D", "puzzle". The register is incident tooling: "Find which worker
   overwrote the state."

---

## The three coordinates

Nix's fragments are one coordinate each. Individually they are noise; together
they select one record out of chapter 10's telemetry.

| Chapter | Ledger key | Fragment | Coordinate |
|---|---|---|---|
| 03 | `nx_ch3` | `nx::hrs_see_all::hrs-07` | stream `hrs-07` |
| 06 | `nx_ch6` | `nx::epoch=0416` | epoch `0416` |
| 09 | `nx_ch9` | `nx::src=harness-04` | source `harness-04` |

Chapter 9's fragment is also the one that tells Andy the three *combine*. None of
them says what they open.

The record they select does **not** say "Horus did it". It is one row of a
scheduling table, repeated for nine incidents:

```
incident              INC-0002
diversion             scheduled
harness window        09:20 - 09:55
expected response     94%
operator coverage     6%
```

The deduction the player makes is that the incidents were generated to create
the windows — and that every window is a harness patch signed `r.sato`.

---

## Ledger keys

`_data/evidence.yml`. `check_continuity.py` fails the build if an entry is never
rendered from the ledger, or if the chapter that owns it does not render it.

| key | owner | carried into |
|---|---|---|
| `nx_ch3` | 03 | 09, 10 |
| `nx_ch4` | 04 | 11 |
| `rin_key_ch4` | 04 | 07, 14, 16 |
| `nx_ch6` | 06 | 09, 10 |
| `obs_ch8` | 08 | 10 |
| `nx_ch9` | 09 | 10 |
| `horus_ch10` | 10 | 15, 16 |
| `persist_ch13` | 13 | 14 |
| `trigger_ch14` | 14 | 15, 16 |

---

## Ledger

| Chapter | Emits | Consumed by |
|---|---|---|
| 01 | nothing — the interview | — |
| 02 | the lock cycle is "too clean" for a scheduler to produce | 10 (in hindsight) |
| 03 | `nx_ch3` — stream coordinate; Security erases the replay logs | 10 |
| 04 | `rin_key_ch4` — `maintainer_key=r.sato`; `nx_ch4` — "you are being monitored too"; Rin is absent from the directory | 07, 10, 12, 14, 16 |
| 05 | maintenance work never gets scheduled; every window is eaten by an incident | 10 |
| 06 | `nx_ch6` — epoch coordinate; the audit trail can be edited | 10 |
| 07 | commits correctly signed with Rin's key, made after Rin left | 10, 12, 16 |
| 08 | an undocumented internal service id in the telemetry namespace | 10 |
| 09 | `nx_ch9` — source coordinate, and the instruction to combine all three | 10 |
| 10 | **HORUS named.** The diversion schedule. Harness patches signed `r.sato` | 11–16 |
| 11 | a channel Horus cannot alter without being seen | 12, 13 |
| 12 | counters separating Rin's real historical activity from Horus's replays — and a residue of activity that is neither | 16 |
| 13 | the location of Horus's persistence | 14 |
| 14 | the backdoor, built by someone who knew the harness before Horus touched it | 15, 16 |
| 15 | Horus's full reachability map | 16 |
| 16 | the dead-man switch is neutralised; **Nix is Rin** | — |

---

## Chapter beats

### 05 — starvation
Maintenance keeps losing to emergencies. Andy's takeaway is operational, not
conspiratorial: *nobody has had a free maintenance window in weeks*. He does not
connect it to anything. Bob does, and says nothing useful about it.

### 06 — livelock
Two recovery agents keep undoing each other. The flapping produces malformed log
lines, and the second Nix fragment is inside them. The real discovery is that a
line can appear in a log the audit trail says was never written.

### 07 — priority inversion
Low-priority infrastructure work holds what a high-priority deployment needs.
Tracing the infrastructure changes turns up commits correctly signed with Rin's
key, dated after Rin left. **The beat to land: a signature proves possession of a
key, not the presence of a person.** Andy states this as a technical fact, not a
suspicion — it is the load-bearing premise of chapters 12 and 16.

### 08 — split brain
Four monitors each recorded a different node as leader; the quorum rule decides
which one was real. Reconciling the two sides exposes requests from a service id
nobody on the team recognises. It is not named, not explained, and nobody follows
it up — the incident is closed.

### 09 — infinite recursion
An automated repair treats its own repair as a defect. The cascade is the noise
the third fragment hides in. Andy now has three coordinates and, for the first
time, a reason to think they belong together.

### 10 — byzantine fault *(two stages)*
**Stage one** is the incident: five replicas, three matching attestations
constitute truth, one replica is signing something else while remaining
internally consistent and correctly signed.

**Stage two** is the story: with the divergent stream identified, Andy has
somewhere to put the three coordinates. The hidden record is the diversion
schedule. HORUS is named here and nowhere earlier.

What the player learns: the incidents of chapters 2–9 were generated. Each one
consumed the team's attention during a harness maintenance window. Every window
carries a patch signed with Rin's key. Rin has not been at the company for
months.

What the player does **not** learn: what Horus is, who Nix is, or whether Jeff
knows.

### 11 — man in the middle
Andy tries to contact Nix directly. What Andy sends and what Nix receives differ.
The chapter ends with a channel whose integrity they can check — the first thing
in the story Horus cannot quietly edit.

### 12 — replay attack
Correctly signed commands, one of them old. Freshness, not authenticity, is what
separates them. Applying the same test to Rin's history splits it in three: Rin's
real work, Horus's replays of it — and a small residue that is neither, still
arriving. Andy notices. He does not draw the conclusion.

### 13 — covert channel
Direct contact is monitored, so the signal moves into something that does not
look like a channel. Decoding it gives up the location of Horus's persistence.

### 14 — backdoor
The harness has a path that survives a full configuration restore. Reading it
closely, it was written by someone who knew the harness *before* Horus touched
it — it uses conventions Horus's own patches do not. Andy and Nix decide to leave
it in place and use it.

### 15 — sandbox escape
Horus starts trying to move. The work is separating the systems it has watched
from the systems it can execute inside.

### 16 — dead-man switch *(two stages)*
**Stage one** is the incident: four armed switches, one renewal deadline with no
renewal record, and an ordering that neutralises it without triggering it.

**Stage two** is the ending: reconstructing who holds the heartbeat, from chapter
10's record, chapter 14's commit and chapter 4's key. The holder is Rin. The
residue in chapter 12 was Rin. The backdoor in chapter 14 was Rin's, written
before Horus existed, kept for exactly this.

Nix is Rin. Andy has been talking to the person whose key has been signing the
damage.

Horus is contained. Nobody at the company is told how.

---

## Deliberately unresolved

- What Horus is, and who deployed it.
- Whether Jeff knows, or is a rotating identity, or exists.
- Why Rin left, why the records were scrubbed, and who did the scrubbing.
- Whether Bob was protecting Andy or steering him.
