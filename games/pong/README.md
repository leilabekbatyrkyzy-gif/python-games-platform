# AI Pong Master

Browser adaptation of the uploaded `source/pong.py`, preserved byte-for-byte.
Open `index.html` through the platform HTTP server. No third-party runtime or camera access required.

Mouse, touch, arrow keys or W/S control the left paddle against an AI opponent. Pause/resume, local best score and speed milestones every 5 points are supported. Web Audio generates effects because the original WAV files were not supplied. The browser version does not implement MediaPipe hand tracking or fist power shots; use the desktop source for those features. This is an adaptation, not direct Python execution.

Desktop dependencies: OpenCV, MediaPipe (a version supporting `mp.solutions.hands`), NumPy and Pygame, plus a GUI/audio-capable machine and optionally a webcam. The original source is preserved; desktop execution was not tested in the cloud environment.
