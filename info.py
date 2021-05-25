import pygame

caption = "Bouncing Bullets"
screenWidth = 1280
screenHeight = 720
FPS = 60
BGColour = (200, 200, 200)

screen = pygame.display.set_mode((screenWidth, screenHeight))  # Sets resolution.

playerImage = pygame.image.load("player.png")
bulletImage = pygame.image.load("bullet.png")
enemyImage = pygame.image.load("enemy.png")
moveSpeed = 5
playerBulletSpeed = 10
enemySpeed = 3
maxBullets = 10

tileWidth = 128
tileHeight = 128
