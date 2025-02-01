import pygame
import math

# pygame setup
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
ballPosition = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ballVelocity = pygame.Vector2(-300, 100)  # Initial velocity
paddlePosition = {'x': 150, 'y': (screen.get_height() / 2) - (paddleHeight / 2)}

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color
    screen.fill("purple")

    if ballPosition.x <= 0:
        ballPosition.x = screen.get_width() / 2
        ballPosition.y = screen.get_height() / 2
        scores[0] += 1
        ballVelocity = pygame.Vector2(-300, 100)  # Reset ball velocity

    text_surface = coolfondant.render(str(scores[0]), False, (0, 0, 0))
    screen.blit(text_surface, (screen.get_width() - 50, 0))
    text_surface = coolfondant.render(str(scores[1]), False, (0, 0, 0))
    screen.blit(text_surface, (30, 0))
    pygame.draw.circle(screen, "red", ballPosition, 15)
    paddle = pygame.Rect(paddlePosition['x'], paddlePosition['y'], paddleWidth, paddleHeight)
    pygame.draw.rect(screen, "red", paddle)
    
    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddlePosition['y'] -= 300 * dt
    if keys[pygame.K_s]:
        paddlePosition['y'] += 300 * dt
    
    # Ball movement
    ballPosition += ballVelocity * dt

    # Collision detection
    ballEdgeX = ballPosition.x - 15  # Left edge of the ball
    ballEdgeY = ballPosition.y
    paddleTopPixel = paddlePosition['y']
    paddleBottomPixel = paddlePosition['y'] + paddleHeight
    
    if ballEdgeX < paddleRightEdgeX and paddleTopPixel <= ballEdgeY <= paddleBottomPixel:
        # Calculate bounce angle
        # distance from center=ball’s y position−paddle’s center y position
        relative_intersect = (ballPosition.y - (paddlePosition['y'] + paddleHeight / 2)) / (paddleHeight / 2)
        max_bounce_angle = math.radians(45)  # Convert to radians
        new_angle = relative_intersect * max_bounce_angle #update theta
        
        # Update ball velocity
        ballSpeed = ballVelocity.length()
        ballVelocity.x = ballSpeed * math.cos(new_angle)
        ballVelocity.y = ballSpeed * math.sin(new_angle)
        
        # Ensure the ball moves to the right after hitting the paddle
        if ballVelocity.x < 0:
            ballVelocity.x *= -1
    
    # flip() the display
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
