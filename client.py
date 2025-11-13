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
    