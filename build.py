import pygame
import info as i
import sprites as s
import levels as l

cameraInstance = ""
playerInstance = ""


class Camera:

    def __init__(self, level):
        # Length of a string (row) in the level list * tile width.
        self.mapWidth = len(level[0]) * i.tileWidth
        # Number of strings (columns) in the level list * tile height.
        self.mapHeight = len(level) * i.tileHeight
        # Setting up the camera as a rect.
        self.rect = pygame.Rect(0, 0, self.mapWidth, self.mapHeight)

    def offset(self, sprite):
        # Returns the sprite's rect after moving it relative to the camera.
        # Must return a rect in order to be used as part of the sprite's draw() function.
        return sprite.rect.move(self.rect.topleft)

    def update(self, sprite):
        # Setting the position of the camera's rect based on the player's position & the screen.
        x = -sprite.rect.centerx + int(i.screenWidth/2)
        y = -sprite.rect.centery + int(i.screenHeight/2)

        # Setting upper & lower limits for the camera.
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.mapWidth - i.screenWidth), x)
        y = max(-(self.mapHeight - i.screenHeight), y)
        # Update the position of the rect.
        self.rect = pygame.Rect(x, y, self.mapWidth, self.mapHeight)


# Function for automatically building a level written as a list of strings.
def level_build(level):
    # Functions separated like layers -- player will always be on top of enemies, which will always be on top of walls, etc.
    background(level)
    build_walls(level)
    place_enemies(level)
    place_player(level)
    place_buttons(level)


def background(level):
    # Spawn a background based on the current level.
    if level == l.title:
        s.Background(0)
    if level == l.level1:
        s.Background(1)
    elif level == l.level2:
        s.Background(2)
    elif level == l.level3:
        s.Background(3)
    else:
        # Some levels don't have backgrounds (e.g. main menu).
        return


def build_walls(level):
    # X and y positions to feed into Wall()
    x = 0
    y = 0
    # Each string (row) in the list (level)...
    for row in level:
        # Each column (letter in string), move the X by the tile size. Spawn sprite instances according to letters (see level.py for key).
        for column in row:
            if column == "W":
                s.Wall(x, y)
            if column == "H":
                s.Door(x, y, "hor")
            if column == "V":
                s.Door(x, y, "ver")
            x += i.tileWidth
        # Each row (string in list), reset the X to 0 and increase the Y by the tile size.
        x = 0
        y += i.tileHeight


# Same code as build_walls()
def place_enemies(level):
    x = 0
    y = 0
    for row in level:
        for column in row:
            if column == "E":
                s.Enemy(x, y)
            if column == "B":
                s.Boss(x, y)
            x += i.tileWidth
        x = 0
        y += i.tileHeight


# Same code as build_walls()
def place_player(level):
    # Using global variables so the camera & player instances can be altered in the main loop.
    global cameraInstance
    global playerInstance
    x = 0
    y = 0
    for row in level:
        for column in row:
            if column == "P":
                cameraInstance = Camera(level)
                playerInstance = s.Player(x, y, cameraInstance)
            x += i.tileWidth
        x = 0
        y += i.tileHeight


# Same code as build_walls()
def place_buttons(level):
    x = 0
    y = 0
    for row in level:
        for column in row:
            if column == "S":
                s.Start(x, y)
            if column == "Q":
                s.Quit(x, y)
            if column == "?":
                s.HowToPlay(x, y)
            if column == "N":
                s.BarSlider(x, y)
            if column == "I":
                s.Instructions(x, y)
            x += i.tileWidth
        x = 0
        y += i.tileHeight


# Function for removing all sprites, effectively clearing the entire screen.
def clear_level():
    for sprite in s.allSprites:
        sprite.kill()
    # Also reset any sprite lists.
    s.enemyList = []
    s.aliveEnemyList = []
    s.bulletList = []
    # Also turn off the house alarm, if it's playing.
    pygame.mixer.Sound.stop(i.houseAlarm)


# Function for building an overlay on top of the existing level.
# Used for pausing, proceeding to next level, dying, etc.
def overlay_build(overlayLevel):
    x = 0
    y = 0
    for row in overlayLevel:
        for column in row:
            if column == "C":
                s.Continue(x, y)
            if column == "N":
                s.BarSlider(x, y)
            if column == "M":
                s.Menu(x, y)
            x += i.tileWidth
        x = 0
        y += i.tileHeight


# Function to destroy the overlay.
def overlay_close():
    for sprite in s.overlayGroup:
        sprite.kill()
