# Rock, Paper, Scissors / Тас, қағаз, қайшы

Browser adaptation of the uploaded `source/tas_kagaz_kaiwy.py`, preserved byte-for-byte. Runs as static HTML/CSS/JavaScript with no external libraries or camera access. The desktop source needs Pygame, OpenCV, MediaPipe and NumPy; its camera-vs-AI and camera-vs-friend modes are not included in this browser adaptation. Desktop execution is untested here.

The original RPS_AI logic is preserved: the AI learns the player's next move following their previous two moves and counters the most frequent prediction; unknown patterns choose randomly. Ties follow rock/paper/scissors insertion order. The AI commits its move before learning the current player's choice. The UI provides custom SVG hand illustrations, a short reveal animation, scores, last five rounds and Kazakh/Russian/English text. Keys 1/2/3 or touch/mouse choose a move. Reset cancels any pending reveal and clears scores and AI memory. State lasts for the current page session.

Run `BASE_URL=http://127.0.0.1:8000 node tests/rps.cjs` from the repository root with Playwright and Chromium installed.
