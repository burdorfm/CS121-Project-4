from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time

class SnakeHead(Agent):

    WIDTH = 1
    LENGTH = 1

    def __init__(self,world):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.direction = "right"
        self.agility = self.length / 4
        position = world.bounds.point_at(.5,.5)
        Agent.__init__(self,position,world)
        
    def keep_within_bounds(self):
        if self.position.y - self.length/2.0 < self.world.bounds.ymin:
            self.position.y = self.world.bounds.ymin + self.length/2.0
        if self.position.y + self.length/2.0 > self.world.bounds.ymax:
            self.position.y = self.world.bounds.ymax - self.length/2.0
        if self.position.x - self.width/2.0 < self.world.bounds.xmin:
            self.position.x = self.world.bounds.xmin + self.width/2.0
        if self.position.x + self.width/2.0 > self.world.bounds.xmax:
            self.position.x = self.world.bounds.xmax - self.width/2.0

    def color(self):
            return "#FF8040"

    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)       
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1, p2, p3, p4]
        
    def move_down(self):
        self.position.y -= self.agility
        self.keep_within_bounds()
    def move_up(self):
        self.position.y += self.agility
        self.keep_within_bounds()
    def move_left(self):
        self.position.x -= self.agility
        self.keep_within_bounds()
    def move_right(self):
        self.position.x += self.agility
        self.keep_within_bounds()

    def updatePos(self, direction):
        if direction == "up":
            self.move_up()
        elif direction == "down":           
            self.move_down()
        elif direction == "right":
            self.move_right()
        elif direction == "left":
            self.move_left()

    def changeDirection(self, direction):
        self.direction = direction
        
    def update(self):
        self.keep_within_bounds()
        self.updatePos(self.direction)

class SnakeBody(Agent):
    def __init__(self,world,followObject):
        self.position = followObject.position + Vector2D(-followObject.width, 0)
        self.length = followObject.length
        self.width = followObject.width
        self.direction = followObject.direction
        self.frontSeg = followObject
        self.turnPositions = [[],[],[]]
        self.storedDirection = self.direction
        self.agility = followObject.agility
        #self.shadowPLace(followObject)

        Agent.__init__(self,self.position,world)
        #instantiates
    def keep_within_bounds(self):
        if self.position.y - self.length/2.0 < self.world.bounds.ymin:
            self.position.y = self.world.bounds.ymin + self.length/2.0
        if self.position.y + self.length/2.0 > self.world.bounds.ymax:
            self.position.y = self.world.bounds.ymax - self.length/2.0
        if self.position.x - self.width/2.0 < self.world.bounds.xmin:
            self.position.x = self.world.bounds.xmin + self.width/2.0
        if self.position.x + self.width/2.0 > self.world.bounds.xmax:
            self.position.x = self.world.bounds.xmax - self.width/2.0

    def color(self):
            return "#FF8040"

    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)       
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1, p2, p3, p4]
        
    def move_down(self):
        self.position.y -= self.agility
        self.keep_within_bounds()
    def move_up(self):
        self.position.y += self.agility
        self.keep_within_bounds()
    def move_left(self):
        self.position.x -= self.agility
        self.keep_within_bounds()
    def move_right(self):
        self.position.x += self.agility
        self.keep_within_bounds()

    def updatePos(self, direction):
        if self.storedDirection != self.frontSeg.direction:
            self.turnPositions[0].append(self.frontSeg.position.x)
            self.turnPositions[1].append(self.frontSeg.position.y)
            self.turnPositions[2].append(self.frontSeg.direction)
            self.storedDirection = self.frontSeg.direction

        if len(self.turnPositions[0]) > 0:
            a = abs(self.position.x - self.turnPositions[0][0])
            b = abs(self.position.y - self.turnPositions[1][0])
            if a < .0001 or b < .0001:
                self.changeDirection(self.turnPositions[2][0])
                self.turnPositions[0].pop(-len(self.turnPositions[0]))
                self.turnPositions[1].pop(-len(self.turnPositions[1]))
                self.turnPositions[2].pop(-len(self.turnPositions[2]))            

        if self.direction == "up":
            self.move_up()
        elif self.direction == "down":
            self.move_down()
        elif self.direction == "right":
            self.move_right()
        elif self.direction == "left":
            self.move_left()

    def changeDirection(self, direction):
        self.direction = direction
        
    def update(self):
        self.keep_within_bounds()
        self.updatePos(self.direction)



class Snake:
    def __init__(self, world):
        self.head = SnakeHead(world)
        self.tail = SnakeBody(world, head)

    def grow():
        newTail = SnakeBody(world, tail)
class PlaySnake(Game):

    def __init__(self):
        Game.__init__(self,"Snake",60.0,45.0,1500,600,topology='bound',console_lines=6)
        
        self.report("player: use a,w,s,d to move")
        self.report("player: don't hit your body or the walls")
        self.report("player: eat to grow")

        self.left_score  = 0
        self.right_score = 0
        self.use_mouse   = False
        #self.snake = Snake(self)
        self.snakehead  = SnakeHead(self)
        self.snakebody = SnakeBody(self, self.snakehead)


        i = 0
        pointer = self.snakebody
        while i < 40:
            a = SnakeBody(self, pointer)
            pointer = a
            i += 1


    def handle_keypress(self,event):
        Game.handle_keypress(self,event)
        if event.char == ' ':
            self.use_mouse = not self.use_mouse
        elif event.char == 'w' and not self.use_mouse: #SNEK UP
            if self.snakehead.direction != "down":
                self.snakehead.changeDirection("up")
        elif event.char == 's' and not self.use_mouse: #SNEK DOWN
            if self.snakehead.direction != "up":
                self.snakehead.changeDirection("down")
        elif event.char == 'd' and not self.use_mouse:
            if self.snakehead.direction != "left":
                self.snakehead.changeDirection("right")
        elif event.char == 'a' and not self.use_mouse:
            if self.snakehead.direction != "right":
                self.snakehead.changeDirection("left")

        #NEED A CHECK FOR IF EVENT 180 degrees from movement vector

    #def reset()

    #def populate????

    def display_score(self):
        self.report("LEFT:"+str(self.left_score)+"\tRIGHT:"+str(self.right_score))

    def update(self):
        Game.update(self)

game = PlaySnake()
while not game.GAME_OVER:
    time.sleep(1.0/60.0)
    game.update()
