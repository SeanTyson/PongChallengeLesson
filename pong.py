import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
playerHeight = 120
playerWidth = 30
paddleRightEdgeX = 180
leftPaddleHit = False
ballPosition = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
playerPosition = {'x': 150, 'y': (screen.get_height() / 2) - (playerHeight / 2)}
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", ballPosition, 15)
    paddle = pygame.Rect(playerPosition['x'], playerPosition['y'], playerWidth, playerHeight)
    pygame.draw.rect(screen, "red", paddle)
    
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerPosition['y'] -= 300 * dt
    if keys[pygame.K_s]:
        playerPosition['y'] += 300 * dt

    if leftPaddleHit:
        ballPosition.x += 300 * dt
    else:
        ballPosition.x -= 300 * dt

    #TODO: Make this dynamic so it will always be a pixel exactly in the range of the ballposition possible values
    ballEdge = ballPosition.x + 15 
    playerTopPixel = playerPosition['y'] + playerHeight / 2
    playerBottomPixel = playerPosition['y'] - playerHeight / 2
    if ballEdge < paddleRightEdgeX and ballEdge < playerTopPixel:
        leftPaddleHit = True
        ballPosition.x += 300 * dt


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()