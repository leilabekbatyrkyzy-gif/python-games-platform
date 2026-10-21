# Python/Pygame browser builds

Place each future game in its own directory, for example `games/python/my-game/`.
Keep Python sources alongside a documented build process; publish generated browser assets under `games/web/my-game/`.

Pygame scripts do not run directly in an HTML page. A possible toolchain is [pygbag](https://pygame-web.github.io/): adapt the main loop to async, yield with `await asyncio.sleep(0)`, use relative asset paths and replace unsupported filesystem/network integrations. Pin the selected toolchain and dependencies for each game; this platform does not install a speculative Python runtime.

After a successful browser build, register the game in `js/catalog.js`, add names/descriptions/help in every locale in `js/i18n.js`, and provide a lazy loader conforming to `docs/architecture.md`. Test keyboard and touch input, loading failures, mobile performance and runtime cleanup. Check the runtime's CDN requirements before deploying under a restrictive content security policy. Python builds and their runtime downloads are not included in the current platform.
