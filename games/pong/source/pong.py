import cv2
import mediapipe as mp
import numpy as np
import random
import pygame
import sys

# Pygame микшерін дыбыс үшін инициализациялау
pygame.mixer.init()

def load_sound(file):
    try:
        return pygame.mixer.Sound(file)
    except:
        return None

# Дыбыстық файлдар
sound_hit = load_sound("hit.wav")
sound_power = load_sound("power.wav")
sound_wall = load_sound("wall.wav")
sound_score = load_sound("score.wav")

def play_sfx(sound):
    if sound:
        sound.play()

# MediaPipe параметрлері
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Ойын өлшемдері
WIDTH, HEIGHT = 800, 500
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 10

# Ойын күйлері
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
current_state = STATE_MENU

# Ойынның жұмыс істеп тұрғанын бақылайтын флаг
is_running = True

# Басқару режимдері
MODE_CAMERA = 0 
MODE_SENSOR = 1 
control_mode = MODE_SENSOR 

# Бастапқы позициялар мен мәндер
player_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ai_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2

# Жылдамдық параметрлері
BASE_SPEED = 7
ball_speed_x, ball_speed_y = BASE_SPEED, BASE_SPEED

# Ұпайлар мен рекорд
player_score, ai_score = 0, 0
high_score = 0 
last_max_milestone = 0 # Ең жоғары жеке ұпай бойынша соңғы меже

is_fist = False
mouse_y = HEIGHT // 2 

# Батырмалардың координаттары [x1, y1, x2, y2]
btn_start = [WIDTH//2 - 120, HEIGHT//2 - 100, WIDTH//2 + 120, HEIGHT//2 - 50]
btn_mode = [WIDTH//2 - 120, HEIGHT//2 - 30, WIDTH//2 + 120, HEIGHT//2 + 20]
btn_exit = [WIDTH//2 - 120, HEIGHT//2 + 40, WIDTH//2 + 120, HEIGHT//2 + 90]
btn_pause = [WIDTH - 150, 5, WIDTH - 5, 50] 
btn_resume = [WIDTH//2 - 120, HEIGHT//2 - 30, WIDTH//2 + 120, HEIGHT//2 + 20]

def reset_ball(reset_score=False):
    global ball_x, ball_y, ball_speed_x, ball_speed_y, player_score, ai_score, last_max_milestone
    
    if reset_score:
        player_score, ai_score = 0, 0
        last_max_milestone = 0
    
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    
    # Көшбасшының ұпайына байланысты деңгей (қайсысы бірінші жетті)
    top_score = max(player_score, ai_score)
    level = top_score // 5
    current_speed = BASE_SPEED + (level * 1.8) # Жылдамдық өсуін сәл арттырдық
    
    ball_speed_x = current_speed if ball_speed_x < 0 else -current_speed
    ball_speed_y = random.choice([-current_speed, current_speed])
    play_sfx(sound_score)

def check_fist(hand_landmarks):
    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]
    count = 0
    for i in range(4):
        if hand_landmarks.landmark[tips[i]].y > hand_landmarks.landmark[joints[i]].y:
            count += 1
    return count >= 3

def mouse_callback(event, x, y, flags, param):
    global current_state, control_mode, mouse_y, is_running
    mouse_y = y
    if event == cv2.EVENT_LBUTTONDOWN:
        if current_state == STATE_MENU:
            if btn_start[0] < x < btn_start[2] and btn_start[1] < y < btn_start[3]:
                reset_ball(reset_score=True)
                current_state = STATE_PLAYING
            elif btn_mode[0] < x < btn_mode[2] and btn_mode[1] < y < btn_mode[3]:
                control_mode = MODE_SENSOR if control_mode == MODE_CAMERA else MODE_CAMERA
            elif btn_exit[0] < x < btn_exit[2] and btn_exit[1] < y < btn_exit[3]:
                is_running = False 
        elif current_state == STATE_PLAYING:
            if btn_pause[0] < x < btn_pause[2] and btn_pause[1] < y < btn_pause[3]:
                current_state = STATE_PAUSED
        elif current_state == STATE_PAUSED:
            if btn_resume[0] < x < btn_resume[2] and btn_resume[1] < y < btn_resume[3]:
                current_state = STATE_PLAYING
            elif btn_exit[0] < x < btn_exit[2] and btn_exit[1] < y < btn_exit[3]:
                current_state = STATE_MENU

def draw_button(img, coords, text, color=(100, 100, 100)):
    cv2.rectangle(img, (coords[0], coords[1]), (coords[2], coords[3]), color, -1)
    cv2.rectangle(img, (coords[0], coords[1]), (coords[2], coords[3]), (255, 255, 255), 2)
    cv2.putText(img, text, (coords[0] + 15, coords[1] + 32), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

window_name = "AI Pong Master"
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, mouse_callback)
cap = cv2.VideoCapture(0)

while is_running:
    success, frame = cap.read()
    if not success:
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    else:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (WIDTH, HEIGHT), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    if current_state == STATE_MENU:
        cv2.putText(frame, "AI PONG MASTER", (WIDTH//2 - 160, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3)
        cv2.putText(frame, f"REKORD: {high_score}", (WIDTH//2 - 80, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(frame, "EREJELER:", (50, HEIGHT - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
        cv2.putText(frame, "- Kim birinshi 5 upai jinaса, jyldamdyq artady", (50, HEIGHT - 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, "- 10, 20 upailarda qattyraq jyldamdaidy", (50, HEIGHT - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        draw_button(frame, btn_start, "BASTAU", (0, 150, 0))
        mode_text = "REJIM: SENSOR" if control_mode == MODE_SENSOR else "REJIM: KAMERA"
        draw_button(frame, btn_mode, mode_text, (150, 150, 0))
        draw_button(frame, btn_exit, "SHYGU", (0, 0, 150))
        
    elif current_state == STATE_PLAYING or current_state == STATE_PAUSED:
        if control_mode == MODE_CAMERA and success:
            results = hands.process(rgb_frame)
            is_fist = False
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if current_state == STATE_PLAYING:
                        y_coord = hand_landmarks.landmark[9].y
                        player_y = int(y_coord * HEIGHT) - PADDLE_HEIGHT // 2
                        is_fist = check_fist(hand_landmarks)
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            if current_state == STATE_PLAYING:
                player_y = mouse_y - PADDLE_HEIGHT // 2
                is_fist = False

        player_y = max(0, min(HEIGHT - PADDLE_HEIGHT, player_y))

        if current_state == STATE_PLAYING:
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
                ball_speed_y *= -1
                play_sfx(sound_wall)

            # Көшбасшының ұпайы
            top_score = max(player_score, ai_score)
            
            ai_speed = 6 + (top_score // 5)
            ai_center = ai_y + PADDLE_HEIGHT // 2
            if ai_center < ball_y - 25: ai_y += ai_speed
            elif ai_center > ball_y + 25: ai_y -= ai_speed
            ai_y = max(0, min(HEIGHT - PADDLE_HEIGHT, ai_y))

            if player_score > high_score:
                high_score = player_score

            # Жылдамдықты арттыру логикасы: Кез келгені бірінші болып 5-ке жетсе
            if top_score > 0 and top_score % 5 == 0 and top_score > last_max_milestone:
                last_max_milestone = top_score
                # 10, 20 сияқты межелерде жылдамдық өте қатты артады
                boost = 1.3 if top_score % 10 == 0 else 1.15
                ball_speed_x *= boost
                ball_speed_y *= boost

            if ball_x <= PADDLE_WIDTH:
                if player_y < ball_y < player_y + PADDLE_HEIGHT:
                    ball_speed_x = abs(ball_speed_x) * (1.8 if is_fist else 1.05)
                    play_sfx(sound_power if is_fist else sound_hit)
                    ball_x = PADDLE_WIDTH + 1
                elif ball_x < 0:
                    ai_score += 1
                    reset_ball()

            if ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE:
                if ai_y < ball_y < ai_y + PADDLE_HEIGHT:
                    ball_speed_x = -abs(ball_speed_x)
                    play_sfx(sound_hit)
                    ball_x = WIDTH - PADDLE_WIDTH - BALL_SIZE - 1
                elif ball_x > WIDTH:
                    player_score += 1
                    reset_ball()

        # Графика
        p_color = (0, 165, 255) if is_fist else (255, 120, 0)
        cv2.rectangle(frame, (0, player_y), (PADDLE_WIDTH, player_y + PADDLE_HEIGHT), p_color, -1)
        cv2.rectangle(frame, (WIDTH - PADDLE_WIDTH, ai_y), (WIDTH, ai_y + PADDLE_HEIGHT), (0, 0, 255), -1)
        
        b_color = (0, 255, 255) if abs(ball_speed_x) > 15 else (255, 255, 255)
        cv2.circle(frame, (int(ball_x), int(ball_y)), BALL_SIZE, b_color, -1)

        cv2.putText(frame, f"Siz: {player_score}", (30, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Rekord: {high_score}", (WIDTH//2 - 60, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"AI: {ai_score}", (WIDTH - 280, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Көшбасшының ұпайы бойынша деңгей
        current_lvl = max(player_score, ai_score) // 5
        cv2.putText(frame, f"Level: {current_lvl}", (WIDTH//2 - 40, HEIGHT - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)

        if current_state == STATE_PLAYING:
            draw_button(frame, btn_pause, "TOQTATU", (60, 60, 60))
        else:
            cv2.putText(frame, "PAUZA", (WIDTH//2 - 70, HEIGHT//2 - 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            draw_button(frame, btn_resume, "JALGASTYRU", (0, 150, 0))
            draw_button(frame, btn_exit, "MENYUGE", (0, 0, 150))

    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'): 
        is_running = False

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
sys.exit()
