import pygame
import UI
import math
import graphanim

screen = pygame.display.set_mode((UI.width, UI.height))
pygame.display.set_caption("Simulation")

def graphing(userGraphingValues,actualGraphingValues, difficulty, sprite): # take value dictionaries and sprite as parameters
    usersAnswerKey = list(userGraphingValues.keys())[0]

    if (usersAnswerKey == "v") or (not "u" in userGraphingValues): # check if "u" needs to be generated
        if "t" in userGraphingValues:
            tempU = userGraphingValues["v"] - userGraphingValues["a"] * userGraphingValues["t"] # u in terms of v
        else:
            tempU = math.sqrt(userGraphingValues["v"] ** 2 - 2 * userGraphingValues["a"] * userGraphingValues["s"])
            userGraphingValues.update({"t":-userGraphingValues["u"]/userGraphingValues["a"]})
        if "u" in userGraphingValues:
            userGraphingValues["u"] = tempU # ensure u takes into account user input
        else:
            userGraphingValues.update({"u": tempU}) # create new u if there isn't one already

    # determine an appropriate domain and range
    turnPointY = - ((actualGraphingValues["u"]**2)/(2*actualGraphingValues["a"]))
    xMax = actualGraphingValues["t"] # always generate up until the "t" value
    if actualGraphingValues["v"] < 0: # if we have gone past the turning point:
        yMax = turnPointY # ensure the max height is the turning point
        if actualGraphingValues["s"] < 0:
            yMin = actualGraphingValues["s"] # ensure negative s can be displayed if necessary
        else:
            yMin = 0
    else:
        yMax = actualGraphingValues["s"] # generate up until height of s if before turning point
        yMin = 0

    c1 = 1/2 * userGraphingValues["a"]
    c2 = userGraphingValues["u"]

    graphanim.plotParabolaAnimation(c1, c2, 0, 0, xMax, yMin, yMax,
                                    sprite, difficulty, userGraphingValues)