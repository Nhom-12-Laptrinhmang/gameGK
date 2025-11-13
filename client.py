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
   #Phan nay là kết nối client với serve
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
#kết thúc xử lí client với server