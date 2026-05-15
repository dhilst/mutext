# μ-text Agent Notes

## Project

Static Jekyll prototype for the μ-text narrative troubleshooting simulator.

## Toolchain

- Jekyll runs from the vendored bundle path.
- Tailwind is built with the local npm dependency.
- No backend, authentication, persistence, payments, ranking, or real puzzle solver should be added in this prototype phase.

## Commands

Use the vendored Ruby executables and gem home first:

```bash
export GEM_HOME="vendor/bundle/ruby/3.4.0"
export GEM_PATH="vendor/bundle/ruby/3.4.0"
export PATH="vendor/bundle/ruby/3.4.0/bin:$PATH"
```

Build:

```bash
npm run build
```

Serve locally:

```bash
npm run serve
```

The default local URL is:

```text
http://127.0.0.1:4000/
```

## Important Files

- `_config.yml` configures Jekyll and no-theme output.
- `_layouts/default.html` contains the global shell UI.
- `_includes/` contains reusable static UI components.
- `index.md` is the landing console.
- `_posts/` is the location for post content and puzzle content. Keep posts and puzzles there.
- `_posts/2026-05-15-tutorial.md` is the tutorial incident screen. Jekyll publishes it at `/puzzles/tutorial.html`.
- `_lore/` contains static lore collection pages.
- `assets/css/main.css` is the Tailwind input file.
- `assets/css/site.css` is the compiled stylesheet.
- `assets/js/main.js` contains vanilla JS placeholder interactions.

## Design Direction

Keep the interface close to internal corporate tooling, retro terminal systems, incident dashboards, and restrained cyberpunk engineering environments. Favor clear dense UI, subtle motion, dark terminal colors, dry incident copy, and atmospheric story presentation.

## Narrative Boundary

DO NOT BREAK THE NARRATIVE INSIDE THE GAME.

Visible game UI must stay in-world. Do not put implementation notes, design guidance, style instructions, or meta-language such as "the UI should feel..." into pages, panels, tooltips, logs, chat, lore, or any other user-facing game content. Keep that guidance in `AGENTS.md`, code comments when truly necessary, issues, or development docs only.

## Puzzle Structure

Puzzle pages should use readable Markdown where practical and follow the same player-facing structure:

1. Email with an introduction to the problem.
2. Clues.
3. Table.
4. Answer input.
