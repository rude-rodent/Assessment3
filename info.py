import pygame
import levels as l

caption = "Bouncing Bullets"
screenWidth = 1280
screenHeight = 720
FPS = 60
BGColour = (200, 200, 200)

screen = pygame.display.set_mode((screenWidth, screenHeight))  # Sets resolution.
currentLevel = l.menu  # Set to the first stage of the game (main menu).

# Load all the images for the sprites.
bulletImage = pygame.image.load("bullet.png")
enemyImage = pygame.image.load("enemy.png")
startImage = pygame.image.load("start.png")
startDark = pygame.image.load("startdark.png")
optionsImage = pygame.image.load("options.png")
optionsDark = pygame.image.load("optionsdark.png")
quitImage = pygame.image.load("quit.png")
quitDark = pygame.image.load("quitdark.png")

playerIdle = [pygame.image.load("Assets/Player/idle/1.png"), pygame.image.load("Assets/Player/idle/2.png"),
              pygame.image.load("Assets/Player/idle/3.png"), pygame.image.load("Assets/Player/idle/4.png"),
              pygame.image.load("Assets/Player/idle/5.png")]
playerWalk = [pygame.image.load("Assets/Player/walk/1.png"), pygame.image.load("Assets/Player/walk/2.png"),
              pygame.image.load("Assets/Player/walk/3.png"), pygame.image.load("Assets/Player/walk/4.png"),
              pygame.image.load("Assets/Player/walk/5.png")]
playerShoot = [pygame.image.load("Assets/Player/shoot/1.png"), pygame.image.load("Assets/Player/shoot/2.png"),
               pygame.image.load("Assets/Player/shoot/3.png")]

# Various values that can be tweaked.
moveSpeed = 5
playerBulletSpeed = 10
enemySpeed = 3
maxBullets = 10

tileWidth = 128
tileHeight = 128
