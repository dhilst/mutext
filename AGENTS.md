# μ-text Agent Notes

## Project

Static Jekyll prototype for the μ-text narrative troubleshooting simulator.

## Toolchain

- Jekyll runs from the vendored bundle path.
- Tailwind is built with the local npm dependency.
- The puzzle checker under `checker/` is an offline authoring tool (Python + Z3, run with `uv`). It never ships to the site.
- No backend, authentication, persistence, payments, or ranking should be added in this prototype phase. Nothing in the shipped site may depend on the checker.

## Commands

Use the vendored Ruby executables and gem home first:

```bash
export GEM_HOME="vendor/bundle/ruby/3.4.0"
export GEM_PATH="vendor/bundle/ruby/3.4.0"
export PATH="vendor/bundle/ruby/3.4.0/bin:$PATH"
```

Serve locally (for development):

```bash
npm run serve
```

The default local URL is:

```text
http://127.0.0.1:4000/
```

Verify the puzzles (what CI runs, and what must pass before any chapter ships):

```bash
npm run check          # puzzles (strict) + continuity + unit tests
```

Production build (for GitHub Pages only):

```bash
npm run build
```

### baseurl caveat

`_config.yml` has `baseurl: "/mutext"` for the GitHub Pages deploy at `https://dhilst.github.io/mutext/`. The `npm run serve` command overrides this with `--baseurl ''` so assets resolve correctly on localhost.

**Do NOT run `npm run build` while `npm run serve` is running.** It overwrites `_site/` with production paths (`/mutext/...`) and breaks the local server. If you need to rebuild Tailwind while serving, restart the serve command instead.

## Important Files

- `_config.yml` configures Jekyll and no-theme output.
- `_layouts/default.html` contains the global shell UI.
- `_includes/` contains reusable static UI components.
- `index.md` is the landing console.
- `_posts/` is the location for post content and puzzle content. Keep posts and puzzles there.
- `_posts/2026-05-15-tutorial.md` is the tutorial incident screen. Jekyll publishes it at `/puzzles/001-tutorial.html`.
- `_lore/` contains static lore collection pages.
- `assets/css/main.css` is the Tailwind input file.
- `assets/css/site.css` is the compiled stylesheet.
- `assets/js/main.js` contains vanilla JS placeholder interactions.
- `_data/evidence.yml` is the cross-chapter evidence ledger. Any string two chapters must agree on lives there and is rendered from there — never typed into two posts.
- `_includes/evidence-card.html` renders a ledger entry.
- `checker/puzzles/NNN-slug.yaml` is the solver input paired with each post; the checker fails the build if the two disagree.
- `docs/` and `checker/` are excluded from the build. Keep solutions and design notes there.

## Design Direction

Keep the interface close to internal corporate tooling, retro terminal systems, incident dashboards, and restrained cyberpunk engineering environments. Favor clear dense UI, subtle motion, dark terminal colors, dry incident copy, and atmospheric story presentation.

## Narrative Boundary

DO NOT BREAK THE NARRATIVE INSIDE THE GAME.

Visible game UI must stay in-world. Do not put implementation notes, design guidance, style instructions, or meta-language such as "the UI should feel..." into pages, panels, tooltips, logs, chat, lore, or any other user-facing game content. Keep that guidance in `AGENTS.md`, code comments when truly necessary, issues, or development docs only.

## Puzzle Structure

Check docs/puzzle-spec.md for the grid, the page layout and the authoring order.
Check docs/sat-checker.md for the checker, the clue grammar and the clue-quality rules.

Two rules worth knowing before touching a grid:

- Row groups are listed in **reverse** category order (`cols = G1..G(D-1)`, `rows = GD..G2`). Listing them forward puts a category against itself and leaves pairs uncrossed.
- Never change a shipped grid's shape — grid marks are a positional array in localStorage keyed by pathname.

## Characters

Check docs/characters.md

## Continuity

Check docs/story-graph.md before writing any chapter. It records what Andy knows
at each point, which chapter plants what, and the invariants (Horus is unnamed
before chapter 10; "Nix is Rin" is not derivable before chapter 16).

## Git

Do not add Co-Authored-By lines to commits.
Always use `--no-gpg-sign` when committing.
