import pygame
import sys
import math

pygame.init()
pygame.display.set_caption("Assessment 3")
screen = pygame.display.set_mode((1920, 1024))  # Sets resolution.

screenWidth = 1280
screenHeight = 720
FPS = 60

playerImage = pygame.image.load("player.png")
bulletImage = pygame.image.load("bullet.png")
moveSpeed = 5
playerBulletSpeed = 10

tileWidth = 160
tileHeight = 170


class Player:

    def __init__(self):
        # Hit box of the player, used to move the sprite and detect collisions.
        self.hitBox = pygame.Rect(300, 300, 50, 50)
        # Original image kept to avoid distortion caused by rotating.
        self.originalImage = playerImage
        # Will be set later.a
        self.rotatedImage = playerImage
        self.rotatedImageRect = playerImage.get_rect()

    def look(self):
        # Get the mouse position.
        mouseX, mouseY = pygame.mouse.get_pos()
        # Calculate the vector between the player and mouse.
        relativeX, relativeY = mouseX - self.hitBox.centerx, mouseY - self.hitBox.centery
        # Convert the vector into an angle (in radians). Must be inverted.
        radAngle = -math.atan2(relativeY, relativeX)
        # Convert the angle into degrees.
        degAngle = radAngle * 180 / math.pi
        # Create a rotated copy of the original image (if no copy, distortion happens).
        self.rotatedImage = pygame.transform.rotate(self.originalImage, int(degAngle))
        # Create a rect of the rotated image; its center is the center of a rect of the original image; its center is the player's position.
        self.rotatedImageRect = self.rotatedImage.get_rect(center=(self.hitBox.centerx, self.hitBox.centery))

    def move(self, velX, velY):
        # Move the player based on key presses, based on a move speed value.
        if velX != 0:
            self.collision(velX, 0)
        if velY != 0:
            self.collision(0, velY)

    def collision(self, velX, velY):
        self.hitBox.x += velX
        self.hitBox.y += velY

        for wall in wallList:
            if self.hitBox.colliderect(wall.hitBox):
                if velX > 0:
                    self.hitBox.right = wall.hitBox.left
                if velX < 0:
                    self.hitBox.left = wall.hitBox.right
                if velY > 0:
                    self.hitBox.bottom = wall.hitBox.top
                if velY < 0:
                    self.hitBox.top = wall.hitBox.bottom

    def fire(self):
        # Use the mouse and player positions to create a Vector2 between them. Normalise the vector to remove magnitude.
        mouseX, mouseY = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(mouseX - self.hitBox.centerx, mouseY - self.hitBox.centery).normalize()
        # Position of the player.
        position = self.hitBox.center
        # Instantiate a bullet; pass it the position and direction values.
        bulletInstance = Bullet(position, direction)
        playerBulletList.append(bulletInstance)

    def draw(self):
        # Blit the rotated image to the position of the rotated image's rect.
        screen.blit(self.rotatedImage, self.rotatedImageRect)
        # pygame.draw.rect(screen, (255, 255, 255), self.hitBox)


class Bullet:

    def __init__(self, position, direction):
        # The x and y values from the position tuple.
        self.hitBox = pygame.Rect(position[0], position[1], 6, 6)
        self.image = bulletImage
        self.bulletSpeed = playerBulletSpeed
        # The direction, a Vector2.
        self.direction = direction
        self.xPos = position[0]
        self.yPos = position[1]

    def move(self):
        # Movement with perfect collisions.
        # Loop this a number of times equal to the desired bullet speed.
        for i in range(playerBulletSpeed):
            # Move along the X axis by an amount specified in the direction (normalised vector).
            self.xPos += self.direction.x
            # Update the hit box's x position.
            self.hitBox.x = int(self.xPos)
            # Check the collision.
            self.collision()
            # If the collision function returns true:
            if self.collision():
                # Move the hit box out of the collider.
                self.hitBox.x -= 1
                # Reverse the x component of the hit box's direction (because it hit the left/right side of a wall).
                self.direction.x *= -1
        # Do the same for the y axis.
        for i in range(playerBulletSpeed):
            self.yPos += + self.direction.y
            self.hitBox.y = int(self.yPos)
            self.collision()
            if self.collision():
                self.hitBox.y -= 1
                self.direction.y *= -1

    def collision(self):
        # Loop through the walls, if the bullet has collided with one, return True.
        for wall in wallList:
            if self.hitBox.colliderect(wall.hitBox):
                return True
        return False

    def draw(self):
        # Draw the bullet at its updated position.
        screen.blit(self.image, self.hitBox)
        pygame.draw.rect(screen, (255, 255, 255), self.hitBox)


class Wall:

    def __init__(self, x, y):
        wallList.append(self)
        self.x = x
        self.y = y
        self.w = 160
        self.h = 170
        self.colour = 100, 100, 100
        self.hitBox = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        pygame.draw.rect(screen, self.colour, self.hitBox)


# Function for automatically building a level written as a list of strings.
def level_build():
    # X and y positions to feed into Wall()
    x = 0
    y = 0
    for row in level1:
        # Each column (letter in string), move the X by the tile size. If W, spawn a wall.
        for column in row:
            if column == "W":
                Wall(x, y)
            x += tileWidth
        # Each row (string in list), reset the X to 0 and increase the Y by the tile size.
        x = 0
        y += tileHeight


level1 = ["WWWWWWWWWWWW",
          "W          W",
          "W          W",
          "W          W",
          "W          W",
          "WWWWWWWWWWWW"]

wallList = []
playerInstance = Player()
playerBulletList = []
background = (200, 30, 30)

level_build()

running = True

while running:
    pygame.time.Clock().tick(FPS)

    for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            playerInstance.fire()

    screen.fill(background)

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        playerInstance.move(-moveSpeed, 0)
    if key[pygame.K_d]:
        playerInstance.move(moveSpeed, 0)
    if key[pygame.K_w]:
        playerInstance.move(0, -moveSpeed)
    if key[pygame.K_s]:
        playerInstance.move(0, moveSpeed)

    playerInstance.look()
    playerInstance.draw()

    for wall in wallList:
        wall.draw()

    for bullet in playerBulletList:
        bullet.move()
        bullet.draw()

    pygame.display.update()
    pygame.display.flip()  # 2 buffers: stuff that's going to draw, stuff that's already drawn. Flip turns the two.
