import pygame
import math
import info as i

allSprites = pygame.sprite.Group()
wallList = []


class Player(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos, camera):
        pygame.sprite.Sprite.__init__(self)
        # Add player to the sprite group.
        allSprites.add(self)
        # Hit box of the player, used to move the sprite and detect collisions.
        # Original image kept to avoid distortion caused by rotating.
        self.originalImage = i.playerImage
        self.image = i.playerImage
        # A rect is required for the sprite's draw() function.
        self.rect = i.playerImage.get_rect()
        # Hit box used to control movement and collisions.
        self.hitBox = pygame.Rect(xPos, yPos, 50, 50)
        # Imported because some calculations require the camera's position.
        self.camera = camera

    def get_keys(self):
        # Calls the move method any time a key is pressed; send the appropriate move speed value.
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.move(-i.moveSpeed, 0)
        if key[pygame.K_d]:
            self.move(i.moveSpeed, 0)
        if key[pygame.K_w]:
            self.move(0, -i.moveSpeed)
        if key[pygame.K_s]:
            self.move(0, i.moveSpeed)

    def update(self):
        self.get_keys()
        self.look()

    def look(self):
        # Get the mouse position.
        mouseX, mouseY = pygame.mouse.get_pos()
        # Calculate the vector between the player and mouse. Add the player's hit box to the camera's top left coordinates to keep the position relative to the screen.
        relativeX, relativeY = mouseX - (self.hitBox.centerx + self.camera.rect.x), mouseY - (self.hitBox.centery + self.camera.rect.y)
        # Convert the vector into an angle (in radians). Must be inverted.
        radAngle = -math.atan2(relativeY, relativeX)
        # Convert the angle into degrees.
        degAngle = radAngle * 180 / math.pi
        # Create a rotated copy of the original image (if no copy, distortion happens).
        self.image = pygame.transform.rotate(self.originalImage, int(degAngle))
        # Create a rect of the rotated image; its center is the center of a rect of the original image; its center is the player's position.
        self.rect = self.image.get_rect(center=(self.hitBox.centerx, self.hitBox.centery))

    def move(self, velX, velY):
        # Perfect collisions aren't needed here as the player is large and moves slowly.
        # Call the collision method for both axis separately.
        if velX != 0:
            self.collision(velX, 0)
        if velY != 0:
            self.collision(0, velY)

    def collision(self, velX, velY):
        # Move the player along 1 axis at a time.
        self.hitBox.x += velX
        self.hitBox.y += velY

        for wall in wallList:
            # Check for collisions with any walls.
            if self.hitBox.colliderect(wall.rect):
                # If a collision is detected, check which way the player was moving when it happened.
                if velX > 0:
                    # If the player was moving right, move their hit box to the left side of the wall.
                    self.hitBox.right = wall.rect.left
                if velX < 0:
                    self.hitBox.left = wall.rect.right
                if velY > 0:
                    self.hitBox.bottom = wall.rect.top
                if velY < 0:
                    self.hitBox.top = wall.rect.bottom

    def fire(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        # Use the mouse and player positions to create a Vector2 between them. Normalise the vector to remove magnitude.
        # Add player's position to camera's top left to keep the positions relative to the screen size.
        direction = pygame.math.Vector2(mouseX - (self.hitBox.centerx + self.camera.rect.x), mouseY - (self.hitBox.centery + self.camera.rect.y)).normalize()
        # Position of the player.
        position = self.hitBox.center
        # Instantiate a bullet; pass it the position and direction values.
        Bullet(position, direction)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        # Add the bullet to the sprite group.
        allSprites.add(self)
        # The x and y values from the position tuple.
        self.xPos = position[0]
        self.yPos = position[1]
        # Create a rect for the bullet, will control position & collisions.
        self.rect = pygame.Rect(position[0], position[1], 6, 6)
        self.image = i.bulletImage
        self.bulletSpeed = i.playerBulletSpeed
        # The direction, a Vector2.
        self.direction = direction


    def update(self):
        # Movement with perfect collisions.
        # Loop this a number of times equal to the desired bullet speed.
        for num in range(i.playerBulletSpeed):
            # Move along the X axis by an amount specified in the direction (normalised vector).
            self.xPos += self.direction.x
            # Update the hit box's x position.
            self.rect.x = int(self.xPos)
            # Check the collision.
            self.collision()
            # If the collision function returns true:
            if self.collision():
                # Move the hit box out of the collider.
                self.rect.x -= 1
                # Reverse the x component of the hit box's direction (because it hit the left/right side of a wall); makes the bullet bounce.
                self.direction.x *= -1
        # Do the same for the y axis.
        for num in range(i.playerBulletSpeed):
            self.yPos += + self.direction.y
            self.rect.y = int(self.yPos)
            self.collision()
            if self.collision():
                self.rect.y -= 1
                self.direction.y *= -1

    def collision(self):
        # Loop through the walls, if the bullet has collided with one, return True.
        for wall in wallList:
            if self.rect.colliderect(wall.rect):
                return True
        return False


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Add the wall to the wall list and sprite group.
        wallList.append(self)
        allSprites.add(self)
        self.colour = 100, 100, 100
        # Set the wall's rect based on tile size values stored in info.
        self.rect = pygame.Rect(x, y, i.tileWidth, i.tileHeight)
        self.image = pygame.Surface((i.tileWidth, i.tileHeight))
