# Architecture

- `index.html`: semantic page, catalog container, native modal dialog.
- `css/style.css`: shared responsive design, reduced-motion support.
- `js/i18n.js`: complete `ru`, `kk`, `en` dictionaries. Only the trusted headline translation contains HTML; user search is never inserted into markup.
- `js/catalog.js`: game registry and decorative artwork.
- `js/app.js`: locale persistence (with unavailable-storage fallback), category/search state, modal lifecycle and lazy loading.
- `js/games.js`: independent Snake, Memory and two-player Tic-tac-toe implementations.

## Game adapter

A registry entry has `{ id, category, runtime, art, load }`. `load()` returns a Promise of a mount function. `mount({ stage, status, directionPad, t })` renders the game and returns a synchronous cleanup function. Cleanup must remove external event listeners, timers, audio and workers. Restart calls cleanup before mounting again. A generation counter discards outdated async loads after close/restart.

For a Python browser build, add an adapter that mounts a titled iframe in `stage` pointing to its generated `index.html`. Use the minimum sandbox permissions compatible with that build, do not grant top-level navigation or camera/microphone by default, and remove the iframe during cleanup. Define and validate a `postMessage` protocol if reporting score/readiness across frames. Do not inject untrusted build HTML into the parent document. Add a visible loading/error state and retry action in the adapter. A generic iframe is not proof that an arbitrary Pygame project is browser-compatible.

## State and deployment

Only locale is persisted in localStorage. Game state is in memory; restarting or closing resets it. No accounts, backend, analytics or credentials are required. Serve static assets through HTTP(S); ES modules are not supported through `file://`. Deploy the repository root to GitHub Pages or another static host. Relative imports support a project subpath. The optional Google Fonts stylesheet falls back to local fonts offline. Add server-side persistence/authentication in a separate service if required later; never put secrets in client JavaScript.
