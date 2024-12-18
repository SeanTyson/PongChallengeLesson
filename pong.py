import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
coolfondant = pygame.font.SysFont('Comic Sans MS', 30)
dt = 0
scores = [0,0]
paddleHeight = 120
paddleWidth = 30
paddleRightEdgeX = 180
leftPaddleHit = False
ballPosition = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
paddlePosition = {'x': 150, 'y': (screen.get_height() / 2) - (paddleHeight / 2)}
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    if ballPosition.x <= 0:
        ballPosition.x = screen.get_width() / 2
        ballPosition.y = screen.get_height() / 2
        scores[0] += 1
    

    text_surface = coolfondant.render(str(scores[0]), False, (0, 0, 0))
    screen.blit(text_surface, (screen.get_width() - 50,0))
    text_surface = coolfondant.render(str(scores[1]), False, (0, 0, 0))
    screen.blit(text_surface, (30,0))
    pygame.draw.circle(screen, "red", ballPosition, 15)
    paddle = pygame.Rect(paddlePosition['x'], paddlePosition['y'], paddleWidth, paddleHeight)
    pygame.draw.rect(screen, "red", paddle)
    
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddlePosition['y'] -= 300 * dt
    if keys[pygame.K_s]:
        paddlePosition['y'] += 300 * dt

    if leftPaddleHit:
        ballPosition.x += 300 * dt
        ballPosition.y -= 100 * dt
    else:
        ballPosition.x -= 300 * dt
        ballPosition.y += 100 * dt

    #TODO: Make this dynamic so it will always be a pixel exactly in the range of the ballposition possible values
    ballEdgeX = ballPosition.x + 15
    ballEdgeY = ballPosition.y + 15
    paddleTopPixel = paddlePosition['y']
    paddleBottomPixel = paddlePosition['y'] + paddleHeight
    if ballEdgeX < paddleRightEdgeX and ballEdgeY >= paddleTopPixel and ballEdgeY <= paddleBottomPixel:
        leftPaddleHit = True
        ballPosition.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()