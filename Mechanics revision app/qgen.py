import random
import pygame as pg
import sys
import UI
import endscreen
import graphing
from rounding import roundReal
from settings import settingsMenu

class Projectile:
    def __init__(self, initSprite, initName, initmaxSpeed):
        self.sprite = initSprite
        self.name = initName
        self.maxSpeed = initmaxSpeed

class Planet:
    def __init__(self, initName, initG):
        self.gravity = initG
        self.name = initName

def generateParameters(projectiles, planets, verb1D):
    chosenProjectile = projectiles[random.randint(0, len(projectiles) - 1)]
    chosenPlanet = planets[random.randint(0, len(planets) - 1)]
    chosenVerb = verb1D[random.randint(0, len(verb1D) - 1)]
    return chosenProjectile, chosenPlanet, chosenVerb, type

projectileList = [
    Projectile("ball.png", "ball", 30),
    Projectile("rock.png", "rock", 30),
    Projectile("dart.png", "dart", 100),
    Projectile("R (1).png", "paper aeroplace", 30),
    ]

planetList = [
    Planet("Earth", 9.8),
    Planet("Mars", 3.7),
    Planet("the Earth's moon", 1.6),
    Planet("an unnamed planet", roundReal(random.uniform(0.1,25),1)),
    Planet("Jupiter", 24.7),
    Planet("Venus", 8.8),
    Planet("Mercury", 3.7)
]

verb1DList = ["dropped", "thrown", "projected", "ejected", "released", "shot out of a launcher"]

difficulty = "hard"


#verb2DList = ["thrown"]
#planetList = [Planet("the back of Miss Gamble's Head", roundReal(random.uniform(0.1,25),1))]
#projectileList = [Projectile("placeholder","water bottle",100)]

class SUVATProblems:
    def __init__(self):
        self.variables = ["s", "u", "v", "a", "t"]
        self.variableNames = {
            "s": "displacement",
            "u": "initial velocity",
            "v": "current velocity",
            "a": "acceleration",
            "t": "time taken"
        }  # dictionary of SUVAT variables

    def generateQuestion(self, chosenProjectile, chosenPlanet, chosenVerb, difficulty):
        # select 3 random variables
        knownVariables = random.sample(self.variables, 3)
        # locate the final variable
        unknownVariable = random.choice(list(set(self.variables) - set(knownVariables)))
        # generate values for known variables
        values = {} # dictionary for SUVAT values
        for var in knownVariables:
            if var == "u":
                values[var] = roundReal(random.uniform(0, chosenProjectile.maxSpeed),2) # positive to ensure graph is displayed
            elif var == "v":
                values[var] = roundReal(random.uniform(-chosenProjectile.maxSpeed, chosenProjectile.maxSpeed),2)
            elif var == "a":
                values[var] = -chosenPlanet.gravity
            else:
                values[var] = roundReal(random.uniform(0.01, 10), 2)

        # choose question type:
        if difficulty == "hard":
            if unknownVariable != "s" and unknownVariable != "t":
                return self.generateQuestion(chosenProjectile, chosenPlanet, chosenVerb, difficulty)
            else:
                max = 1
        else:
            max = 0

        if max == 1:
            if "v" in knownVariables:
                values["v"] = 0

        # calculate the unknown variable using SUVAT equations

        actualValues = values # declare actual values to be used for graphing
        # print("actual values early",actualValues)

        if all(key in values for key in ["a","u","v"]):
            eqS = roundReal((values["v"]**2-values["u"]**2)/(2*values["a"]),2)
            eqT = roundReal((values["v"]-values["u"])/values["a"],2)
            if unknownVariable == "s":
                equation = eqS
                actualValues.update({"t": eqT})
            else:
                equation = eqT
                actualValues.update({"s": eqS})

        elif all(key in values for key in ["s","v","t"]):
            eqU = roundReal(2 * values["s"] / values["t"] - values["v"],2)
            eqA = roundReal(- 2 * (values["s"] - values["v"] * values["t"])/values["t"]**2,2)
            if unknownVariable == "u":
                equation = eqU
                actualValues.update({"a": eqA})
            else:
                equation = eqA
                actualValues.update({"u": eqU})

        elif all(key in values for key in ["s","u","t"]):
            eqV = roundReal(2 * values["s"] / values["t"] - values["u"],2)
            eqA = roundReal(2 * (values["s"] - values["u"] * values["t"])/values["t"]**2,2)
            if unknownVariable == "v":
                equation = eqV
                actualValues.update({"a": eqA})
            else:
                equation = eqA
                actualValues.update({"v": eqV})

        elif all(key in values for key in ["u","v","t"]):
            eqS = roundReal((values["u"]+values["v"])*values["t"]/2,2)
            eqA = roundReal((values["v"] - values["u"])/values["t"],2)
            if max == 1:
                return self.generateQuestion(chosenProjectile, chosenPlanet, chosenVerb,difficulty)
            if unknownVariable == "s":
                equation = eqS
                actualValues.update({"a": eqA})
            else:
                equation = eqA
                actualValues.update({"s": eqS})

        elif all(key in values for key in ["a","v","t"]):
            eqS = roundReal(values["v"] * values["t"] - (values["a"] * values["t"]**2 / 2),2)
            eqU = roundReal(values["v"] - values["a"]*values["t"],2)
            if max == 1:
                return self.generateQuestion(chosenProjectile, chosenPlanet, chosenVerb,difficulty)
            if unknownVariable == "s":
                equation = eqS
                actualValues.update({"u": eqU})
            else:
                equation = eqU
                actualValues.update({"s": eqS})

        elif all(key in values for key in ["a","u","t"]):
            eqS = roundReal(values["u"] * values["t"] + (values["a"] * values["t"]**2 / 2),2)
            eqV = roundReal(values["u"] + values["a"] * values["t"],2)
            if max == 1:
                return self.generateQuestion(chosenProjectile, chosenPlanet, chosenVerb,difficulty)
            if unknownVariable == "s":
                equation = eqS
                actualValues.update({"v": eqV})
            else:
                equation = eqV
                actualValues.update({"s": eqS})

        elif all(key in values for key in ["a","s","t"]):
            eqU = roundReal((2 * values["s"] - values["t"] ** 2 * values["a"])/(2 * values["t"]),2)
            eqV = roundReal((2 * values["s"] + values["t"] ** 2 * values["a"])/(2 * values["t"]),2)
            if unknownVariable == "u":
                equation = eqU
                actualValues.update({"v": eqV})
            else:
                equation = eqV
                actualValues.update({"u": eqU})

        elif all(key in values for key in ["v","s","u"]):
            if values["u"] + values["v"] == 0:
                return self.generateQuestion(chosenProjectile,chosenPlanet,chosenVerb)
            eqA = roundReal((values["v"]**2 - values["u"]**2)/(2*values["s"]),2)
            eqT = roundReal((2*values["s"])/(values["u"]+values["v"]),2)
            if unknownVariable == "a":
                equation = eqA
                actualValues.update({"t": eqT})
            else:
                equation = eqT
                actualValues.update({"a": eqA})

        elif all(key in values for key in ["a","v","s"]):
            # answers are multivalued, regenerate
            return self.generateQuestion(chosenProjectile, chosenPlanet, chosenVerb,difficulty)

        elif all(key in values for key in ["a","u","s"]):
            # answers are multivalued, regenerate
            return self.generateQuestion(chosenProjectile, chosenPlanet, chosenVerb,difficulty)

        actualValues.update({unknownVariable: equation})

        # generate the context
        context = f"A {chosenProjectile.name} is {chosenVerb}"
        if unknownVariable == "a":
            context += f" on an unspecified planet. \n"
            questionValues = {}
        elif "a" not in knownVariables:
            context += f" vertically on an unknown planet, where g = {-actualValues['a']}. \n"
            questionValues = {"a":actualValues["a"]}
        else:
            context += f" vertically on {chosenPlanet.name}, where g = {chosenPlanet.gravity}. \n"
            questionValues = {"a":-chosenPlanet.gravity}

        if actualValues["u"] < actualValues["v"]:  # acceleration is negative so v must be less than u
            return self.generateQuestion(chosenProjectile, chosenPlanet, chosenVerb,difficulty)
        if actualValues["a"] >= 0: #accel must be negative
            return self.generateQuestion(chosenProjectile, chosenPlanet, chosenVerb,difficulty)

        # generate the question
        count = 0
        if max == 1:
            if unknownVariable == "s":
                question = f"What is the maximum displacement when "
            else:
                question = f"How much time away is the point of maximum displacement when "
        else:
            question = f"What is the {self.variableNames[unknownVariable]} when "

        for i, j in values.items():
            count += 1
            if max == 1 and i != "u":
                pass
            elif i == "a":
                pass
            else:
                question += f"{self.variableNames.get(i)} is {j:.2f}, "
                questionValues.update({i:j})
            if (count == 3 and max == 0) or (count == 4 and max == 1): # accounts for skipped variables
                break
        questionOut = context + question[:-2] + "?"
        answerOut = f"{self.variableNames[unknownVariable]} = {equation:.2f}"

        # print(f"actual values {actualValues}")

        return questionOut, answerOut, questionValues, unknownVariable, actualValues, chosenProjectile.sprite, self.variableNames

# example usage
def questionScreen(count, difficulty):
    # generation preconditions, to be edited when question queue is complete
    generator = SUVATProblems()

    params = generateParameters(projectileList, planetList, verb1DList)
    questionTuple = generator.generateQuestion(*params[0:3], difficulty)
    # print(f"Real answer: {questionTuple[1]}")
    # print(f"Values: {questionTuple[2]}")

    question = UI.Element(250, 100, 1065, 300, questionTuple[0], None, False, UI.buttonFont,None)
    inputBox = UI.Element(600, 750, 400, 110, "", "answerInputted", True, UI.buttonFont,None)
    settingsButton = UI.Element(1480, 780, 80, 80, "", "settingsPressed", False, UI.buttonFont,"settings button.jpg")
    elements = [question,inputBox,settingsButton]  # list of elements to be iterated through

    pg.display.set_caption("Question")
    # pg loop
    nextPhase = False
    while nextPhase == False:
        for event in pg.event.get():  # check for input every iteration
            if event.type == pg.QUIT:  # allows app to be closed
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN: # check for keyboard input
                if inputBox.text == ("Invalid format!"):
                    inputBox.text = ""
                elif event.key == pg.K_BACKSPACE:
                    inputBox.text = inputBox.text[:-1] # allow for backspacing
                elif event.key == pg.K_RETURN:
                    try:
                        float(inputBox.text)
                    except ValueError:
                        inputBox.text = ("Invalid format!")
                    else:
                        # print(f"unrounded input{inputBox.text}")
                        usersAnswer = roundReal(float(inputBox.text),2)
                        graphingValues = {questionTuple[3]:usersAnswer}
                        graphingValues.update(questionTuple[2])
                        graphing.graphing(graphingValues, questionTuple[4], difficulty, questionTuple[5]) # load projectile motion
                        # print(f"User's answer: {usersAnswer}") # displays the variable in IDE
                        nextPhase = True  # loop breaking condition
                elif len(inputBox.text) < 15: # maximum length
                    inputBox.text += event.unicode # enters the unicode equivalent of the user's keyboard input
            elif event.type == pg.MOUSEBUTTONDOWN:  # checks for mouse input
                if event.button == 1:  # checks for LMC
                    for element in elements:  # iterate through each element
                        if element.rect.collidepoint(event.pos):  # finds the element that the click was on
                            if element.action == "settingsPressed":  # checks if the element's action is settingsPressed
                                settingsMenu(count, difficulty)
        UI.screen.fill(UI.green)  # set screen colour background
        for element in elements:  # iterate through all elements
            element.draw(UI.screen)  # draw all elements
        pg.display.flip()  # update display after every iteration
    endscreen.endScreen(questionTuple, usersAnswer, count)