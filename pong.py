import pygame
import math

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
paddleRightEdgeX = 180
rPaddleLeftEdgeX = screen.get_width() -180
ballPosition = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ballVelocity = pygame.Vector2(-300, 100)  # Initial velocity
paddlePosition = {'x': 150, 'y': (screen.get_height() / 2) - (paddleHeight / 2)}
rPaddlePosition = {'x': rPaddleLeftEdgeX, 'y': (screen.get_height() / 2) - (paddleHeight / 2)}
pygame.mixer.music.load("assets/audio/thats_a_paddlin.mp3")  

def handle_paddle_collision(paddle, is_left_paddle):
    global ballVelocity 

    # Calculate bounce angle
    # distance from center=ball’s y position−paddle’s center y position
    relative_intersect = (ballPosition.y - (paddle['y'] + paddleHeight / 2)) / (paddleHeight / 2)
    max_bounce_angle = math.radians(45)  # Max bounce angle
    new_angle = relative_intersect * max_bounce_angle  # Update theta

    # Update ball velocity
    ballSpeed = ballVelocity.length()
    ballVelocity.x = ballSpeed * math.cos(new_angle)
    ballVelocity.y = ballSpeed * math.sin(new_angle)

    # Ensure the ball moves in the correct direction after hitting the right paddle
    if  not is_left_paddle: 
        ballVelocity.x *= -1

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    if ballPosition.x <= 0:
        ballPosition.x = screen.get_width() / 2
        ballPosition.y = screen.get_height() / 2
        scores[0] += 1
        pygame.mixer.music.play()
        ballVelocity = pygame.Vector2(-300, 100)  # Reset ball velocity
    elif ballPosition.x >= screen.get_width():
        ballPosition.x = screen.get_width() / 2
        ballPosition.y = screen.get_height() / 2
        scores[1] += 1
        pygame.mixer.music.play()
        ballVelocity = pygame.Vector2(-300, 100) 

    text_surface = coolfondant.render(str(scores[0]), False, (0, 0, 0))
    screen.blit(text_surface, (screen.get_width() - 50, 0))
    text_surface = coolfondant.render(str(scores[1]), False, (0, 0, 0))
    screen.blit(text_surface, (30, 0))
    pygame.draw.circle(screen, "red", ballPosition, 15)
    paddle = pygame.Rect(paddlePosition['x'], paddlePosition['y'], paddleWidth, paddleHeight)
    pygame.draw.rect(screen, "red", paddle)
    rPaddle = pygame.Rect(rPaddlePosition['x'], rPaddlePosition['y'], paddleWidth, paddleHeight)
    pygame.draw.rect(screen, "red", rPaddle)
    
    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddlePosition['y'] -= 300 * dt
    if keys[pygame.K_s]:
        paddlePosition['y'] += 300 * dt
    if keys[pygame.K_UP]:
        rPaddlePosition['y'] -= 300 * dt
    if keys[pygame.K_DOWN]:
        rPaddlePosition['y'] += 300 * dt
    
    # Ball movement
    ballPosition += ballVelocity * dt

    # Collision detection
    ballEdgeX = ballPosition.x - 15  # Left edge of the ball
    rBallEdgeX = ballPosition.x + 15 # Right edge of the ball
    ballEdgeY = ballPosition.y
    paddleTopPixel = paddlePosition['y']
    paddleBottomPixel = paddlePosition['y'] + paddleHeight
    rPaddleTopPixel = rPaddlePosition['y']
    rPaddleBottomPixel = rPaddlePosition['y'] + paddleHeight
    
    if ballEdgeY >= screen.get_height() or ballEdgeY <=0:
        if ballVelocity.y >0:
            ballVelocity.y = -ballVelocity.y
        else:
            ballVelocity.y *=-1

    if (ballEdgeX < paddleRightEdgeX and rBallEdgeX > paddleRightEdgeX - 30) and paddleTopPixel <= ballEdgeY <= paddleBottomPixel:
        handle_paddle_collision(paddlePosition, True)
    

    elif (rBallEdgeX > rPaddleLeftEdgeX and ballEdgeX < rPaddleLeftEdgeX + 30) and rPaddleTopPixel <= ballEdgeY <= rPaddleBottomPixel:
        handle_paddle_collision(rPaddlePosition, False)
    
    # flip() the display - pygame weirdness?
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
