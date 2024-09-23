import pygame
import pyautogui
import textwrap
import win32api

# initialize PyGame
pygame.init()

# constants, functions and preconditions
width, height = pyautogui.size()
monitorArea = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0))).get("Monitor")
workArea = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0))).get("Work")
taskbarHeight = (monitorArea[3]-workArea[3])
height = workArea[3] # accounts for taskbar
green = (172, 255, 117)  # shade of green used in designs
black = (0, 0, 0)
white = (255, 255, 255)
red = (247, 101, 99)
grey = (204, 204, 204)
buttonFont = pygame.font.Font(None, int(72*(height*width)/((1920*1080))))
titleFont = pygame.font.Font(None, int(96*(height*width)/((1920*1080))))

def xwidthScale(param):
    param *= (width)/1600
    return param

def yScale(param):
    param *= (height)/900
    param -= taskbarHeight #allows room for the taskbar
    return param

def heightScale(param):
    param *= (height)/900
    return param

# create the screen
screen = pygame.display.set_mode((width, height)) # allow space for taskbar
pygame.display.set_caption("Menu Screen") # title of the screen

# element class
class Element:
    def __init__(self, xPos, yPos, pWidth, pHeight, text, action, rounded, chosenFont, sprite):
        self.rect = pygame.Rect(xwidthScale(xPos), yScale(yPos), xwidthScale(pWidth), heightScale(pHeight))
        self.text = text
        self.rounded = rounded
        self.font = chosenFont
        self.action = action # action that should be performed on button press
        if isinstance(sprite,str):
            self.sprite = pygame.image.load(sprite).convert_alpha()
            print(type(self.sprite))

    def draw(self, screen):
        if self.rounded == True: # allow for rounded buttons
            roundness = 30
        else:
            roundness = 0
        pygame.draw.rect(screen, white, self.rect, 0, roundness) # draw element
        pygame.draw.rect(screen, black, self.rect, 1, roundness)  # draw outline of element
        if hasattr(self, "sprite"): # check if there is a sprite and scale it correctly
            self.sprite = pygame.transform.scale(self.sprite, (self.rect.width-2, self.rect.height-2))
            screen.blit(self.sprite, (self.rect.x+1, self.rect.y+1)) # display sprite
        wrappedText = textwrap.fill(self.text, int(xwidthScale(45)))  # allowed width
        lines = wrappedText.splitlines() # separate each line so they can be displayed separately
        # render each line of text
        for i, line in enumerate(lines):
            textSurface = self.font.render(line, True, black)
            # calculate the position for each line
            lineRect = textSurface.get_rect(center=(self.rect.centerx, self.rect.top + i * self.font.get_linesize()+heightScale(70)))
            screen.blit(textSurface, lineRect)


