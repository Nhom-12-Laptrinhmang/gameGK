import socket
import json
import pygame
import threading
import sys
import os


HOST = '127.0.0.1'
PORT = 12345
WIDTH, HEIGHT = 800, 500
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (200, 200, 200)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oẳn Tù Tì")
clock = pygame.time.Clock()


try:
    font = pygame.font.SysFont("Tahoma", 36)
    small_font = pygame.font.SysFont("Tahoma", 24)
except:
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)


ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(name, scale=None):
    path = os.path.join(ASSETS_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


try:
    bg_img = load_image("background.png", (WIDTH, HEIGHT))
    player_left_idle = load_image("player_left_idle.png", (150, 150))
    player_right_idle = load_image("player_right_idle.png", (150, 150))
    rock_img = load_image("rock.png", (80, 80))
    paper_img = load_image("paper.png", (80, 80))
    scissors_img = load_image("scissors.png", (80, 80))
    win_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "win.mp3"))
    lose_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "lose.mp3"))
    draw_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "draw.mp3"))
except Exception as e:
    print("Lỗi load assets:", e)
    sys.exit()


state = "waiting"
choice = None
opponent_choice = None
result = None
scores = {"win": 0, "lose": 0, "draw": 0}
fade_alpha = 0


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
except Exception as e:
    print("Không thể kết nối server:", e)
    sys.exit()


choice_map = {"Búa": "rock", "Bao": "paper", "Kéo": "scissors"}
reverse_choice_map = {v: k for k, v in choice_map.items()}


def send_message(msg):
    try:
        client_socket.send(json.dumps(msg).encode())
        print(f"[DEBUG] Đã gửi tới server: {msg}")
    except:
        pass


def receive_messages():
    global state, opponent_choice, result
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            msg = json.loads(data)
            print(f"[DEBUG] Nhận từ server: {msg}")
            if msg["action"] == "start":
                state = "choosing"
            elif msg["action"] == "result":
                state = "result"
                result = msg["result"]
                opponent_choice = reverse_choice_map.get(msg["opponent"], msg["opponent"])
                scores[result] += 1
                print(f"[INFO] Kết quả: Bạn {'THẮNG' if result=='win' else 'THUA' if result=='lose' else 'HOÀ'} | Đối thủ chọn {opponent_choice}")


                try:
                    send_message({
                        "action": "report_result",
                        "your_choice": choice_map[choice],
                        "opponent_choice": msg["opponent"],
                        "result": result
                    })
                    print("[DEBUG] Đã gửi kết quả về server")
                except:
                    print("[ERROR] Không thể gửi kết quả về server")

                if result == "win":
                    win_sound.play()
                elif result == "lose":
                    lose_sound.play()
                else:
                    draw_sound.play()
            elif msg["action"] == "opponent_disconnected":
                state = "disconnected"
                print("[INFO] Đối thủ đã thoát!")
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()


symbol_images = {"Kéo": scissors_img, "Búa": rock_img, "Bao": paper_img}

def fade_in_out():
    global fade_alpha
    if state == "result":
        fade_alpha = min(200, fade_alpha + 10)
    else:
        fade_alpha = max(0, fade_alpha - 10)

def draw_button(text, x, y, w, h, hover=False):
    color = GREEN if hover else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2, border_radius=10)
    txt = font.render(text, True, BLACK)
    screen.blit(txt, (x + w//2 - txt.get_width()//2, y + h//2 - txt.get_height()//2))

def draw_choice(symbol, pos):
    img = symbol_images.get(symbol)
    if img:
        screen.blit(img, pos)


running = True

button_width = 100
button_height = 50
spacing = 80

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill(WHITE)
    screen.blit(bg_img, (0,0))


    total_width = 3 * button_width + 2 * spacing
    start_x = WIDTH // 2 - total_width // 2

    y_buttons = HEIGHT // 2 + 60


    choosing_buttons = [
        ("Búa", start_x, y_buttons, button_width, button_height),
        ("Bao", start_x + (button_width + spacing), y_buttons, button_width, button_height),
        ("Kéo", start_x + 2 * (button_width + spacing), y_buttons, button_width, button_height),
    ]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == "choosing":

                for text, bx, by, bw, bh in choosing_buttons:
                    if bx <= mouse_x <= bx + bw and by <= mouse_y <= by + bh:
                        choice = text
                        send_message({"action": "choose", "choice": choice_map[choice]})
                        state = "waiting_opponent"
                        break
            elif state == "result":
                if 300 <= mouse_x <= 500 and 420 <= mouse_y <= 470:
                    send_message({"action": "play_again"})