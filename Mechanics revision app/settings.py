import UI
import pygame
import sys
import menu
import qgen

# create elements
title = UI.Element(525, 100, 530, 110, "Settings", None, False, UI.titleFont, None)
menuButton = UI.Element(525, 240, 530, 110, "Quit to main menu", "menu", True, UI.buttonFont, None)
skipButton = UI.Element(525, 380, 530, 110, "Skip question", "skip", True, UI.buttonFont, None)
difficultyButton = UI.Element(525, 520, 530, 110, "Reset difficulty", "reset", True, UI.buttonFont, None)
resumeButton = UI.Element(525, 660, 530, 110, "Resume", "resume", True, UI.buttonFont, None)

elements = [title, menuButton, skipButton, difficultyButton, resumeButton] # list of elements to be iterated through

def settingsMenu(count, difficulty):
    screen = pygame.display.set_mode((UI.width, UI.height)) # allow space for taskbar
    pygame.display.set_caption("Menu Screen") # title of the screen
    while True:
        for event in pygame.event.get():  # check for input every iteration
            if event.type == pygame.QUIT:  # allows app to be closed
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # checks for mouse input
                if event.button == 1:  # checks for LMC
                    for element in elements:  # iterate through each element
                        if element.rect.collidepoint(event.pos):  # finds the element that the click was on
                            if element.action == "menu":
                                menu.displayMenu() # load menu
                            elif element.action == "skip":
                                qgen.questionScreen(count, difficulty) # generate new question
                            elif element.action == "reset":
                                qgen.questionScreen(0, "easy") # set difficulty to easy and count to 0
                            elif element.action == "resume":
                                print("resume")
                                return None # break out of pygame loop to resume previous activity
        screen.fill(UI.grey)  # set screen colour background
        for element in elements:  # iterate through all elements
            element.draw(screen)  # draw all elements
        pygame.display.flip()  # update display after every iteration