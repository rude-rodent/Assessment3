import pygame
import levels as l

caption = "Bouncing Bullets"
screenWidth = 1280
screenHeight = 720
FPS = 60
BGColour = (100, 100, 100)

screen = pygame.display.set_mode((screenWidth, screenHeight))  # Sets resolution.
currentLevel = l.menu  # Set to the first stage of the game (main menu).

# Load all the images for the sprites.
bulletImage = pygame.image.load("bullet.png")
startImage = pygame.image.load("start.png")
startHover = pygame.image.load("startdark.png")
optionsImage = pygame.image.load("options.png")
optionsHover = pygame.image.load("optionsdark.png")
quitImage = pygame.image.load("quit.png")
quitHover = pygame.image.load("quitdark.png")

# List comprehension to load in the animation frames (they are saved as numbers in folders).
playerIdle = [pygame.image.load("Assets/Player/idle/" + str(i + 1) + ".png") for i in range(5)]
playerWalk = [pygame.image.load("Assets/Player/walk/" + str(i + 1) + ".png") for i in range(5)]
playerShoot = [pygame.image.load("Assets/Player/shoot/" + str(i + 1) + ".png") for i in range(3)]
playerReload = [pygame.image.load("Assets/Player/reload/" + str(i + 1) + ".png") for i in range(8)]

enemyIdle = pygame.image.load("Assets/Guard/walk/1.png")
enemyWalk = [pygame.image.load("Assets/Guard/walk/" + str(i + 1) + ".png") for i in range(10)]
enemyDeath = [pygame.image.load("Assets/Guard/death/" + str(i + 1) + ".png") for i in range(4)]

# Various values that can be tweaked.
moveSpeed = 5
playerBulletSpeed = 10
enemySpeed = 3
maxBullets = 10

tileWidth = 128
tileHeight = 128

# Variable used to reset the score back to its original value.
startingScore = 1000
# Score that can be changed during the game.
score = 1000

# Text that will be displayed in the same area; simpler to have one variable that can display either form of text.
# Will either display "R to reload" if the player's gun is empty, or "R to restart" if the player is dead.
reloadOrRestartText = ""
