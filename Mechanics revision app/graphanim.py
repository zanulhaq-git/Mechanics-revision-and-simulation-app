import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pygame as pg

# allow parabola to draw out over time
def update(frame, xValues, yValues, line, ab, text_box, userGraphingValues):
    line.set_data(xValues[:frame], yValues[:frame])  # at each frame, line increments in x and relative y value
    currentX = xValues[frame]
    currentY = yValues[frame]
    ab.xybox = (currentX, currentY)  # update the image position
    for event in pg.event.get():  # check for input every iteration
        if event.type == pg.QUIT:  # allows app to be closed
            pg.quit()
            sys.exit()

    # update text box
    text_box.set_text(f'Time: {currentX:.2f}\n'
                      f'Displacement: {currentY:.2f}\n'
                      f'Initial velocity: {userGraphingValues["u"]:.2f}\n'
                      f'Current velocity: {(userGraphingValues["u"] + userGraphingValues["a"] * currentX):.2f}\n'
                      f'Acceleration: {userGraphingValues["a"]}')
    return line, ab, text_box

def plotParabolaAnimation(a, b, c, xMin, xMax, yMin, yMax, img_path, difficulty, userGraphingValues):
    fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
    xValues = np.linspace(xMin, xMax, 400)  # create a set of 400 evenly spaced x values
    yValues = a * xValues ** 2 + b * xValues + c  # equation of the curve

# configure axes and line
    line, = ax.plot([], [], label=f'{c:.2f} + {b:.2f}t + {a:.2f}t^2')  # labels the line with its equation
    ax.set_xlabel('Time')
    ax.set_ylabel("Displacement")
    ax.set_title('1D Simulation\n[Close window to skip]')

    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlim(xMin, xMax)
    ax.set_ylim(yMin, yMax)
    ax.legend()

    # Load the image
    img = mpimg.imread(img_path)
    imagebox = OffsetImage(img, zoom=0.1)
    ab = AnnotationBbox(imagebox, (0, 0), frameon=False, xycoords='data', boxcoords="data", pad=0)
    ax.add_artist(ab)  # add image to plot

    # Add textbox for coordinates outside the plot
    text_box = ax.text(1.1, 0.9, '', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8))

    def updateWrapper(frame):  # houses update method as frame is the only allowed parameter
        nonlocal line, ab, text_box  # uses line and ab from outer scope
        line, ab, text_box = update(frame, xValues, yValues, line, ab, text_box, userGraphingValues)
        return line, ab, text_box

    ani = FuncAnimation(fig, updateWrapper, frames=len(xValues), interval=10, repeat=False)

    plt.subplots_adjust(right=0.6)
    plt.grid(False)  # hide cartesian plane grid
    plt.show()  # display plot