import UI
import qgen
import pygame
import sys

# create elements
title = UI.Element(300, 100, 1000, 160, "Projectile Motion Revision", None, False, UI.titleFont, None)
illustration = UI.Element(300, 300, 1000, 400, "", None, False, UI.buttonFont, "simulation.png")
startButton = UI.Element(600, 750, 400, 110, "Start", "startApplication", True, UI.buttonFont, None)
elements = [title, illustration, startButton] # list of elements to be iterated through

def displayMenu():
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
                            if element.action == "startApplication":  # checks if the element's action is startApplication
                                qgen.questionScreen(0,"easy")
        screen.fill(UI.green)  # set screen colour background
        for element in elements:  # iterate through all elements
            element.draw(screen)  # draw all elements
        pygame.display.flip()  # update display after every iteration

