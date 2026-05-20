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

1. Start with the known invalid token: `token-beta`.
2. The crashed process must be the one using `token-beta`.
3. The `renderer` was not using `token-beta`.
4. The `parser` was not using `token-alpha`.
5. Since `/models` used `token-gamma`, that leaves `token-beta` for another
resource.
6. `crawler` was accessing `/cache`.
7. The crash did not happen in `/logs`.
8. Therefore, the crash happened while accessing `/cache`.
9. Since `crawler` accessed `/cache`, and `token-beta` was invalid, the answer
is:

``` crawler + token-beta + /cache ```

## Solution

```crawler, token-beta, /cache ```
