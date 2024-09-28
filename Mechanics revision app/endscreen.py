import UI
import pygame
import sys
import qgen
from settings import settingsMenu

def endScreen(questionTuple, usersAnswer, count):
    answerString = f"You said: {questionTuple[6][questionTuple[3]]} = {usersAnswer}"
    answerString += ((int(UI.xwidthScale(45))) - len(answerString)) * " "
    answerString2 = f"The correct answer is: {questionTuple[1]}"
    answerString += answerString2
    answerString += ((int(UI.xwidthScale(45))) - len(answerString2)) * " "
    if usersAnswer == questionTuple[4][questionTuple[3]]:
        answerString += f"You were correct!"
        colour = UI.green # green background
        count += 1
    else:
        answerString += f"You were incorrect!"
        colour = UI.red # red background
        count = 0 # reset if wrong

    if count >= 3: # if 3 in a row correct
        difficulty = "hard"
    else:
        difficulty = "easy"

    # create elements
    question = UI.Element(250, 100, 1065, 300, questionTuple[0], None, False, UI.buttonFont, None)
    answer = UI.Element(250, 450 ,1065, 200, answerString, None, False, UI.buttonFont, None)
    settingsButton = UI.Element(1480, 780, 80, 80, "", "settingsPressed", False, UI.buttonFont,"settings button.jpg")
    nextQButton = UI.Element(600, 750, 400, 110, "Next question", "nextQuestion", True, UI.buttonFont, None)
    elements = [question,answer,settingsButton, nextQButton] # list of elements to be iterated through

    screen = pygame.display.set_mode((UI.width, UI.height)) # allow space for taskbar
    pygame.display.set_caption("End screen") # title of the screen
    while True:
        for event in pygame.event.get():  # check for input every iteration
            if event.type == pygame.QUIT:  # allows app to be closed
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # checks for mouse input
                if event.button == 1:  # checks for LMC
                    for element in elements:  # iterate through each element
                        if element.rect.collidepoint(event.pos):  # finds the element that the click was on
                            if element.action == "nextQuestion":  # checks if the element's action is nextQuestion
                                qgen.questionScreen(count, difficulty)
                            elif element.action == "settingsPressed":  # checks if the element's action is settingsPressed
                                settingsMenu(count, difficulty)
        screen.fill(colour)  # set screen colour background
        for element in elements:  # iterate through all elements
            element.draw(screen)  # draw all elements
        pygame.display.flip()  # update display after every iteration

