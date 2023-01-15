import os
import random
import time
import turtle
import hand_control_tetris.hand_controller as hc
import cv2
from PIL import Image
import numpy as np
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
print(sys._MEIPASS)


class Shape():
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = random.randint(1, 7)
        self.square = [[1, 1],
                       [1, 1]]
        self.horizontal_line = [[1, 1, 1, 1]]
        self.left_L = [[1, 0, 0, 0],
                       [1, 1, 1, 1]]
        self.right_L = [[0, 0, 0, 1],
                        [1, 1, 1, 1]]
        self.left_S = [[1, 1, 0],
                       [0, 1, 1]]
        self.right_S = [[0, 1, 1],
                        [1, 1, 0]]
        self.T = [[0, 1, 0],
                  [1, 1, 1]]
        self.shapes = [self.square, self.horizontal_line,
                       self.left_L, self.left_S, self.right_S, self.T]
        self.shape = random.choice(self.shapes)
        self.height = len(self.shape)
        self.width = len(self.shape[0])

    def move_left(self, grid):
        if self.x > 0 and grid[self.y][self.x-1] == 0 and grid[self.y+self.height-1][self.x-1] == 0:
            self.erase_shape(grid)
            self.x = self.x-1
            self.draw_shape(grid)

    def move_right(self, grid):
        if self.x+self.width-1 < 11 and grid[self.y][self.x+self.width] == 0 and grid[self.y+self.height-1][self.x+self.width] == 0:
            self.erase_shape(grid)
            self.x = self.x+1
            self.draw_shape(grid)

    def move_down(self, grid):
        if self.y+self.height-1 < 23 and grid[self.y+self.height][self.x] == 0 and grid[self.y+self.height][self.x+self.width-1] == 0:
            self.erase_shape(grid)
            self.y = self.y+1
            self.draw_shape(grid)

    def draw_shape(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                if self.shape[y][x] == 1:
                    grid[self.y+y][self.x+x] = self.color

    def erase_shape(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                grid[self.y+y][self.x+x] = 0

    def can_move(self, grid):
        for x in range(self.width):
            if self.shape[self.height-1][x] == 1:
                if grid[self.y+self.height][self.x+x] != 0:
                    return False
            elif self.shape[self.height-2][x] == 1:
                if grid[self.y+self.height-1][self.x+x] != 0:
                    return False
            elif self.shape[self.height-3][x] == 1:
                if grid[self.y+self.height-2][self.x+x] != 0:
                    return False
        return True

    def rotate(self, grid):
        self.erase_shape(grid)
        rotated_shape = []
        for x in range(self.width):
            new_row = []
            for y in range(self.height-1, -1, -1):
                new_row.append(self.shape[y][x])
            rotated_shape.append(new_row)
        if self.x+self.height < 12 and grid[self.y+self.width+1][x] == 0:
            self.shape = rotated_shape
            self.height = len(self.shape)
            self.width = len(self.shape[0])


def draw_border(pen):
    pen.pencolor("#505050")
    pen.pensize(3)
    pen.penup()
    """
    pen.goto(-140, 260)
    pen.pendown()
    pen.goto(-140, -240)
    pen.goto(120, -240)
    pen.goto(120, 260)
    pen.goto(-140, 260)
    """
    pen.goto(-270, 260)
    pen.pendown()
    pen.goto(-270, -240)
    pen.goto(-10, -240)
    pen.goto(-10, 260)
    pen.goto(-270, 260)
    pen.hideturtle()
    pen.penup()


def draw_grid(pen, grid):
    pen.clear()
    top = 240
    left = -250
    #-120
    shapes = ["black", "#00f0f0", "blue", "orange",
              "yellow", "green", (resource_path('hand_control_tetris/Image/purpleTetris.gif'), "shape"), "#f00000"]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            screen_x = left+(x*20)
            screen_y = top-(y*20)
            number = grid[y][x]
            shape = shapes[number]
            if (shape[1] == "shape"):
                pen.shape(shape[0])
            else:
                pen.color(shape)
            pen.goto(screen_x, screen_y)
            pen.shape("square")
            pen.stamp()

    try:
        global img, wn
        img = Image.fromarray(img.astype('uint8')).convert('RGB')
        img.thumbnail((220,220),Image.ANTIALIAS)
        img.save(resource_path('hand_control_tetris/Image/purple.gif'))
        wn.register_shape(resource_path('hand_control_tetris/Image/purple.gif'))
        pen.shape(resource_path('hand_control_tetris/Image/purple.gif'))
        #-10 + 50 + half of the width of the shape (110) = 150
        pen.goto(150, 100)
        pen.stamp()
        pen.shape("square")
    except NameError:
        print(NameError)


def check_grid(grid):
    y = 23
    while y > 0:
        is_full = True
        for x in range(0, 12):
            if grid[y][x] == 0:
                is_full = False
                y = y-1
                break
        if is_full:
            global score
            score = score+10
            draw_score(pen, score)
            for copy_y in range(y, 0, -1):
                for copy_x in range(0, 12):
                    grid[copy_y][copy_x] = grid[copy_y-1][copy_x]


def draw_score(pen, score):
    pen.hideturtle()
    pen.color("blue")
    pen.goto(95, 232)
    gamescore = "Score:"+str(score)
    pen.write(gamescore, font=("Times", 24, "normal"))


grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

def main():
    pen = turtle.Turtle()
    pen.penup()
    pen.speed(0)
    pen.shape("square")
    pen.setundobuffer(None)

    border_pen = turtle.Turtle()
    border_pen.speed(0)
    draw_border(border_pen)

    global wn
    wn = turtle.Screen()
    wn.title("Tetris")
    wn.bgcolor("#e6e1d5")
    wn.setup(width=640, height=640)
    wn.tracer(0, 1)
    wn.register_shape(resource_path('hand_control_tetris/Image/purpleTetris.gif'))

    shape = Shape()

    wn.listen()
    wn.onkeypress(lambda: shape.move_left(grid), "Left")
    wn.onkeypress(lambda: shape.move_right(grid), "Right")
    wn.onkeypress(lambda: shape.move_down(grid), "Down")
    wn.onkeypress(lambda: shape.rotate(grid), "space")

    delay = .5

    score = 0


    cap = cv2.VideoCapture(0)
    detector = hc.handDetector()
    global img

    while True:
        wn.update()
        if shape.y == 23-shape.height+1:
            shape = Shape()
            check_grid(grid)
        if shape.can_move(grid):
            shape.erase_shape(grid)
            shape.y = shape.y+1
            shape.draw_shape(grid)
        else:
            shape = Shape()
            check_grid(grid)
        draw_grid(pen, grid)
        draw_score(pen, score)
        time.sleep(delay)

        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist) > 20:
            if (lmlist[4][1] > lmlist[3][1]) and (lmlist[4][2] < lmlist[0][2]) and (lmlist[17][1] > lmlist[20][1]) and (lmlist[20][2] < lmlist[17][2]):
                shape.rotate(grid)
            elif (lmlist[4][1] > lmlist[3][1]) and (lmlist[4][2] < lmlist[0][2]):
                shape.move_left(grid)
            elif (lmlist[17][1] > lmlist[20][1]) and (lmlist[20][2] < lmlist[17][2]):
                shape.move_right(grid)
        else:
            shape.move_down(grid)



if __name__ == "__main__": main()