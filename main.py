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
            for btn in s.buttonGroup:
                btn.is_clicked()


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

textTimer = 0

# Build the first level (main menu) before starting the loop.
b.level_build(i.currentLevel)


if running:
    # Play the game music on an endless loop.
    pygame.mixer.Sound.play(i.gameMusic, -1)

while running:
    # Limit the frame rate.
    clock.tick(i.FPS)

    # Always increase the text timer by 1 each frame, will set it back to 0 when the proceedText is changed.
    textTimer += 1
    # When text timer is greater than 300 (5 seconds), set the text back to being blank.
    if textTimer >= 300:
        i.proceedText = ""

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

        pygame.display.update()
        pygame.display.flip()

        # If the start button is clicked...
        for startButton in s.startGroup:
            if startButton.clicked:
                # Update the current level, clear the screen, then build the next level.
                i.currentLevel = l.level1
                i.proceedText = "MISSION: clear all floors and find the boss."
                textTimer = 0
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

        pygame.display.update()
        pygame.display.flip()

        # If the start button is clicked...
        for startButton in s.startGroup:
            if startButton.clicked:
                # Update the current level, clear the screen, then build the next level.
                i.currentLevel = l.level1
                load_level()


# # # # # # # # # # # # # # # # # # # # # IN LEVEL # # # # # # # # # # # # # # # # # # # # #


    # If you're in an actual game level.
    if i.currentLevel == l.level1 or i.currentLevel == l.level2 or i.currentLevel == l.level3:

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

        # If an alive guard detected a dead guard, set off the alarm and "kill" the player.
        if s.enemyDetected:
            b.playerInstance.alive = False
            pygame.mixer.Sound.play(i.houseAlarm, -1)
            # Set this global variable back to false so future guards can be detected.
            s.enemyDetected = False

        # # # Updating.
        s.allSprites.update()
        # Updates the camera's position based on the player.
        b.cameraInstance.update(b.playerInstance)
        # Adds the restart text if the player is dead.
        if not b.playerInstance.alive:
            i.reloadOrRestartText = "R to restart!"
        # Update the reload or restart display & proceed text display once the sprites have been updated.
        reloadOrRestartDisplay = font.render(i.reloadOrRestartText, True, pygame.Color('white'))
        proceedTextDisplay = font.render(i.proceedText, True, pygame.Color('white'))

        # # # Blitting.
        # Offsets the sprites relative to the camera's position.
        for sprite in s.allSprites:
            # Don't offset the pause overlay relative to the camera's position -- this is UI and should be centered.
            if sprite in s.pauseOverlayGroup:
                pass
            else:
                i.screen.blit(sprite.image, b.cameraInstance.offset(sprite))
        # Blit the score to the screen.
        i.screen.blit(scoreDisplay, (i.screenWidth - 210, 10))
        # Blit the reload or restart text.
        i.screen.blit(reloadOrRestartDisplay, (20, i.screenHeight - 50))
        i.screen.blit(proceedTextDisplay, (40, 10))

        # # # Checking for win condition.
        # If no enemies remain, move to the next level.
        if len(s.aliveEnemyList) == 0:
            # If you're in level 1, save your score and go to level 2.
            if i.currentLevel == l.level1:
                i.lvl1FinalScore = i.score
                i.proceedText = "1st floor cleared. Proceed to 2nd floor..."
                i.currentLevel = l.level2
            # If you're in level 2, save your score and go to level 3.
            elif i.currentLevel == l.level2:
                i.lvl2FinalScore = i.score
                i.proceedText = "2nd floor cleared. Destroy all guards and the boss..."
                i.currentLevel = l.level3
            elif i.currentLevel == l.level3:
                i.lvl3FinalScore = i.score
                pass  # put win condition here
            # Set the proceed text, then load the next level.
            textTimer = 0
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

            # Set the volume of all sounds to the value determined by the volume slider.
            for sound in i.soundList:
                sound.set_volume(s.normalisedValue)

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

        # # # Checking for lose condition.
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
