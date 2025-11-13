import socket
import threading
import json
import time

HOST = '127.0.0.1'
PORT = 12345
waiting_queue = []
lock = threading.Lock()


def handle_game(player1, player2):

    try:

        player1.send(json.dumps({"action": "start"}).encode())
        player2.send(json.dumps({"action": "start"}).encode())

        choices = {}
        while len(choices) < 2:

            for player in [player1, player2]:
               