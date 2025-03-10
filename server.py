import socket
import threading
import json
import pygame

HOST = "0.0.0.0"
PORT = 5050

clients = []
shutdown_flag = False  # Global flag to signal shutdown

clock = pygame.time.Clock()
dt = 0
ballPosition = [640.0, 360.0]  # Store as a list instead of pygame.Vector2
ballVelocity = [-300.0, 100.0]  # Store as a list instead of pygame.Vector2
game_state = {"ballPosition": ballPosition, "paddles": [360, 360]}

def broadcast_game_state():
    state_json = json.dumps(game_state)
    for client in clients:
        try:
            message = f"{len(state_json):<10}" + state_json
            client.sendall(message.encode('utf-8'))
        except:
            clients.remove(client)

def handle_client(client_socket, player_id):
    global game_state
    try:
        while not shutdown_flag:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            try:
                paddle_y = json.loads(data)
                game_state["paddles"][player_id-1] = paddle_y
            except:
                continue
            
            broadcast_game_state()
    except:
        pass
    finally:
        clients.remove(client_socket)
        client_socket.close()

def handle_ball_movement():
    global ballPosition, dt, ballVelocity
    while True:
        ballPosition[0] += ballVelocity[0] * dt
        ballPosition[1] += ballVelocity[1] * dt
        dt = clock.tick(60) / 1000

def start_server():
    global shutdown_flag
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
        server_socket.settimeout(1)  # Set a timeout on accept() to periodically check for shutdown
        print(f"Server started on {HOST}:{PORT}")

        while not shutdown_flag:
            try:
                client_socket, _ = server_socket.accept()
                clients.append(client_socket)
                player_id = len(clients)
                client_socket.sendall(str(player_id).encode('utf-8'))
                print(f"New connection, assigned Player {player_id}")
                threading.Thread(target=handle_client, args=(client_socket, player_id), daemon=True).start()
                threading.Thread(target=handle_ball_movement, daemon=True).start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        shutdown_flag = True  # Signal all threads to exit

        # Close all client sockets
        for client in clients:
            client.close()

        # Close the server socket
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    start_server()