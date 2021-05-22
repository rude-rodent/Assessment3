import pygame
import info as i
import sprites as s
import levels as l

# Length of a string (row) in the level list * tile width.
mapWidth = len(l.level1[0]) * i.tileWidth
# Number of strings (columns) in the level list * tile height.
mapHeight = len(l.level1) * i.tileHeight


class Camera:

    def __init__(self):
        self.width = mapWidth
        self.height = mapHeight
        # Setting up the camera as a rect.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def offset(self, sprite):
        # Returns the sprite's rect after moving it relative to the camera.
        # Must return a rect in order to be used as part of the draw() function in main.
        return sprite.rect.move(self.rect.topleft)

    def update(self, sprite):
        # Setting the position of the camera's rect based on the player's position & the screen.
        x = -sprite.rect.centerx + int(i.screenWidth/2)
        y = -sprite.rect.centery + int(i.screenHeight/2)

        # Setting upper & lower limits for the camera.
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - i.screenWidth), x)
        y = max(-(self.height - i.screenHeight), y)
        # Update the position of the rect.
        self.rect = pygame.Rect(x, y, self.width, self.height)


# Function for automatically building a level written as a list of strings.
def level_build():
    # X and y positions to feed into Wall()
    x = 0
    y = 0
    for row in l.level1:
        # Each column (letter in string), move the X by the tile size. If W, spawn a wall.
        for column in row:
            if column == "W":
                s.Wall(x, y)
            x += i.tileWidth
        # Each row (string in list), reset the X to 0 and increase the Y by the tile size.
        x = 0
        y += i.tileHeight
