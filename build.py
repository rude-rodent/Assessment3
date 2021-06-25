import pygame
import info as i
import sprites as s

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
        # Must return a rect in order to be used as part of the draw() function in main.
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
    # Functions separated like layers -- player will always be on top of enemies, which will always be on top of walls.
    build_walls(level)
    place_enemies(level)
    place_player(level)
    place_buttons(level)


def build_walls(level):
    # X and y positions to feed into Wall()
    x = 0
    y = 0
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
            if column == "B":
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
    s.enemyList = []
    s.aliveEnemyList = []
    pygame.mixer.Sound.stop(i.houseAlarm)


def pause_overlay(pauseLevel):
    x = 0
    y = 0
    for row in pauseLevel:
        for column in row:
            if column == "C":
                s.Continue(x, y)
            if column == "M":
                s.Menu(x, y)
            x += i.tileWidth
        x = 0
        y += i.tileHeight


def pause_close():
    for sprite in s.pauseOverlayGroup:
        sprite.kill()
