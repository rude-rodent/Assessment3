import pygame
import sys
import math

pygame.init()
pygame.display.set_caption("Assessment 3")
screen = pygame.display.set_mode((1280, 720))  # Sets resolution.

screenWidth = 1280
screenHeight = 720

playerImage = pygame.image.load("player.png")
bulletImage = pygame.image.load("bullet.png")
moveSpeed = 0.3
playerBulletSpeed = 1


class Player:

    def __init__(self):
        # Starting position.
        self.x = screenWidth / 2
        self.y = screenHeight / 2
        # Original image kept to avoid distortion caused by rotating.
        self.originalImage = playerImage
        # Will be set later.
        self.rotatedImage = playerImage
        self.rotatedImageRect = playerImage.get_rect()

    def look(self):
        # Get the mouse position.
        mouseX, mouseY = pygame.mouse.get_pos()
        # Calculate the vector between the player and mouse.
        relativeX, relativeY = mouseX - self.x, mouseY - self.y
        # Convert the vector into an angle (in radians). Must be inverted.
        radAngle = -math.atan2(relativeY, relativeX)
        # Convert the angle into degrees.
        degAngle = radAngle * 180/math.pi
        # Create a rotated copy of the original image (if no copy, distortion happens).
        self.rotatedImage = pygame.transform.rotate(self.originalImage, int(degAngle))
        # Create a rect of the rotated image; its center is the center of a rect of the original image; its center is the player's position.
        self.rotatedImageRect = self.rotatedImage.get_rect(center=self.originalImage.get_rect(center=(self.x, self.y)).center)

    def move(self):
        # Move the player based on key presses, based on a move speed value.
        if pygame.key.get_pressed()[pygame.K_a]:
            self.x -= moveSpeed
        if pygame.key.get_pressed()[pygame.K_d]:
            self.x += moveSpeed
        if pygame.key.get_pressed()[pygame.K_w]:
            self.y -= moveSpeed
        if pygame.key.get_pressed()[pygame.K_s]:
            self.y += moveSpeed

    def fire(self):
        # Use the mouse and player positions to create a Vector2 between them. Normalise the vector to remove magnitude.
        mouseX, mouseY = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(mouseX - self.x, mouseY - self.y).normalize()
        # Position of the player.
        position = (self.x, self.y)
        # Instantiate a bullet; pass it the position and direction values.
        bulletInstance = Bullet(position, direction)
        playerBulletList.append(bulletInstance)

    def draw(self):
        # Blit the rotated image to the position of the rotated image's rect.
        screen.blit(self.rotatedImage, self.rotatedImageRect)


class Bullet:

    def __init__(self, position, direction):
        self.image = bulletImage
        self.bulletSpeed = playerBulletSpeed
        # The x and y values from the position tuple.
        self.x = position[0]
        self.y = position[1]
        # The direction, a Vector2.
        self.direction = direction

    def move(self):
        # Add the x and y values from the direction Vector2, multiplied by the bullet speed.
        self.x += self.direction.x * self.bulletSpeed
        self.y += self.direction.y * self.bulletSpeed

    def draw(self):
        # Draw the bullet at its updated position.
        screen.blit(self.image, (self.x, self.y))


playerInstance = Player()
playerBulletList = []
background = (200, 30, 30)

running = True
while running:
    for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            playerInstance.fire()

    screen.fill(background)

    playerInstance.move()
    playerInstance.look()
    playerInstance.draw()
    for bullet in playerBulletList:
        bullet.move()
        bullet.draw()

    pygame.display.update()
    pygame.display.flip()  # 2 buffers: stuff that's going to draw, stuff that's already drawn. Flip turns the two.

