import pygame
import random
import cv2
import mediapipe as mp
import numpy as np

# Түстер палитрасы
WHITE = (255, 255, 255)
BLACK = (15, 23, 42)
BLUE = (59, 130, 246)
RED = (239, 68, 68)
GREEN = (34, 197, 94)
GRAY = (71, 85, 105)
DARK_GRAY = (30, 41, 59)
GOLD = (250, 204, 21)

class RPS_AI:
    def __init__(self):
        self.history = []
        self.patterns = {}
        self.choices = ['тас', 'қағаз', 'қайшы']
        self.counters = {'тас': 'қағаз', 'қағаз': 'қайшы', 'қайшы': 'тас'}

    def get_prediction(self):
        if len(self.history) < 2:
            return random.choice(self.choices)
        
        last_two = tuple(self.history[-2:])
        if last_two in self.patterns:
            stats = self.patterns[last_two]
            predicted_move = max(stats, key=stats.get)
            return self.counters[predicted_move]
        return random.choice(self.choices)

    def update_learning(self, player_move):
        if len(self.history) >= 2:
            last_two = tuple(self.history[-2:])
            if last_two not in self.patterns:
                self.patterns[last_two] = {'тас': 0, 'қағаз': 0, 'қайшы': 0}
            patterns_ref = self.patterns[last_two]
            if player_move in patterns_ref:
                patterns_ref[player_move] += 1
        self.history.append(player_move)

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1000, 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI Тас-Қайшы-Қағаз (Camera Edition)")
        self.clock = pygame.time.Clock()
        
        # Қазақша қаріптер
        font_list = ["segoe ui", "arial", "tahoma", "dejavu sans"]
        self.font_main = pygame.font.SysFont(font_list, 36, bold=True)
        self.font_small = pygame.font.SysFont(font_list, 22)
        self.font_emoji = pygame.font.SysFont(["segoe ui symbol", "arial"], 100)
        self.font_countdown = pygame.font.SysFont(font_list, 150, bold=True)
        
        # MediaPipe Hands баптаулары
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.cap = None 
        
        self.ai = RPS_AI()
        self.scores = {"p1": 0, "p2": 0}
        self.round_num = 1
        
        self.mode = "MENU"
        self.p1_choice = None
        self.p2_choice = None
        self.result_text = "Таңдау жасаңыз"
        self.result_color = WHITE
        
        # Кері санақ күйі
        self.is_counting = False
        self.count_start_time = 0
        self.current_count = 0
        
        # Батырмалар
        self.game_buttons = {
            'тас': pygame.Rect(50, 650, 150, 70),
            'қағаз': pygame.Rect(220, 650, 150, 70),
            'қайшы': pygame.Rect(390, 650, 150, 70)
        }
        
        self.menu_buttons = {
            'AI': pygame.Rect(350, 200, 300, 70),
            'CAMERA': pygame.Rect(350, 300, 300, 70),
            'CAMERA_FRIEND': pygame.Rect(350, 400, 300, 70)
        }
        
        self.emojis = {'тас': '✊', 'қағаз': '✋', 'қайшы': '✌️'}
        self.p1_cam_gesture = None
        self.p2_cam_gesture = None

    def draw_text(self, text, font, color, x, y, center=True):
        img = font.render(text, True, color)
        rect = img.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(img, rect)

    def get_gestures(self, frame):
        """MediaPipe арқылы қол қимылдарын анықтау"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        gestures = {"left": None, "right": None}
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                avg_x = sum([lm.x for lm in landmarks]) / len(landmarks)
                
                fingers = []
                for tip, base in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                    fingers.append(landmarks[tip].y < landmarks[base].y)
                
                up_count = fingers.count(True)
                gesture = None
                if up_count == 0: gesture = "тас"
                elif up_count >= 3: gesture = "қағаз"
                elif up_count == 2 and fingers[0] and fingers[1]: gesture = "қайшы"
                
                if avg_x < 0.5:
                    gestures["left"] = gesture
                else:
                    gestures["right"] = gesture
        return gestures

    def determine_winner(self, p1, p2):
        if p1 == p2: return "тең"
        rules = {'тас': 'қайшы', 'қағаз': 'тас', 'қайшы': 'қағаз'}
        return "p1" if rules[p1] == p2 else "p2"

    def process_result(self, p1, p2):
        if not p1 or not p2:
            self.result_text = "Қол танылмады! Қайталаңыз."
            self.result_color = RED
            return

        self.p1_choice = p1
        self.p2_choice = p2
        res = self.determine_winner(p1, p2)
        
        if res == "тең":
            self.result_text = "ТЕҢ ТҮСТІ! 🤝"
            self.result_color = GRAY
        elif res == "p1":
            p1_name = "СІЗ" if self.mode != "CAMERA_FRIEND_MODE" else "1-ОЙЫНШЫ"
            self.result_text = f"{p1_name} ЖЕҢДІ! 🎉"
            self.result_color = GREEN
            self.scores["p1"] += 1
        else:
            p2_name = "2-ОЙЫНШЫ" if self.mode == "CAMERA_FRIEND_MODE" else "AI"
            self.result_text = f"{p2_name} ЖЕҢДІ! 🤖"
            self.result_color = RED
            self.scores["p2"] += 1
            
        if self.mode == "AI_MODE" or self.mode == "CAMERA_MODE":
            self.ai.update_learning(p1)
        self.round_num += 1

    def draw_menu(self):
        self.screen.fill(BLACK)
        self.draw_text("ТАС-ҚАЙШЫ-ҚАҒАЗ", self.font_main, GOLD, 500, 80)
        
        mouse_pos = pygame.mouse.get_pos()
        labels = {
            "AI": "AI-мен ойнау (Батырма)", 
            "CAMERA": "📷 Камера (vs AI)", 
            "CAMERA_FRIEND": "📷 Камера (Доспен)"
        }
        
        for mode, rect in self.menu_buttons.items():
            color = BLUE if rect.collidepoint(mouse_pos) else DARK_GRAY
            pygame.draw.rect(self.screen, color, rect, border_radius=15)
            self.draw_text(labels[mode], self.font_main, WHITE, rect.centerx, rect.centery)

    def draw_game(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, 1000, 100))
        self.draw_text(f"Раунд: {self.round_num}", self.font_main, WHITE, 500, 30)
        
        p1_label = "1-ОЙЫНШЫ" if self.mode == "CAMERA_FRIEND_MODE" else "СІЗ"
        p2_label = "2-ОЙЫНШЫ" if self.mode == "CAMERA_FRIEND_MODE" else "AI 🤖"
        
        self.draw_text(f"{p1_label}: {self.scores['p1']}", self.font_main, BLUE, 200, 70)
        self.draw_text(f"{p2_label}: {self.scores['p2']}", self.font_main, RED, 800, 70)

        # Камера режимдері
        if self.mode in ["CAMERA_MODE", "CAMERA_FRIEND_MODE"]:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                gestures = self.get_gestures(frame)
                self.p1_cam_gesture = gestures["left"]
                self.p2_cam_gesture = gestures["right"]
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_surf = np.transpose(frame_rgb, (1, 0, 2))
                frame_surf = pygame.surfarray.make_surface(frame_surf)
                frame_surf = pygame.transform.scale(frame_surf, (640, 480))
                self.screen.blit(frame_surf, (180, 150))
                
                if self.mode == "CAMERA_FRIEND_MODE":
                    pygame.draw.line(self.screen, GOLD, (500, 150), (500, 630), 3)
                
                if self.is_counting:
                    overlay = pygame.Surface((640, 480), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 150))
                    self.screen.blit(overlay, (180, 150))
                    self.draw_text(str(self.current_count), self.font_countdown, GOLD, 500, 390)
                else:
                    self.draw_text(self.result_text, self.font_main, self.result_color, 500, 130)
                    if not self.p1_choice:
                        if self.p1_cam_gesture:
                            self.draw_text(f"1-ОЙЫНШЫ: {self.p1_cam_gesture.upper()}", self.font_small, BLUE, 340, 650)
                        if self.mode == "CAMERA_FRIEND_MODE" and self.p2_cam_gesture:
                            self.draw_text(f"2-ОЙЫНШЫ: {self.p2_cam_gesture.upper()}", self.font_small, RED, 660, 650)
                        self.draw_text("Бастау үшін [SPACE] басыңыз", self.font_small, WHITE, 500, 680)

            if self.mode == "CAMERA_MODE":
                # Робот интерфейсі
                pygame.draw.rect(self.screen, DARK_GRAY, (830, 150, 150, 480), border_radius=15)
                pygame.draw.rect(self.screen, RED, (830, 150, 150, 50), border_radius=15)
                self.draw_text("AI ROBOT", self.font_small, WHITE, 905, 175)
                
                if self.p2_choice:
                    self.draw_text(self.emojis[self.p2_choice], self.font_emoji, WHITE, 905, 300)
                else:
                    self.draw_text("🤖", self.font_emoji, GRAY, 905, 300)
                
                # AI-дың "жады" немесе күйін көрсететін элементтер
                pygame.draw.rect(self.screen, BLACK, (845, 420, 120, 180), border_radius=10)
                self.draw_text("Жүйе:", self.font_small, GRAY, 905, 440)
                self.draw_text("Белсенді", self.font_small, GREEN, 905, 470)
                self.draw_text("Үйренуде...", self.font_small, GOLD, 905, 500)
        else:
            # Қалыпты режим (Батырмалармен vs AI)
            self.draw_text(self.result_text, self.font_main, self.result_color, 500, 150)
            if self.p1_choice:
                # Ойыншы жағы
                pygame.draw.circle(self.screen, DARK_GRAY, (300, 320), 100)
                self.draw_text(self.emojis[self.p1_choice], self.font_emoji, WHITE, 300, 320)
                
                # VS
                self.draw_text("VS", self.font_main, GRAY, 500, 320)
                
                # AI/Робот жағы
                pygame.draw.circle(self.screen, DARK_GRAY, (700, 320), 100)
                self.draw_text(self.emojis[self.p2_choice], self.font_emoji, WHITE, 700, 320)
                self.draw_text("ROBOT", self.font_small, RED, 700, 440)
            else:
                # Таңдау жасалғанға дейін роботты көрсету
                pygame.draw.circle(self.screen, DARK_GRAY, (700, 320), 100)
                self.draw_text("🤖", self.font_emoji, RED, 700, 320)
                self.draw_text("AI КҮТУДЕ", self.font_small, GRAY, 700, 440)

        if self.mode == "AI_MODE":
            mouse_pos = pygame.mouse.get_pos()
            for choice, rect in self.game_buttons.items():
                color = BLUE if rect.collidepoint(mouse_pos) else DARK_GRAY
                pygame.draw.rect(self.screen, color, rect, border_radius=15)
                self.draw_text(choice.capitalize(), self.font_small, WHITE, rect.centerx, rect.centery)

        back_rect = pygame.Rect(20, 110, 120, 40)
        pygame.draw.rect(self.screen, RED if back_rect.collidepoint(pygame.mouse.get_pos()) else DARK_GRAY, back_rect, border_radius=10)
        self.draw_text("← Мәзір", self.font_small, WHITE, back_rect.centerx, back_rect.centery)
        self.back_rect = back_rect

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()

            if self.is_counting:
                elapsed = (current_time - self.count_start_time)
                self.current_count = 3 - (elapsed // 1000)
                if elapsed >= 3000:
                    self.is_counting = False
                    if self.mode == "CAMERA_MODE":
                        ai_move = self.ai.get_prediction()
                        self.process_result(self.p1_cam_gesture, ai_move)
                    elif self.mode == "CAMERA_FRIEND_MODE":
                        self.process_result(self.p1_cam_gesture, self.p2_cam_gesture)

            if self.mode == "MENU":
                self.draw_menu()
            else:
                self.draw_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.is_counting:
                        if self.mode in ["CAMERA_MODE", "CAMERA_FRIEND_MODE"]:
                            self.is_counting = True
                            self.count_start_time = pygame.time.get_ticks()
                            self.p1_choice = self.p2_choice = None
                            self.result_text = "Дайындалыңыз..."

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if self.mode == "MENU":
                        if self.menu_buttons['AI'].collidepoint(pos):
                            self.mode = "AI_MODE"
                        elif self.menu_buttons['CAMERA'].collidepoint(pos):
                            self.mode = "CAMERA_MODE"
                            self.cap = cv2.VideoCapture(0)
                        elif self.menu_buttons['CAMERA_FRIEND'].collidepoint(pos):
                            self.mode = "CAMERA_FRIEND_MODE"
                            self.cap = cv2.VideoCapture(0)
                    else:
                        if self.back_rect.collidepoint(pos):
                            if self.cap: 
                                self.cap.release()
                                self.cap = None
                            self.mode = "MENU"
                            self.is_counting = False
                            self.scores = {"p1": 0, "p2": 0}
                            self.round_num = 1
                            self.p1_choice = self.p2_choice = None
                            self.result_text = "Таңдау жасаңыз"
                            continue
                            
                        if self.mode == "AI_MODE":
                            for choice, rect in self.game_buttons.items():
                                if rect.collidepoint(pos):
                                    ai_move = self.ai.get_prediction()
                                    self.process_result(choice, ai_move)

            pygame.display.flip()
            self.clock.tick(30)
            
        if self.cap: self.cap.release()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()


 
