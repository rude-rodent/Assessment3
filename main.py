import pygame
import sys
import info as i
import sprites as s
import build as b

pygame.init()
pygame.display.set_caption(i.caption)
screen = pygame.display.set_mode((i.screenWidth, i.screenHeight))  # Sets resolution.

# Add this to level generation.
cameraInstance = b.Camera()
playerInstance = s.Player(300, 300, cameraInstance)

b.level_build()


running = True

while running:
    pygame.time.Clock().tick(i.FPS)

    for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            playerInstance.fire()

    screen.fill(i.BGColour)

    # Calls the update methods for every object in the sprite group.
    s.allSprites.update()
    # Updates the camera's position based on the player.
    cameraInstance.update(playerInstance)
    # Offsets the sprites relative to the camera's position.
    for sprite in s.allSprites:
        screen.blit(sprite.image, cameraInstance.offset(sprite))

    pygame.display.flip()  # 2 buffers: stuff that's going to draw, stuff that's already drawn. Flip turns the two.
