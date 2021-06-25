import pygame
import sys
import math
import random
import info as i

# Groups used in the main loop for various identification purposes.
# All groups (no lists) so that sprite.kill() removes a sprite from everything simultaneously.
allSprites = pygame.sprite.Group()
wallGroup = pygame.sprite.Group()
obstacleGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
buttonGroup = pygame.sprite.Group()
startGroup = pygame.sprite.Group()
howToPlayGroup = pygame.sprite.Group()
pauseOverlayGroup = pygame.sprite.Group()
continueGroup = pygame.sprite.Group()
menuGroup = pygame.sprite.Group()

# Integers used to control which frame the player's animation is on. Must be global or they will be reset to 0 every time the function is called.
idleCount = 0
walkCount = 0
shootCount = 0
reloadCount = 0

# Groups only allow access to the self.rect.
# Enemies have 2 rect attributes: a small one to detect collisions with bullets & walls, and a larger one for the torchlight surrounding them.
# The enemies need to be in a list so that I can access their 2nd hit box, visionRect, to detect collision with the player.
# 2 enemy groups so only alive enemies can collide with the player, but dead enemies can still be detected by alive enemies.
# Also need access to bullet's number of bounces.
aliveEnemyList = []
enemyList = []
bulletList = []

normalisedValue = 0.5


class Player(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos, camera):
        pygame.sprite.Sprite.__init__(self)
        # Add player to the sprite group.
        allSprites.add(self)
        # Hit box of the player, used to move the sprite and detect collisions.
        # Original image kept to avoid distortion caused by rotating.
        self.originalImage = i.playerIdle[0]
        self.image = i.playerIdle[0]
        # A rect is required for the sprite's draw() function.
        self.rect = i.playerIdle[0].get_rect()
        # Hit box used to control movement and collisions.
        self.hitBox = pygame.Rect(xPos, yPos, 50, 50)
        # Imported because some calculations require the camera's position.
        self.camera = camera
        # Number of bullets in the player's magazine.
        self.magazine = 6
        # Booleans for animations.
        self.alive = True
        self.walking = False
        self.shooting = False
        self.reloading = False

    def update(self):
        self.get_keys()
        self.animation()
        self.look()
        self.enemy_collide()
        self.bullet_collide()
        self.check_magazine()

    def get_keys(self):
        # Calls the move method any time a key is pressed; send the appropriate move speed value.
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.move(-i.moveSpeed, 0)
            self.walking = True
        if key[pygame.K_d]:
            self.move(i.moveSpeed, 0)
            self.walking = True
        if key[pygame.K_w]:
            self.move(0, -i.moveSpeed)
            self.walking = True
        if key[pygame.K_s]:
            self.move(0, i.moveSpeed)
            self.walking = True

        if not key[pygame.K_a] and not key[pygame.K_d] and not key[pygame.K_w] and not key[pygame.K_s]:
            self.walking = False

        if key[pygame.K_r]:
            self.reloading = True

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

        for obstacle in obstacleGroup:
            # Check for collisions with any walls.
            if self.hitBox.colliderect(obstacle.rect):
                # If a collision is detected, check which way the player was moving when it happened.
                if velX > 0:
                    # If the player was moving right, move their hit box to the left side of the wall.
                    self.hitBox.right = obstacle.rect.left
                if velX < 0:
                    self.hitBox.left = obstacle.rect.right
                if velY > 0:
                    self.hitBox.bottom = obstacle.rect.top
                if velY < 0:
                    self.hitBox.top = obstacle.rect.bottom

    def check_magazine(self):
        if self.magazine >= 1:
            # Magazine is not empty; don't display reload text.
            i.reloadOrRestartText = ""
        # If magazine is empty, display reload prompt.
        else:
            # Don't overwrite "R to restart!"; that takes priority.
            if i.reloadOrRestartText == "":
                i.reloadOrRestartText = "R to reload!"

    def fire(self):
        # If player is dead, reloadOrRestartText will show the restart message (that takes priority).
        if self.alive:
            if self.magazine >= 1:
                self.shooting = True
                mouseX, mouseY = pygame.mouse.get_pos()
                # Use the mouse and player positions to create a Vector2 between them. Normalise the vector to remove magnitude.
                # Add player's position to camera's top left to keep the positions relative to the screen size.
                direction = pygame.math.Vector2(mouseX - (self.hitBox.centerx + self.camera.rect.x),
                                                mouseY - (self.hitBox.centery + self.camera.rect.y)).normalize()
                # Position of the player.
                position = self.hitBox.center
                # Instantiate a bullet; pass it the position and direction values.
                Bullet(position, direction)
                # Remove one bullet from the magazine.
                self.magazine -= 1
                # Remove 5 from the total score (score starts at 1000 and decreases with time and with each bullet fired).
                i.score -= 5
                pygame.mixer.Sound.play(i.shootSound)

    def enemy_collide(self):
        # If the enemy walks into the enemy's torchlight, it's game over.
        for enemy in aliveEnemyList:
            if self.hitBox.colliderect(enemy.visionRect) and enemy.alive:
                self.alive = False
                # If you got detected by a guard, play the house alarm.
                pygame.mixer.Sound.play(i.houseAlarm, -1)

    def bullet_collide(self):
        # Check if the player collided with any bullets.
        for bullet in bulletList:
            if self.hitBox.colliderect(bullet.rect):
                # The bullet can only kill the player if it's bounced at least one time.
                # Because it's instantiated from the center of the player's hit box; it would immediately collide with & kill the player.
                if bullet.bounces >= 1:
                    bullet.alive = False
                    self.alive = False
                    # If you shot yourself, play the death grunt.
                    pygame.mixer.Sound.play(i.guardDeathSound)

    def animation(self):
        global idleCount
        global walkCount
        global shootCount
        global reloadCount
        if self.walking:
            # If the counter is greater than the number of images in the list (5) * how long each image should be blit for (5 frames)...
            if walkCount + 1 >= 25:
                # Set the walk count back to 0, restarting the animation loop.
                walkCount = 0
            else:
                # Otherwise, set the sprite's original image (so it can be rotated in self.look()) to the appropriate image in the animation.
                # I'm int dividing the index by 5 because I want each image to be played for 5 frames before changing.
                self.originalImage = i.playerWalk[walkCount // 5]
                walkCount += 1

        # Identical code to the walking animation; this is for idling.
        if not self.walking:
            # This animation plays slower than walking, each image (5) being played for 12 frames.
            if idleCount + 1 >= 60:
                idleCount = 0
            else:
                self.originalImage = i.playerIdle[idleCount // 12]
                idleCount += 1

        # This animation does NOT loop; it plays through once.
        if self.shooting:
            # This animation only has 3 images, and each image plays for 5 frames, so the counter can't exceed 15.
            if shootCount + 1 >= 15:
                # Set the condition that starts this animation to false, thereby stopping it from looping.
                self.shooting = False
                shootCount = 0
            else:
                self.originalImage = i.playerShoot[shootCount // 5]
                shootCount += 1

        if self.reloading:
            if reloadCount + 1 >= 24:
                pygame.mixer.Sound.play(i.reloadSound)
                self.reloading = False
                # Set the magazine size back to 6 after the reload animation has played fully.
                self.magazine = 6
                reloadCount = 0
            else:
                self.originalImage = i.playerReload[reloadCount // 3]
                reloadCount += 1


class Bullet(pygame.sprite.Sprite):

    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        # Add the bullet to the sprite group.
        allSprites.add(self)
        bulletGroup.add(self)
        bulletList.append(self)
        # The x and y values from the position tuple.
        self.xPos = position[0]
        self.yPos = position[1]
        # Create a rect for the bullet, will control position & collisions.
        self.rect = pygame.Rect(position[0], position[1], 6, 6)
        self.image = i.bulletImage
        self.bulletSpeed = i.playerBulletSpeed
        # The direction, a Vector2.
        self.direction = direction
        self.alive = True
        self.bounces = 0

    def update(self):
        self.check_alive()
        self.move()
        # Movement with perfect collisions.
        # Loop this a number of times equal to the desired bullet speed.

    def move(self):
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
                # Increase the number of bounces.
                self.bounces += 1
        # Do the same for the y axis.
        for num in range(i.playerBulletSpeed):
            self.yPos += + self.direction.y
            self.rect.y = int(self.yPos)
            self.collision()
            if self.collision():
                self.rect.y -= 1
                self.direction.y *= -1
                self.bounces += 1

    def collision(self):
        # Loop through the walls, if the bullet has collided with one, return True.
        for wall in wallGroup:
            if self.rect.colliderect(wall.rect):
                pygame.mixer.Sound.play(i.bulletBounceSound)
                return True
        return False

    def check_alive(self):
        # Bullets only bounce 3 times before being destroyed.
        if self.bounces >= 3:
            self.alive = False
        # To avoid lag/chaos, a limited number of bullets are allowed on screen.
        # Check the # of bullets, if > 10, set the oldest bullet's "alive" bool to false.
        if len(bulletGroup) > i.maxBullets:
            bulletGroup.sprites()[0].alive = False
        # Go through the bulletList and delete any bullets with alive = false. Also delete from the sprite group.
        for bullet in bulletGroup:
            if not bullet.alive:
                bulletGroup.remove(bullet)
                allSprites.remove(bullet)
                bulletList.remove(bullet)


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Add the wall to the wall group, obstacle group, and sprite group.
        wallGroup.add(self)
        obstacleGroup.add(self)
        allSprites.add(self)
        # Set the wall's rect based on tile size values stored in info.
        self.rect = pygame.Rect(x, y, i.tileWidth, i.tileHeight)
        self.image = i.wallImage


class Door(pygame.sprite.Sprite):

    def __init__(self, x, y, axis):
        pygame.sprite.Sprite.__init__(self)
        # Add to the obstacle group and sprite group.
        obstacleGroup.add(self)
        allSprites.add(self)
        # The axis will be the orientation of the door (horizontal or vertical).
        self.axis = axis
        self.rect = pygame.Rect(x, y, i.tileWidth, i.tileHeight)
        # Doors have a different sprite depending on their axis.
        if self.axis == "hor":
            self.image = i.doorHorImage
        elif self.axis == "ver":
            self.image = i.doorVerImage
        self.broken = False

    def update(self):
        if not self.broken:
            self.door_break_check()

    def door_break_check(self):
        # Loop through the bullets, check for a collision.
        for bullet in bulletList:
            if self.rect.colliderect(bullet.rect):
                self.broken = True
                # Kill the bullet.
                bullet.alive = False
                # Break open the door.
                self.door_open()
                pygame.mixer.Sound.play(i.doorBreakSound)
                # Remove the door from the obstacle group; the player and enemies can now walk through it.
                obstacleGroup.remove(self)

    def door_open(self):
        # Update the door's image to a broken version of it.
        if self.axis == "hor":
            self.image = i.doorHorBrokenImage
        elif self.axis == "ver":
            self.image = i.doorVerBrokenImage


class Enemy(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos):
        pygame.sprite.Sprite.__init__(self)
        # Add the enemy to the sprite group.
        allSprites.add(self)
        enemyList.append(self)
        aliveEnemyList.append(self)
        # Save an original version of the image for use in rotation (like the player).
        self.originalImage = i.enemyIdle
        # Give the enemy a hit box, xPos and yPos assigned in the level building function.
        self.hitBox = pygame.Rect(xPos, yPos, 80, 80)
        # The rotatable image & rect that will be used to draw the enemy.
        self.image = i.enemyIdle
        self.rect = self.image.get_rect()
        # Used for collision with the player (player should be detected if they touch the light around the enemy).
        self.visionRect = pygame.Rect(xPos, yPos, 225, 225)
        # List of possible directions -- the enemy will only move up, down, left, or right.
        self.possibleDirections = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # Set the enemy's initial direction.
        self.direction = random.choice(self.possibleDirections)
        self.canMove = 0
        self.walking = False
        self.alive = True
        self.walkCount = 0
        self.deathCount = 0

    def update(self):
        self.animation()
        if self.alive:
            # Use the smallest rect (hitBox) for bullet collisions -- the enemy shouldn't die if the bullet just hits its torchlight.
            # Loop through the bullets.
            for bullet in bulletList:
                # If a collision occurred:
                if self.hitBox.colliderect(bullet.rect):
                    # Delete enemy from all groups, set the bullet's alive status to false.
                    bullet.alive = False
                    self.alive = False
                    aliveEnemyList.remove(self)
                    pygame.mixer.Sound.play(i.guardDeathSound)
            # Move and look if the wait timer has run out -- see self.turn()
            if self.canMove <= pygame.time.get_ticks():
                self.walking = True
                self.move()
                self.look()
            else:
                self.walking = False
            self.visionRect.center = self.hitBox.center
        else:
            self.look()

    def look(self):
        # Rotate the enemy's image based on its direction.
        if self.direction == (1, 0):
            # If the enemy is facing right, the image doesn't need to be rotated.
            self.image = self.originalImage
        if self.direction == (-1, 0):
            self.image = pygame.transform.rotate(self.originalImage, 180)
        if self.direction == (0, 1):
            self.image = pygame.transform.rotate(self.originalImage, 270)
        if self.direction == (0, -1):
            self.image = pygame.transform.rotate(self.originalImage, 90)
        # Create a new rotated rect with its center in the middle of the enemy's hit box.
        self.rect = self.image.get_rect(center=self.hitBox.center)

    def move(self):
        # Create a Vector2 for the enemy's velocity.
        velocity = pygame.Vector2(self.direction[0], self.direction[1]) * i.enemySpeed
        # Same as player, check collisions & move on individual axes.
        if velocity.x != 0:
            self.collisions(velocity.x, 0)
        if velocity.y != 0:
            self.collisions(0, velocity.y)

        # Random chance for the enemy to stop and turn based on a time interval.
        if pygame.time.get_ticks() % 150 == 0:
            turnChance = random.randint(1, 5)
            if turnChance == 1:
                self.turn()

    def collisions(self, velX, velY):
        # Move the enemy's hit box.
        self.hitBox.x += velX
        self.hitBox.y += velY

        # Loop through the walls.
        for obstacle in obstacleGroup:
            # If there is a collision:
            if self.hitBox.colliderect(obstacle.rect):
                # Find which way the enemy is moving.
                if velX > 0:
                    # Push the enemy's hit box out of the wall.
                    self.hitBox.right = obstacle.rect.left - i.enemySpeed
                if velX < 0:
                    self.hitBox.left = obstacle.rect.right + i.enemySpeed
                if velY > 0:
                    self.hitBox.bottom = obstacle.rect.top - i.enemySpeed
                if velY < 0:
                    self.hitBox.top = obstacle.rect.bottom + i.enemySpeed
                # Make the enemy change direction.
                self.turn()

        # If a guard's torchlight touches a dead guard, they will raise the alarm and the game will end.
        for enemy in enemyList:
            if self.visionRect.colliderect(enemy.hitBox):
                if not enemy.alive:
                    pass
                    # GAME OVER STATE.

    def turn(self):
        # Sets a timer that stops the enemy from moving for 1.5 seconds.
        self.canMove = pygame.time.get_ticks() + 1500
        # Change the enemy's direction, but don't turn the enemy towards the wall they just hit.
        oldDirection = self.direction
        # Temporarily remove the enemy's current direction from the list of possible directions.
        self.possibleDirections.remove(oldDirection)
        # Choose a new random direction.
        self.direction = random.choice(self.possibleDirections)
        # Add the old direction back to the list.
        self.possibleDirections.append(oldDirection)

    def animation(self):

        if not self.alive:
            if self.deathCount >= 24:
                self.originalImage = i.enemyDeath[3]
            else:
                self.originalImage = i.enemyDeath[self.deathCount // 6]
                self.deathCount += 1
        else:
            if self.walking:
                # If the counter is greater than the number of images in the list (5) * how long each image should be blit for (5 frames)...
                if self.walkCount + 1 >= 200:
                    # Set the walk count back to 0, restarting the animation loop.
                    self.walkCount = 0
                else:
                    # Otherwise, set the sprite's original image (so it can be rotated in self.look()) to the appropriate image in the animation.
                    # I'm int dividing the index by 5 because I want each image to be played for 5 frames before changing.
                    self.originalImage = i.enemyWalk[self.walkCount // 20]
                    self.walkCount += 1


# Parent class for buttons.
class Button(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Add the button to the sprite group.
        allSprites.add(self)
        # Add the button to the button group; we can loop through them in main.
        buttonGroup.add(self)
        # Boolean to determine whether the button is clicked.
        self.clicked = False

    def is_clicked(self):
        # Checks whether the cursor is over the button. Gets called on the menu screen when the mouse button is clicked.
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.clicked = True


# Child classes for each button type.
class Start(Button):

    # X and Y supplied by b.level_build().
    def __init__(self, x, y):
        super().__init__()
        # Give the button an image & rect so it can be drawn.
        self.image = i.startImage
        self.rect = self.image.get_rect(topleft=(x, y))
        # Start button needs to be accessible in the main loop, so put it in its own separate group.
        startGroup.add(self)

    def update(self):
        # Change the button's colour if it's moused over.
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = i.startHover
        else:
            self.image = i.startImage


class Quit(Button):

    def __init__(self, x, y):
        super().__init__()
        self.image = i.quitImage
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = i.quitHover
        else:
            self.image = i.quitImage
        # Quits the game if clicked.
        if self.clicked:
            pygame.display.quit()
            pygame.quit()
            sys.exit()


class HowToPlay(Button):

    def __init__(self, x, y):
        super().__init__()
        self.image = i.howToPlayImage
        self.rect = self.image.get_rect(topleft=(x, y))
        # This button's functionality on click needs to be determined in the main loop, so add it to a group we can access there.
        howToPlayGroup.add(self)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = i.howToPlayHover
        else:
            self.image = i.howToPlayImage


class Continue(Button):

    def __init__(self, x, y):
        super().__init__()
        self.image = i.continueImage
        self.rect = self.image.get_rect(topleft=(x, y))
        # This button's functionality on click needs to be determined in the main loop, so add it to a group we can access there.
        pauseOverlayGroup.add(self)
        continueGroup.add(self)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = i.continueHover
        else:
            self.image = i.continueImage


class Menu(Button):

    def __init__(self, x, y):
        super().__init__()
        self.image = i.menuImage
        self.rect = self.image.get_rect(topleft=(x, y))
        # This button's functionality on click needs to be determined in the main loop, so add it to a group we can access there.
        pauseOverlayGroup.add(self)
        menuGroup.add(self)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = i.menuHover
        else:
            self.image = i.menuImage


class BarSlider(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        allSprites.add(self)
        self.image = i.barSliderImage
        self.rect = self.image.get_rect(topleft=(x, y))  # y + i.tileHeight/3 to center the slider's y position.
        self.x = x
        self.y = y
        self.width = self.image.get_width() + self.x
        self.hasKnob = False

    def spawn_knob(self):
        Knob(self.x, self.width, self.y)

    def update(self):
        # Spawn a knob for the slider; only do this if it doesn't already have one.
        if not self.hasKnob:
            self.spawn_knob()
            self.hasKnob = True


class Knob(Button):

    def __init__(self, xMin, xMax, y):
        super().__init__()
        self.image = i.knobImage
        # Set starting pos to halfway along the slider.
        self.rect = self.image.get_rect(bottomleft=((xMax + xMin)/2, y + i.tileHeight - 3))
        self.min = xMin
        self.max = xMax
        self.canMove = False

    def update(self):
        global normalisedValue
        self.on_click()
        self.move()
        # The position of the knob on the slider, normalised to be between 0 and 1.
        normalisedValue = (self.rect.x - self.min) / (self.max - self.min)

    def on_click(self):
        # If the knob is clicked:
        if self.clicked:
            # If the knob is not already being moved by the mouse:
            if not self.canMove:
                # Allow the knob to be moved by the mouse.
                self.canMove = True
                # Turn clicked back to false so that the user can click on this multiple times.
                self.clicked = False
            # If the knob is already being moved by the mouse:
            else:
                # Stop it from moving.
                self.canMove = False
                self.clicked = False

    def move(self):
        if self.canMove:
            # Only move the knob along the X axis -- its Y should never change.
            self.rect.x = pygame.mouse.get_pos()[0]
            # Clamp the knob's position so it can't go past the edges of the slider.
            if self.rect.x + self.rect.width > self.max:  # + width because self.rect.x refers to the left side of the knob.
                self.rect.x = self.max - self.rect.width
            if self.rect.x < self.min:
                self.rect.x = self.min


class Instructions(pygame.sprite.Sprite):

    # The instructions are displayed in a simple image; no functionality needed here besides the built-in sprite blit.
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        allSprites.add(self)
        self.image = i.instructionsImage
        self.rect = self.image.get_rect(topleft=(x, y))
