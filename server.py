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
                try:
                    data = player.recv(1024).decode()
                    if not data:
                        raise ConnectionResetError
                    msg = json.loads(data)
                    if msg["action"] == "choose":
                        choices[player] = msg["choice"]
                    elif msg["action"] == "report_result":
                        print(f"[RESULT] Client báo cáo: {msg}")
                except (ConnectionResetError, json.JSONDecodeError):
               
                    other = player2 if player == player1 else player1
                    other.send(json.dumps({"action": "opponent_disconnected"}).encode())
                    return


        p1_choice = choices[player1]
        p2_choice = choices[player2]
        if p1_choice == p2_choice:
            result1, result2 = "draw", "draw"
        elif (p1_choice == "rock" and p2_choice == "scissors") or \
                (p1_choice == "paper" and p2_choice == "rock") or \
                (p1_choice == "scissors" and p2_choice == "paper"):
            result1, result2 = "win", "lose"
        else:
            result1, result2 = "lose", "win"


        player1.send(json.dumps({"action": "result", "result": result1, "opponent": p2_choice}).encode())
        player2.send(json.dumps({"action": "result", "result": result2, "opponent": p1_choice}).encode())


        play_again_count = 0
        while play_again_count < 2:
            for player in [player1, player2]:
                try:
                    data = player.recv(1024).decode()
                    if not data:
                        raise ConnectionResetError
                    msg = json.loads(data)
                    if msg["action"] == "play_again":
                        play_again_count += 1
                    elif msg["action"] == "report_result":
                        print(f"[RESULT] Client báo cáo: {msg}")
                except (ConnectionResetError, json.JSONDecodeError):
                    other = player2 if player == player1 else player1
                    other.send(json.dumps({"action": "opponent_disconnected"}).encode())
                    return

        handle_game(player1, player2)

    except Exception as e:
        print(f"Lỗi trong trận đấu: {e}")
    finally:

        try:
            player1.close()
            player2.close()
        except:
            pass


def handle_client(client_socket):

    with lock:
        waiting_queue.append(client_socket)