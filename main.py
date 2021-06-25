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


# Some functions for code that will be used frequently during the game loop:

def quit_event(click):
    # Quit the game if the user presses the X.
    if click.type == pygame.QUIT:
        pygame.display.quit()
        pygame.quit()
        sys.exit()


def button_click(click):
    # If the user presses the LMB...
    if click.type == pygame.MOUSEBUTTONDOWN:
        if click.button == 1:
            # Check if the user clicked on a button.
            for button in s.buttonGroup:
                button.is_clicked()


def load_level():
    b.clear_level()
    b.level_build(i.currentLevel)
    i.score = i.startingScore


def toggle_pause():
    global paused
    if not paused:
        b.pause_overlay(l.pause)
        paused = True
    else:
        b.pause_close()
        paused = False


paused = False
running = True

# Build the first level (main menu) before starting the loop.
b.level_build(i.currentLevel)


if running:
    # Play the game music on an endless loop.
    pygame.mixer.Sound.play(i.gameMusic, -1)

while running:
    # Limit the frame rate.
    clock.tick(i.FPS)

    # Display the FPS for testing purposes.
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))

    scoreDisplay = font.render("Score: " + str(i.score), True, pygame.Color('white'))

    # Fill the screen with the background colour.
    i.screen.fill(i.BGColour)

    # Always set the volume of all sounds to the value determined by the volume slider.
    for sound in i.soundList:
        sound.set_volume(s.normalisedValue)


# # # # # # # # # # # # # # # # # # # # # MAIN MENU # # # # # # # # # # # # # # # # # # # # #


    # During the main menu.
    if i.currentLevel == l.menu:
        # Check different button presses.
        for event in pygame.event.get():
            # I tried putting the quit functions in just the outer loop, but they were unreliable, so I've had to put them in every level.
            quit_event(event)
            button_click(event)

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
                load_level()

        for howToPlayButton in s.howToPlayGroup:
            if howToPlayButton.clicked:
                i.currentLevel = l.howToPlay
                load_level()


# # # # # # # # # # # # # # # # # # # # # HOW TO PLAY # # # # # # # # # # # # # # # # # # # # #


    if i.currentLevel == l.howToPlay:
        for event in pygame.event.get():
            quit_event(event)
            button_click(event)

        # Update & draw.
        s.allSprites.update()
        s.allSprites.draw(i.screen)
        i.screen.blit(fps, (10, 10))

        pygame.display.update()
        pygame.display.flip()

        # If the start button is clicked...
        for startButton in s.startGroup:
            if startButton.clicked:
                # Update the current level, clear the screen, then build the next level.
                i.currentLevel = l.level1
                load_level()


# # # # # # # # # # # # # # # # # # # # # LEVEL 1 # # # # # # # # # # # # # # # # # # # # #


    # During the first level.
    if i.currentLevel == l.level1:

        # # # Checking for user input.
        for event in pygame.event.get():
            quit_event(event)
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                toggle_pause()
            # If the 1000 ticks user event is called, 1 second has passed -> decrease the score by 1.
            if event.type == pygame.USEREVENT:
                i.score -= 1
            # If the user clicks the LMB, fire a bullet from the player.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    b.playerInstance.fire()

        if s.enemyDetected:
            b.playerInstance.alive = False
            pygame.mixer.Sound.play(i.houseAlarm, -1)
            s.enemyDetected = False

        # # # Updating.
        s.allSprites.update()
        # Updates the camera's position based on the player.
        b.cameraInstance.update(b.playerInstance)
        # Adds the restart text if the player is dead.
        if not b.playerInstance.alive:
            i.reloadOrRestartText = "R to restart!"
        # Update the reload or restart display once the sprites have been updated.
        reloadOrRestartDisplay = font.render(i.reloadOrRestartText, True, pygame.Color('white'))

        # # # Blitting.
        # Offsets the sprites relative to the camera's position.
        for sprite in s.allSprites:
            # Don't offset the pause overlay relative to the camera's position -- this is UI and should be centered.
            if sprite in s.pauseOverlayGroup:
                pass
            else:
                i.screen.blit(sprite.image, b.cameraInstance.offset(sprite))
        i.screen.blit(fps, (50, 50))
        # Blit the score to the screen.
        i.screen.blit(scoreDisplay, (i.screenWidth - 210, 10))
        # Blit the reload or restart text.
        i.screen.blit(reloadOrRestartDisplay, (20, i.screenHeight - 50))

        # # # Checking for win and lose conditions.
        # If no enemies remain, move to the next level.
        if len(s.aliveEnemyList) == 0:
            i.currentLevel = l.level2
            load_level()

        pygame.display.update()
        pygame.display.flip()

        # # # Pause.
        while paused:
            # Make sure the user can still quit the application during this infinite loop.
            for event in pygame.event.get():
                quit_event(event)
                button_click(event)
                # Break out of the pause loop if the user hits escape again.
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    toggle_pause()
                    break

            # Update and blit the buttons.
            for UI in s.pauseOverlayGroup:
                UI.update()
                i.screen.blit(UI.image, UI.rect)
            pygame.display.update()
            pygame.display.flip()

            for continueButton in s.continueGroup:
                if continueButton.clicked:
                    # Break out of the pause loop if the user presses continue.
                    toggle_pause()
                    break
            for menuButton in s.menuGroup:
                if menuButton.clicked:
                    # Go back to the main menu if the user presses this.
                    i.currentLevel = l.menu
                    load_level()
                    toggle_pause()
                    break

        # If you died, loop until user exits the game or presses R.
        while not b.playerInstance.alive:
            # Make sure the user can still quit the application during this infinite loop.
            for event in pygame.event.get():
                quit_event(event)
            # Check for the user pressing R, then restart the level and break.
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                load_level()
                i.reloadOrRestartText = ""
                break


# # # # # # # # # # # # # # # # # # # # # LEVEL 2 # # # # # # # # # # # # # # # # # # # # #


    # During the second level.
    if i.currentLevel == l.level2:

        for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
            quit_event(event)
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                toggle_pause()
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
            if sprite in s.pauseOverlayGroup:
                pass
            else:
                i.screen.blit(sprite.image, b.cameraInstance.offset(sprite))
        i.screen.blit(fps, (50, 50))
        i.screen.blit(scoreDisplay, (i.screenWidth - 210, 10))
        i.screen.blit(reloadOrRestartDisplay, (20, i.screenHeight - 50))

        pygame.display.update()
        pygame.display.flip()

        # # # Pause.
        while paused:
            # Make sure the user can still quit the application during this infinite loop.
            for event in pygame.event.get():
                quit_event(event)
                button_click(event)
                # Break out of the pause loop if the user hits escape again.
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    toggle_pause()
                    break

            # Update and blit the buttons.
            for button in s.buttonGroup:
                button.update()
                i.screen.blit(button.image, button.rect)
            pygame.display.update()
            pygame.display.flip()

            for continueButton in s.continueGroup:
                if continueButton.clicked:
                    # Break out of the pause loop if the user presses continue.
                    toggle_pause()
                    break
            for menuButton in s.menuGroup:
                if menuButton.clicked:
                    # Go back to the main menu if the user presses this.
                    i.currentLevel = l.menu
                    load_level()
                    toggle_pause()
                    break

        while not b.playerInstance.alive:
            for event in pygame.event.get():
                quit_event(event)
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                load_level()
                i.reloadOrRestartText = ""
                break
