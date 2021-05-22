import pygame

caption = "Bouncing Bullets"
screenWidth = 1280
screenHeight = 720
FPS = 60
BGColour = (200, 30, 30)

playerImage = pygame.image.load("player.png")
bulletImage = pygame.image.load("bullet.png")
moveSpeed = 5
playerBulletSpeed = 10

tileWidth = 128
tileHeight = 128
