import pygame
import sys
import info as i
import sprites as s
import levels as l
import build as b

pygame.init()
pygame.display.set_caption(i.caption)

font = pygame.font.Font(None, 30)

clock = pygame.time.Clock()

running = True
b.level_build(i.currentLevel)

while running:

    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))

    i.screen.fill(i.BGColour)
    clock.tick(i.FPS)

    if i.currentLevel == l.level1:

        for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
            if event.type == pygame.QUIT:
                pygame.display.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    b.playerInstance.fire()

        # Calls the update methods for every object in the sprite group.
        s.allSprites.update()
        # Updates the camera's position based on the player.
        b.cameraInstance.update(b.playerInstance)
        # Offsets the sprites relative to the camera's position.
        for sprite in s.allSprites:
            i.screen.blit(sprite.image, b.cameraInstance.offset(sprite))

        i.screen.blit(fps, (50, 50))

        if len(s.enemyGroup) == 0:
            i.currentLevel = l.level2
            b.clear_level()
            b.level_build(i.currentLevel)

    if i.currentLevel == l.level2:

        for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
            if event.type == pygame.QUIT:
                pygame.display.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    b.playerInstance.fire()

        # Calls the update methods for every object in the sprite group.
        s.allSprites.update()
        # Updates the camera's position based on the player.
        b.cameraInstance.update(b.playerInstance)
        # Offsets the sprites relative to the camera's position.
        for sprite in s.allSprites:
            i.screen.blit(sprite.image, b.cameraInstance.offset(sprite))

        i.screen.blit(fps, (50, 50))

    pygame.display.flip()  # 2 buffers: stuff that's going to draw, stuff that's already drawn. Flip turns the two.
