import pygame
import random
import time
import os
from collections import deque

# Түстер палитрасы
WHITE = (255, 255, 255)
BLACK = (15, 23, 42)
BLUE = (59, 130, 246)
RED = (239, 68, 68)
GREEN = (34, 197, 94)
GRAY = (30, 41, 59)
GOLD = (255, 215, 0)
PLAYER_COLOR = (34, 211, 238) 
BUTTON_COLOR = (71, 85, 105)
BUTTON_HOVER = (94, 114, 143)
ACTIVE_COLOR = (30, 64, 175)

# Бастапқы баптаулар
WINDOW_HEIGHT = 650
MAZE_AREA = 620
SIDE_PANEL_WIDTH = 240
WIDTH = MAZE_AREA + SIDE_PANEL_WIDTH
HEIGHT = WINDOW_HEIGHT

class MazeApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ақылды лабиринт 3.1 - Arrows & Swipe")
        self.clock = pygame.time.Clock()
        
        # Қаріптер
        self.font_small = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_mid = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_big = pygame.font.SysFont("Arial", 22, bold=True)
        
        # Деңгей баптаулары
        self.difficulties = {
            "Оңай": 15,
            "Орташа": 31,
            "Қиын": 51
        }
        self.current_diff = "Орташа"
        self.grid_size = self.difficulties[self.current_diff]
        
        # Түймелер координаттары
        panel_x = MAZE_AREA + 20
        # Деңгейлер
        self.btn_easy = pygame.Rect(panel_x, 120, 200, 35)
        self.btn_med = pygame.Rect(panel_x, 160, 200, 35)
        self.btn_hard = pygame.Rect(panel_x, 200, 200, 35)
        
        # Басқару стрелкалары (D-pad)
        bw, bh = 50, 50
        cx, cy = panel_x + 100, 340
        self.btn_up = pygame.Rect(cx - bw//2, cy - bh - 5, bw, bh)
        self.btn_down = pygame.Rect(cx - bw//2, cy + 5, bw, bh)
        self.btn_left = pygame.Rect(cx - bw*1.5 - 5, cy, bw, bh)
        self.btn_right = pygame.Rect(cx + bw//2 + 5, cy, bw, bh)

        # Функциялар
        self.btn_ai = pygame.Rect(panel_x, 440, 200, 45)
        self.btn_reset = pygame.Rect(panel_x, 495, 200, 45)

        # Басқару логикасы
        self.dragging = False
        self.drag_start = None
        self.swipe_threshold = 20
        self.move_delay = 0.12
        self.last_move_time = 0
        
        self.sounds = {}
        self.load_sounds()
        self.reset_maze()

    def load_sounds(self):
        sound_files = {"generate": "generate.wav", "solve": "solve.wav", "finish": "finish.wav", "move": "move.wav"}
        for name, file in sound_files.items():
            if os.path.exists(file):
                self.sounds[name] = pygame.mixer.Sound(file)
            else:
                self.sounds[name] = None

    def play_sound(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

    def reset_maze(self, diff_name=None):
        if diff_name:
            self.current_diff = diff_name
            self.grid_size = self.difficulties[diff_name]
            
        self.cell_size = MAZE_AREA // self.grid_size
        self.grid = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.path = []
        self.player_pos = [1, 1] 
        self.solve_time = 0
        self.is_solved = False
        self.has_won = False
        self.status_msg = f"{self.current_diff} деңгей"
        self.generate_maze()

    def generate_maze(self):
        self.play_sound("generate")
        stack = [(1, 1)]
        self.grid[1][1] = 0
        while stack:
            curr_r, curr_c = stack[-1]
            neighbors = []
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 < nr < self.grid_size - 1 and 0 < nc < self.grid_size - 1 and self.grid[nr][nc] == 1:
                    neighbors.append((nr, nc))
            if neighbors:
                next_r, next_c = random.choice(neighbors)
                self.grid[curr_r + (next_r - curr_r) // 2][curr_c + (next_c - curr_c) // 2] = 0
                self.grid[next_r][next_c] = 0
                stack.append((next_r, next_c))
            else:
                stack.pop()

    def move_player(self, dr, dc):
        current_time = time.time()
        if current_time - self.last_move_time < self.move_delay:
            return
        
        if self.has_won: return
        nr, nc = self.player_pos[0] + dr, self.player_pos[1] + dc
        if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.grid[nr][nc] == 0:
            self.player_pos = [nr, nc]
            self.last_move_time = current_time
            self.play_sound("move")
            if (nr, nc) == (self.grid_size - 2, self.grid_size - 2):
                self.has_won = True
                self.status_msg = "ЖЕҢІС!"
                self.play_sound("finish")

    def solve_maze_ai(self):
        if self.is_solved or self.has_won: return
        self.play_sound("solve")
        start_time = time.time()
        start, end = (1, 1), (self.grid_size - 2, self.grid_size - 2)
        queue, visited, parent = deque([start]), {start}, {}

        while queue:
            curr = queue.popleft()
            if curr == end: break
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc)); parent[(nr, nc)] = curr; queue.append((nr, nc))
        
        curr, path = end, []
        while curr in parent:
            path.append(curr); curr = parent[curr]
        path.append(start)
        self.path = path
        self.solve_time = round(time.time() - start_time, 4)
        self.is_solved = True
        self.status_msg = "AI аяқтады"
        self.play_sound("finish")

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        if mouse_pressed:
            # Лабиринт аймағындағы Swipe (Жүргізу)
            if mouse_pos[0] < MAZE_AREA:
                if not self.dragging:
                    self.drag_start = mouse_pos
                    self.dragging = True
                else:
                    dx = mouse_pos[0] - self.drag_start[0]
                    dy = mouse_pos[1] - self.drag_start[1]
                    if abs(dx) > self.swipe_threshold or abs(dy) > self.swipe_threshold:
                        if abs(dx) > abs(dy):
                            self.move_player(0, 1 if dx > 0 else -1)
                        else:
                            self.move_player(1 if dy > 0 else -1, 0)
                        self.drag_start = mouse_pos
            
            # Оң жақ панельдегі стрелкаларды басып тұру
            else:
                if self.btn_up.collidepoint(mouse_pos):    self.move_player(-1, 0)
                elif self.btn_down.collidepoint(mouse_pos):  self.move_player(1, 0)
                elif self.btn_left.collidepoint(mouse_pos):  self.move_player(0, -1)
                elif self.btn_right.collidepoint(mouse_pos): self.move_player(0, 1)
        else:
            self.dragging = False

    def draw_ui(self):
        pygame.draw.rect(self.screen, GRAY, (MAZE_AREA, 0, SIDE_PANEL_WIDTH, HEIGHT))
        pygame.draw.line(self.screen, WHITE, (MAZE_AREA, 0), (MAZE_AREA, HEIGHT), 2)

        self.screen.blit(self.font_big.render("МӘЗІР", True, WHITE), (MAZE_AREA + 20, 20))
        
        color = GOLD if self.has_won else (GREEN if self.is_solved else WHITE)
        self.screen.blit(self.font_mid.render(self.status_msg, True, color), (MAZE_AREA + 20, 60))

        # Деңгейлер
        self.screen.blit(self.font_small.render("ДЕҢГЕЙ ТАҢДАУ:", True, WHITE), (MAZE_AREA + 20, 100))
        for btn, label in [(self.btn_easy, "Оңай"), (self.btn_med, "Орташа"), (self.btn_hard, "Қиын")]:
            bg = ACTIVE_COLOR if self.current_diff == label else BUTTON_COLOR
            if btn.collidepoint(pygame.mouse.get_pos()): bg = BUTTON_HOVER
            pygame.draw.rect(self.screen, bg, btn, border_radius=8)
            txt = self.font_mid.render(label, True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=btn.center))

        # Басқару стрелкалары (D-pad)
        self.screen.blit(self.font_small.render("БАСҚАРУ:", True, WHITE), (MAZE_AREA + 20, 260))
        btns = [(self.btn_up, "↑"), (self.btn_down, "↓"), (self.btn_left, "←"), (self.btn_right, "→")]
        for rect, label in btns:
            bg = BUTTON_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
            pygame.draw.rect(self.screen, bg, rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=10)
            txt = self.font_big.render(label, True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

        # Функциялар
        for btn, label, bg in [(self.btn_ai, "AI ШЕШУ", (34, 197, 94)), (self.btn_reset, "ЖАҢА ОЙЫН", (239, 68, 68))]:
            if btn.collidepoint(pygame.mouse.get_pos()): bg = tuple(max(0, c-30) for c in bg)
            pygame.draw.rect(self.screen, bg, btn, border_radius=10)
            txt = self.font_mid.render(label, True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=btn.center))

        # Нұсқаулық
        instr = ["Тәсілдер:", "- Саусақпен жүргізу", "- Экран стрелкалары", "- Пернетақта"]
        for i, text in enumerate(instr):
            self.screen.blit(self.font_small.render(text, True, (200, 200, 200)), (MAZE_AREA + 20, 560 + i*20))

    def draw(self):
        self.screen.fill(BLACK)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                color = WHITE if self.grid[r][c] == 0 else BLACK
                if (r, c) == (1, 1) or (r, c) == (self.grid_size - 2, self.grid_size - 2): color = RED
                if (r, c) in self.path: color = BLUE
                pygame.draw.rect(self.screen, color, (c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size))

        py_r, py_c = self.player_pos
        padding = self.cell_size // 5
        pygame.draw.rect(self.screen, PLAYER_COLOR, 
                         (py_c * self.cell_size + padding, py_r * self.cell_size + padding, 
                          self.cell_size - padding*2, self.cell_size - padding*2), border_radius=4)
        
        self.draw_ui()
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.btn_easy.collidepoint(pos): self.reset_maze("Оңай")
                    elif self.btn_med.collidepoint(pos):  self.reset_maze("Орташа")
                    elif self.btn_hard.collidepoint(pos): self.reset_maze("Қиын")
                    elif self.btn_ai.collidepoint(pos):   self.solve_maze_ai()
                    elif self.btn_reset.collidepoint(pos): self.reset_maze()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:    self.move_player(-1, 0)
                    if event.key == pygame.K_DOWN:  self.move_player(1, 0)
                    if event.key == pygame.K_LEFT:  self.move_player(0, -1)
                    if event.key == pygame.K_RIGHT: self.move_player(0, 1)
                    if event.key == pygame.K_SPACE: self.reset_maze()
                    if event.key == pygame.K_RETURN: self.solve_maze_ai()

            self.handle_input()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    app = MazeApp()
    app.run()
 
 
