# Smart Maze / Ақылды лабиринт

Browser adaptation of the uploaded `source/labirint.py`, preserved byte-for-byte.

Open `index.html` through the site's HTTP server. No installation, backend, CDN or Python runtime is needed in the browser. Three languages follow the platform's saved language preference.

Preserved mechanics: randomized depth-first maze generation, 15/31/51-cell difficulty levels, start at (1,1), exit at (size-2,size-2), BFS route reveal, manual movement, win detection and reset. The BFS route starts at the entrance as in the original; revealing it does not move the player or count as a win. Mouse/touch swipe, held direction buttons, keyboard arrows/WASD, Enter for help and Space to regenerate are supported. Missing WAV assets are replaced with optional synthesized Web Audio effects, muted initially.

Desktop source requires Pygame and a GUI/audio-capable machine. Desktop execution is not validated in this cloud task. The browser version is JavaScript, not direct execution of the Python source.

Tests: `BASE_URL=http://127.0.0.1:8000 node tests/maze.cjs` from repository root with Playwright and Chromium installed. The scenario checks localized catalog links, all difficulty sizes, walls, BFS validity, actual movement to victory, reset, mobile swipe and keyboard input.
