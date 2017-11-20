from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time

class SnakeHead(Agent):

    WIDTH     = 1
    LENGTH    = 1

    def __init__(self,world):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.direction = "right"
        self.agility = self.length/2
        self.position = world.bounds.point_at(.5,.5)
        Agent.__init__(self,self.position,world)

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
    def move_up(self):
        self.position.y += self.agility
    def move_left(self):
        self.position.x -= self.agility
    def move_right(self):
        self.position.x += self.agility

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
        self.updatePos(self.direction)

class SnakeBody(Agent):
    def __init__(self,world,followObject):
        self.position = self.initPosition(followObject)
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

    def initPosition(self, followObject):
        if followObject.direction == "right" or followObject.direction == None:
            return followObject.position + Vector2D(-followObject.width, 0)
        elif followObject.direction == "left":
            return followObject.position + Vector2D(followObject.width, 0)
        elif followObject.direction == "up":
            return followObject.position + Vector2D(0, -followObject.length)
        elif followObject.direction == "down":
            return followObject.position + Vector2D(0, followObject.length)

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
    def move_up(self):
        self.position.y += self.agility
    def move_left(self):
        self.position.x -= self.agility
    def move_right(self):
        self.position.x += self.agility

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
        self.updatePos(self.direction)

class Snake:
    def __init__(self, world):
        self.head = SnakeHead(world)
        self.tail = SnakeBody(world, self.head)
        self.world = world
        self.length = 2

    def grow(self):
        newTail = SnakeBody(self.world, self.tail)
        self.tail = newTail
        self.length += 1
    def changeDir(self, direction):
        self.head.changeDirection(direction)

class Apple(Agent):
    def __init__(self, world):
        self.position = world.bounds.point_at(random.uniform(.007,1.1),random.uniform(.007,.987))  #.007x-.903  .140-.987y
        self.width = 1
        self.length = 1
        Agent.__init__(self,self.position,world)

    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)       
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1, p2, p3, p4]
    def color(self):
        return "white"
    def update(self):
        return



class PlaySnake(Game):

    def __init__(self):
        Game.__init__(self,"Snake",1500/7.5,80,1500,600,topology='wrapped',console_lines=6)
        
        self.report("player: use a,w,s,d to move")
        self.report("player: don't hit your body or the walls")
        self.report("player: eat to grow")

        self.left_score  = 0
        self.right_score = 0
        self.use_mouse   = False
        self.snake = Snake(self)
        self.food = Apple(self)


    def handle_keypress(self,event):       #requires changes!!!
        Game.handle_keypress(self,event)
        if event.char == ' ':
            self.snake.grow()
            self.remove(self.food)
            self.food = Apple(self)
        elif event.char == 'w' and not self.use_mouse: #SNEK UP
            if self.snake.head.direction != "down":
                self.snake.changeDir("up")
        elif event.char == 's' and not self.use_mouse: #SNEK DOWN
            if self.snake.head.direction != "up":
                self.snake.changeDir("down")
        elif event.char == 'd' and not self.use_mouse:
            if self.snake.head.direction != "left":
                self.snake.changeDir("right")
        elif event.char == 'a' and not self.use_mouse:
            if self.snake.head.direction != "right":
                self.snake.changeDir("left")

        #NEED A CHECK FOR IF EVENT 180 degrees from movement vector

    #def reset()

    #def populate????

    def display_score(self):
        self.report("LEFT:"+str(self.left_score)+"\tRIGHT:"+str(self.right_score))

    def update(self):
        difVector = self.snake.head.position - self.food.position
        if abs(difVector.dx) <= self.snake.head.width and abs(difVector.dy) <= self.snake.head.length:
            self.snake.grow()
            self.remove(self.food)
            self.food = Apple(self)

        Game.update(self)

game = PlaySnake()
while not game.GAME_OVER:
    time.sleep(1.0/60.0)
    game.update()
