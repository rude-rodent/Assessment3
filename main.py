import pygame
import sys
import info as i
import sprites as s
import levels as l
import build as b

pygame.init()
pygame.display.set_caption(i.caption)

font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()
# Every 1000 ticks, call a user event.
pygame.time.set_timer(pygame.USEREVENT, 1000)

running = True

# Build the first level (main menu) before starting the loop.
b.level_build(i.currentLevel)

while running:
    # Limit the frame rate.
    clock.tick(i.FPS)

    # Display the FPS for testing purposes.
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))

    scoreDisplay = font.render("Score: " + str(i.score), True, pygame.Color('white'))

    # Fill the screen with the background colour.
    i.screen.fill(i.BGColour)

    # During the main menu.
    if i.currentLevel == l.menu:
        # Check different button presses.
        for event in pygame.event.get():
            # Quit the game if the user presses the X.
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            # If the user presses the LMB...
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if the user clicked on a button.
                    for button in s.allSprites:
                        button.is_clicked()

        # Runs the update functions on all active sprites.
        s.allSprites.update()
        # Draws all active sprites to the screen.
        s.allSprites.draw(i.screen)
        # Draws the FPS (draws last so it's on top of walls).
        i.screen.blit(fps, (10, 10))

        pygame.display.update()
        pygame.display.flip()

        # If the start button is clicked...
        for startButton in s.startGroup:
            if startButton.clicked:
                # Update the current level, clear the screen, then build the next level.
                i.currentLevel = l.level1
                b.clear_level()
                b.level_build(i.currentLevel)
                i.score = i.startingScore


    # During the first level.
    if i.currentLevel == l.level1:

        # # # Checking for user input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            # If the 1000 ticks user event is called, 1 second has passed -> decrease the score by 1.
            if event.type == pygame.USEREVENT:
                i.score -= 1
            # If the user clicks the LMB, fire a bullet from the player.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    b.playerInstance.fire()

        # # # Updating.
        s.allSprites.update()
        # Updates the camera's position based on the player.
        b.cameraInstance.update(b.playerInstance)
        # Update the reload or restart display once the sprites have been updated.
        reloadOrRestartDisplay = font.render(i.reloadOrRestartText, True, pygame.Color('white'))

        # # # Blitting.
        # Offsets the sprites relative to the camera's position.
        for sprite in s.allSprites:
            i.screen.blit(sprite.image, b.cameraInstance.offset(sprite))
        i.screen.blit(fps, (50, 50))
        # Blit the score to the screen.
        i.screen.blit(scoreDisplay, (i.screenWidth - 210, 10))
        # Blit the reload or restart text.
        i.screen.blit(reloadOrRestartDisplay, (20, i.screenHeight - 50))

        pygame.display.update()
        pygame.display.flip()

        # # # Checking for win and lose conditions.
        # If no enemies remain, move to the next level.
        if len(s.aliveEnemyList) == 0:
            i.currentLevel = l.level2
            b.clear_level()
            b.level_build(i.currentLevel)
            i.score = i.startingScore

        # If you died, loop until user exits the game or presses R.
        while not b.playerInstance.alive:
            # Make sure the user can still quit the application during this infinite loop.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            # Check for the user pressing R, then restart the level and break.
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                b.clear_level()
                b.level_build(i.currentLevel)
                i.score = i.startingScore
                i.reloadOrRestartText = ""
                break

    # During the second level.
    if i.currentLevel == l.level2:

        for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                i.score -= 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    b.playerInstance.fire()

        s.allSprites.update()
        b.cameraInstance.update(b.playerInstance)

        # Update the reload or restart display once the sprites have been updated.
        reloadOrRestartDisplay = font.render(i.reloadOrRestartText, True, pygame.Color('white'))

        for sprite in s.allSprites:
            i.screen.blit(sprite.image, b.cameraInstance.offset(sprite))
        i.screen.blit(fps, (50, 50))
        i.screen.blit(scoreDisplay, (i.screenWidth - 210, 10))
        i.screen.blit(reloadOrRestartDisplay, (20, i.screenHeight - 50))

        pygame.display.update()
        pygame.display.flip()

        while not b.playerInstance.alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                b.clear_level()
                b.level_build(i.currentLevel)
                i.score = i.startingScore
                i.reloadOrRestartText = ""
                break
