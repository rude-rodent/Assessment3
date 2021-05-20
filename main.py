import pygame
import sys
import math

pygame.init()
pygame.display.set_caption("Assessment 3")
screen = pygame.display.set_mode((1280, 720))  # Sets resolution.

screenWidth = 1280
screenHeight = 720
FPS = 60

playerImage = pygame.image.load("player.png")
bulletImage = pygame.image.load("bullet.png")
moveSpeed = 5
playerBulletSpeed = 10


class Player:

    def __init__(self):
        # Hit box of the player, used to move the sprite and detect collisions.
        self.hitBox = pygame.Rect(30, 30, 50, 50)
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
        degAngle = radAngle * 180/math.pi
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

    def move(self):
        # Add the x and y values from the direction Vector2, multiplied by the bullet speed.
        self.hitBox.x += self.direction.x * self.bulletSpeed
        self.hitBox.y += self.direction.y * self.bulletSpeed

    def draw(self):
        # Draw the bullet at its updated position.
        screen.blit(self.image, self.hitBox)
        pygame.draw.rect(screen, (255, 255, 255), self.hitBox)


class Wall:

    def __init__(self):
        wallList.append(self)
        self.x = 300
        self.y = 300
        self.w = 300
        self.h = 300
        self.colour = 100, 100, 100
        self.hitBox = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        pygame.draw.rect(screen, self.colour, self.hitBox)


wallList = []
wallInstance = Wall()
playerInstance = Player()
playerBulletList = []
background = (200, 30, 30)

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
        for wall in wallList:
            if bullet.hitBox.colliderect(wall.hitBox):
                displacement = pygame.math.Vector2(bullet.hitBox.centerx - wall.hitBox.centerx, bullet.hitBox.centery - wall.hitBox.centery)
                xExtent = wall.hitBox.w/2
                yExtent = wall.hitBox.h/2
                xUnit = pygame.math.Vector2((wall.hitBox.midright[0] - wall.hitBox.centerx), (wall.hitBox.midright[1] - wall.hitBox.centery)).normalize()
                yUnit = pygame.math.Vector2((wall.hitBox.midbottom[0] - wall.hitBox.centerx), (wall.hitBox.midbottom[1] - wall.hitBox.centery)).normalize()
                xDistance = pygame.math.Vector2.dot(displacement, xUnit)
                print(xDistance)
                if xDistance >= xExtent:
                    xDistance = xExtent
                if xDistance <= -xExtent:
                    xDistance = -xExtent
                yDistance = pygame.math.Vector2.dot(displacement, yUnit)
                print(yDistance)
                if yDistance >= yExtent:
                    yDistance = yExtent
                if yDistance <= -yExtent:
                    yDistance = -yExtent
                print(xDistance, yDistance)
                # BUG: if xDistance == xExtent or yDistance == yExtent, normal = 0?
                collidePoint = pygame.math.Vector2(wall.hitBox.center + xDistance * xUnit + yDistance * yUnit)
                normal = pygame.math.Vector2(bullet.hitBox.center - collidePoint).normalize()
                
                # r = d -2(d.n)n
                newDirection = bullet.direction - 2 * pygame.math.Vector2.dot(bullet.direction, normal) * normal
                bullet.direction = newDirection

        bullet.move()
        bullet.draw()

    pygame.display.update()
    pygame.display.flip()  # 2 buffers: stuff that's going to draw, stuff that's already drawn. Flip turns the two.
