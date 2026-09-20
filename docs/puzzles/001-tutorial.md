# Puzzle 1: Tutorial

## Lore Start

After solving 32 logic challenges and inverting 1024 linked lists, Andy finally
reached the final interview step.

The meeting room was empty except for a terminal, a whiteboard, and Bob.

Bob did not look up from his coffee.

“Andy, right?”

Andy nodded.

Bob pointed at the terminal.

“Good. One of our generated systems crashed last night. Three processes were
running, three access tokens were active, and three resources were being
touched. One process crashed while accessing one resource with an invalid
token.”

Andy frowned. “So this is debugging?”

Bob smiled.

“No. This is troubleshooting.”

He tapped the whiteboard.

“Find the what process crashed. Then input into the system in the format
process, token, resource”

## Tutorial Goal

Teach the player how to solve a μ-text puzzle.

The answer is a 3-part tuple:

```txt Process + Token + Resource ````

Example:

```txt crawler + token-beta + /cache ```

(the shape of an answer, not this puzzle's answer)

## Puzzle Entities

### Processes

* `parser`
* `crawler`
* `renderer`

### Tokens

* `token-alpha`
* `token-beta`
* `token-gamma`

### Resources

* `/cache`
* `/logs`
* `/models`

## Clues

1. The `parser` was not using `token-alpha`.
2. The process accessing `/models` was using `token-gamma`.
3. The `crawler` was accessing `/cache`.
4. The crash did not happen in `/logs`.
5. `token-beta` was invalid.
6. The `renderer` was not using `token-beta`.

## Tutorial Explanation

Bob explains:

1. `crawler` was accessing `/cache` (clue 3), and the process on `/cache` was
using `token-gamma` (clue 2). So `crawler` holds `token-gamma`.
2. The process using `token-alpha` was accessing `/logs` (clue 4). That cannot
be `crawler`, and it cannot be `parser` (clue 1). So `renderer` holds
`token-alpha` and is on `/logs`.
3. That leaves `parser` with `token-beta`, on `/models` — the only resource
left. Clue 6 agrees: `renderer` was not using `token-beta`.
4. `token-beta` was invalid (clue 5), so the crash is the `parser`'s.

``` parser + token-beta + /models ```

## Solution

```parser, token-beta, /models ```

## Checker

`checker/puzzles/001-tutorial.yaml`. Clues 1 and 6 are marked `keep_redundant`:
they are implied by the rest, and are kept because this is the chapter that
teaches elimination. Clue 5 is `narrative_only` — it names the answer row rather
than constraining the grid.
