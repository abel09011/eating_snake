#eating_snakev0.2

import math
import random
import pygame
import sys
import tkinter as tk
from tkinter import messagebox

#Two Objects "cube & snake"
class cube(object):
    rows = 20
    w = 500
                                                    #Color Green
    def __init__(self, start, dirnx=1, dirny=0, color=(0,255,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move (self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0] #Row
        j = self.pos[1] #Column

        #Rectangle X Y with height
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))

        #Draws eyes that are alligned
        if eyes:
            centre = dis // 2
            radius = 4 #Eye radius
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
                                    #Color Black
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        

#Snake function is composed of cube objects
class snake(object):
    #Creates list
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        #Head of snake = cubes
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0 #Values can be -1, 0 or 1
        self.dirny = 1 #Values can be -1, 0 or 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #Gets all of the key values
            keys = pygame.key.get_pressed()

            for key in keys:
                # Left make x negative
                # Right make x positive
                # same for y
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    
                    #Adds key (current position  of head of snake)
                    #Which is then set equal to which direction it turns
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        #Gets index & cube object from body            
        for i, c in enumerate(self.body):
            #For each object, we get the position
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                #If we are in the last cube, we remove the cube
                if i == len(self.body)-1:
                    self.turns.pop(p)
            #We are checking if we have reached the edge of the screen
            else:
                #If we move left and the x position is 0, then the position is in the right
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                #If we move right and we are in the edge of the screen, we then move left
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                #If we move down and we are in the edge of the screen, we then move Up
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                #If we move up and we are in the edge of the screen, we then move down
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                #If none is true, then we move our cube in direction x & y (forward)
                else: c.move(c.dirnx,c.dirny)
                
    #Reset function       
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        #We create a new cube to the direction opposite that we are going
        if dx ==1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        #When we draw the 1st cube head, then draw the eyes
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
#Various functions
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn #Increments x
        y = y + sizeBtwn #Increments y
        
        #Draws 2 lines for the grid every loop
        #                Argument, Color White,  Location(Start, End)
        #                                         x y   x y
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w)) #Vertical
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y)) #Horizontal

        
def redrawWindow(surface):
    global rows, width, s, snack
    #          Color Black
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #Makes sure that a snack does not spawns on top of the snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)
    
#Creates message box that is on top of the screen
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    message_box.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

#Main function loop
def main():
    global width, rows, s, snack
    width = 500
    height = 500
    #For the rows make sure to choose an even number
    rows = 20
    win = pygame.display.set_mode((width, height))
    #Sets the starting position of the snake
    # 10, 10 starts in the middle
    #   Color Green    Starting Position
    s = snake((0,255,0), (10,10))
    #                                      Color Red
    snack = cube(randomSnack(rows, s), color=(255,0,0))
    flag = True

    clock = pygame.time.Clock()
    
    while flag:
        #Delays 50 milli seconds so the program does not run too fast
        #The lower the number is, the faster it is
        pygame.time.delay(50)

        #It makes the game run 10 frames per second
        #You can play with the number
        #The smaller the number is, the slower the game is
        clock.tick(10)

        #Checks to see if the head has hit the snak, if it has, then its added to the body
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            #                                      Color Red
            snack = cube(randomSnack(rows, s), color=(255,0,0))
            
        #Checks to see if the head of the snake has hit the body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play Again...')

                #Resets position once it has collided with its body
                r.reset((10,10))
                break

            
        redrawWindow(win)
    pass


main()




    
    
    
        

