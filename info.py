import pygame
import levels as l
pygame.mixer.init()

caption = "Bouncing Bullets"
screenWidth = 1280
screenHeight = 720
FPS = 60
BGColour = (100, 100, 100)

screen = pygame.display.set_mode((screenWidth, screenHeight))  # Sets resolution.
currentLevel = l.menu  # Set to the first stage of the game (main menu).

# Various values that can be tweaked.
moveSpeed = 5
playerBulletSpeed = 10
enemySpeed = 3
maxBullets = 10

tileWidth = 100
tileHeight = 100

# Variable used to reset the score back to its original value.
startingScore = 1000
# Score that can be changed during the game.
score = 1000

# Text that will be displayed in the same area; simpler to have one variable that can display either form of text.
# Will either display "R to reload" if the player's gun is empty, or "R to restart" if the player is dead.
reloadOrRestartText = ""

# Load all the images for the sprites.
bulletImage = pygame.image.load("Assets/Player/bullet.png")
startImage = pygame.image.load("Assets/UI/start.png")
startHover = pygame.image.load("Assets/UI/startHover.png")
quitImage = pygame.image.load("Assets/UI/quit.png")
quitHover = pygame.image.load("Assets/UI/quitHover.png")
howToPlayImage = pygame.image.load("Assets/UI/howToPlay.png")
howToPlayHover = pygame.image.load("Assets/UI/howToPlayHover.png")
continueImage = pygame.image.load("Assets/UI/continue.png")
continueHover = pygame.image.load("Assets/UI/continueHover.png")
menuImage = pygame.image.load("Assets/UI/mainMenu.png")
menuHover = pygame.image.load("Assets/UI/mainMenuHover.png")
barSliderImage = pygame.image.load("Assets/UI/barSliderImage.png")
knobImage = pygame.image.load("Assets/UI/barKnob.png")
instructionsImage = pygame.image.load("Assets/UI/instructions.png")

map2Image = pygame.image.load("Assets/Environment/map2.png")
wallImage = pygame.image.load("Assets/Environment/wall.png")
doorHorImage = pygame.image.load("Assets/Environment/doorHor.png")
doorHorBrokenImage = pygame.image.load("Assets/Environment/doorHorBroken.png")
doorVerImage = pygame.image.load("Assets/Environment/doorVer.png")
doorVerBrokenImage = pygame.image.load("Assets/Environment/doorVerBroken.png")

# List comprehension to load in the animation frames (they are saved as numbers in folders).
playerIdle = [pygame.image.load("Assets/Player/idle/" + str(i + 1) + ".png") for i in range(5)]
playerWalk = [pygame.image.load("Assets/Player/walk/" + str(i + 1) + ".png") for i in range(5)]
playerShoot = [pygame.image.load("Assets/Player/shoot/" + str(i + 1) + ".png") for i in range(3)]
playerReload = [pygame.image.load("Assets/Player/reload/" + str(i + 1) + ".png") for i in range(8)]

enemyIdle = pygame.image.load("Assets/Guard/walk/1.png")
enemyWalk = [pygame.image.load("Assets/Guard/walk/" + str(i + 1) + ".png") for i in range(10)]
enemyDeath = [pygame.image.load("Assets/Guard/death/" + str(i + 1) + ".png") for i in range(4)]

soundList = []

# Load all the sound effects, add them all to the sound list.
shootSound = pygame.mixer.Sound("Assets/Sound/playerShoot.wav")
soundList.append(shootSound)
reloadSound = pygame.mixer.Sound("Assets/Sound/playerReload.wav")
soundList.append(reloadSound)
guardDeathSound = pygame.mixer.Sound("Assets/Sound/guardDeath.wav")
soundList.append(guardDeathSound)
houseAlarm = pygame.mixer.Sound("Assets/Sound/houseAlarm.wav")
soundList.append(houseAlarm)
doorBreakSound = pygame.mixer.Sound("Assets/Sound/doorBreak.wav")
soundList.append(doorBreakSound)
bulletBounceSound = pygame.mixer.Sound("Assets/Sound/bulletBounce.wav")
soundList.append(bulletBounceSound)

gameMusic = pygame.mixer.Sound("Assets/Sound/music.wav")
soundList.append(gameMusic)
