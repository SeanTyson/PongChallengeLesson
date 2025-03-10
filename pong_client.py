import pygame
import math
import socket
import threading
import json
import traceback

HOST = "127.0.0.1"
PORT = 5050

def receive_updates(client_socket):
    global paddle_positions, player_id, ballPosition

    while True:
        try:
          # Receive the first 10 characters to get the message length
            length_data = client_socket.recv(10).decode('utf-8')
            if not length_data:
                break
            
            message_length = int(length_data.strip())  # Get the message length

            message_data = client_socket.recv(message_length).decode('utf-8')

            game_state = json.loads(message_data)
            ballPosition.x = game_state["ballPosition"][0]
            ballPosition.y = game_state["ballPosition"][1]


            if player_id == 2:        
                paddle_positions[0]['y'] = game_state['paddles'][0]
            else:
                paddle_positions[player_id]['y'] = game_state['paddles'][player_id] # playerid here represents the right paddle

        except Exception as e:
            print(f"Error: {str(e)}")
            break

# initial game setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
coolfondant = pygame.font.SysFont('Comic Sans MS', 30)
dt = 0
scores = [0, 0]
paddleHeight = 120
paddleWidth = 30
rPaddleLeftEdgeX = screen.get_width() -180

paddlePosition = {'x': 150, 'y': (screen.get_height() / 2) - (paddleHeight / 2)}
rPaddlePosition = {'x': rPaddleLeftEdgeX, 'y': (screen.get_height() / 2) - (paddleHeight / 2)}

paddle_positions = [paddlePosition, rPaddlePosition]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

player_id = int(client_socket.recv(1024).decode('utf-8'))
print(f"Assigned Player ID: {player_id}")

receive_thread = threading.Thread(target=receive_updates, args=(client_socket,))
receive_thread.start()


ballPosition = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)  
ballVelocity = pygame.Vector2(-300, 100)

#pygame.mixer.music.load("assets/audio/thats_a_paddlin.mp3")  

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if ballPosition.x <= 0:
        ballPosition.x = screen.get_width() / 2
        ballPosition.y = screen.get_height() / 2
        scores[0] += 1
        #pygame.mixer.music.play()
        ballVelocity = pygame.Vector2(-300, 100)  # Reset ball velocity
    elif ballPosition.x >= screen.get_width():
        ballPosition.x = screen.get_width() / 2
        ballPosition.y = screen.get_height() / 2
        scores[1] += 1
        #pygame.mixer.music.play()
        ballVelocity = pygame.Vector2(-300, 100) 

    screen.fill("purple")

    text_surface = coolfondant.render(str(scores[0]), False, (0, 0, 0))
    screen.blit(text_surface, (screen.get_width() - 50, 0))
    text_surface = coolfondant.render(str(scores[1]), False, (0, 0, 0))
    screen.blit(text_surface, (30, 0))
    pygame.draw.circle(screen, "red", ballPosition, 15)
    paddle = pygame.Rect(paddlePosition['x'], paddlePosition['y'], paddleWidth, paddleHeight)
    pygame.draw.rect(screen, "red", paddle)
    rPaddle = pygame.Rect(rPaddlePosition['x'], rPaddlePosition['y'], paddleWidth, paddleHeight)
    pygame.draw.rect(screen, "red", rPaddle)
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle_positions[player_id-1]['y'] -= 300 * dt
    if keys[pygame.K_s]:
        paddle_positions[player_id-1]['y'] += 300 * dt
    client_socket.sendall(str(paddle_positions[player_id-1]['y']).encode('utf-8'))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
client_socket.close()