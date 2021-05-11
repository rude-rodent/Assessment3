import pygame
import sys

pygame.init()
pygame.display.set_caption("Assessment 3")
screen = pygame.display.set_mode((1280, 720))  # Sets resolution.

screenWidth = 1280
screenHeight = 720

playerImage = pygame.image.load("player.png")
playerHitBox = playerImage.get_rect()


class Player:

    def __init__(self):
        self.xPosition = screenWidth/2
        self.yPosition = screenHeight/2
        self.hitBox = playerHitBox

    def draw(self):
        screen.blit(playerImage, (self.xPosition, self.yPosition))
        self.hitBox = playerImage.get_rect(topleft=(self.xPosition, self.yPosition))
        # pygame.draw.rect(screen, (200, 0, 0), self.hitBox)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_a]:
            self.xPosition -= 1
        if pygame.key.get_pressed()[pygame.K_d]:
            self.xPosition += 1
        if pygame.key.get_pressed()[pygame.K_w]:
            self.yPosition -= 1
        if pygame.key.get_pressed()[pygame.K_s]:
            self.yPosition += 1


playerInstance = Player()
background = (200, 30, 30)

running = True
while running:
    for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(background)

    playerInstance.move()
    playerInstance.draw()

    pygame.display.update()
    pygame.display.flip()  # 2 buffers: stuff that's going to draw, stuff that's already drawn. Flip turns the two.

