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