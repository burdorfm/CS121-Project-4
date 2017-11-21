from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time

"""
FINAL THING THAT NEEDS TO BE DONE FOR INITIAL SNAKE IMPLEMENTATION IS DEATH BY COLLIDING INTO OWN TAIL!!!!
"""

class SnakeHead(Agent):

    WIDTH     = 1
    LENGTH    = 1

    def __init__(self,world):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.frontSeg = None
        self.direction = None#"right"
        self.agility = self.length  #/4 for janky modern snake  #/1 for classic snake
        self.position = world.bounds.point_at(.5,.5)
        Agent.__init__(self,self.position,world)

    def color(self):
        return "yellow"

    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)       
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1, p2, p3, p4]

    def outOfBounds(self):
        if self.position.y - self.length/2.0 < self.world.bounds.ymin:
            return True
        if self.position.y + self.length/2.0 > self.world.bounds.ymax:
            return True
        if self.position.x - self.width/2.0 < self.world.bounds.xmin:
            return True
        if self.position.x + self.width/2.0 > self.world.bounds.xmax:
            return True

        
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
        self.agility = followObject.agility #followObject.agility
        #self.shadowPLace(followObject)

        Agent.__init__(self,self.position,world)
        #instantiates

    def initPosition(self, followObject):
        a = random.randint(1,1)
        if followObject.direction == "right" or followObject.direction == None:
            return followObject.position + Vector2D(-a*followObject.width, 0)
        elif followObject.direction == "left":
            return followObject.position + Vector2D(a*followObject.width, 0)
        elif followObject.direction == "up":
            return followObject.position + Vector2D(0, -a*followObject.length)
        elif followObject.direction == "down":
            return followObject.position + Vector2D(0, a*followObject.length)

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
            #if len(self.turnPositions[0]) > 1:
                #if self.turnPositions[2][0] == self.turnPositions[2][1]:       #check to see if i somehow break the connection
                    #print("WERE DONE")
            a = abs(self.position.x - self.turnPositions[0][0])
            b = abs(self.position.y - self.turnPositions[1][0])
            if a < .0003 or b < .0003:
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
        self.snakeList = []
        self.snakeList.append(self.head)
        self.snakeList.append(self.tail)
        self.world = world
        self.length = 2

    def grow(self):
        newTail = SnakeBody(self.world, self.tail)
        self.tail = newTail
        self.length += 1
        self.snakeList.append(self.tail)
    def changeDir(self, direction):
        self.head.changeDirection(direction)
    def outOfBounds(self):
        if self.head.outOfBounds() == True:
            return True
        return False

class Apple(Agent):
    def __init__(self, world):
        self.position = world.bounds.point_at(random.uniform(.015,.99),random.uniform(.013,.98))  #.99, .98
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
        Game.__init__(self,"Snake",60,45,800,600,topology='wrapped',console_lines=6)
        
        self.report("player: use a,w,s,d to move")
        self.report("player: don't hit your body or the walls")
        self.report("player: eat to grow")
        self.report("player: press d to start!")

        self.use_mouse   = False  #maybe use a mouse thing to determine snake movement
        self.snake = Snake(self)
        self.food = Apple(self)


    def handle_keypress(self,event):       #requires changes!!!
        Game.handle_keypress(self,event)
        if event.char == ' ':
            #escape to menu?????
            pass

        elif event.char == 'w' and not self.use_mouse: #SNEK UP
            if self.snake.head.direction != "down":
                if self.snake.head.direction != None:
                    self.snake.changeDir("up")
        elif event.char == 's' and not self.use_mouse: #SNEK DOWN
            if self.snake.head.direction != "up":
                if self.snake.head.direction != None:
                    self.snake.changeDir("down")
        elif event.char == 'd' and not self.use_mouse:
            if self.snake.head.direction != "left":
                self.snake.changeDir("right")
        elif event.char == 'a' and not self.use_mouse:
            if self.snake.head.direction != "right":
                if self.snake.head.direction != None:
                    self.snake.changeDir("left")

        #NEED A CHECK FOR IF EVENT 180 degrees from movement vector

    #def reset()

    #def populate????

    def display_length(self):
        self.report("Snake is now length: " + str(self.snake.length))

    def update(self):
        difVector = self.snake.head.position - self.food.position
        if abs(difVector.dx) <= self.snake.head.width and abs(difVector.dy) <= self.snake.head.length:
            n = 5
            if n == 1:
                o = ""
            else:
                o = "s"
            i = 1
            while i < n:
                self.snake.grow()
                i+=1
            self.snake.grow()
            self.remove(self.food)
            self.food = Apple(self)
            self.report()
            self.report()
            self.report()
            self.report("Snake has eaten " + str(n) + " apple" + o + "!")
            self.display_length()

        if self.snake.outOfBounds() == True:
            self.report()
            self.report()
            self.report()
            self.report("Snek has crashed into a wall and is now ded!")
            self.report("Final Length Achieved: " + str(self.snake.length))
            self.GAME_OVER = True

        a = self.snake.tail   #MAYBE IGNORE SEFMENT 1 BEFORE HEAD DUE TO TURNING ISSUES!!!
        while a.frontSeg != None:
            difVector = a.position - self.snake.head.position
            if abs(difVector.dx) <= self.snake.head.width/2.01 and abs(difVector.dy) <= self.snake.head.length/2.01: #2.01 for janky modern snake #2.00 for classic snake
                self.report()
                self.report()
                self.report()
                self.report("Snek has crashed into itself and is now ded!")
                self.remove(self.snake.head)
                self.report("Final Length Achieved: " + str(self.snake.length))
                self.GAME_OVER = True
            a = a.frontSeg

        Game.update(self)

game = PlaySnake()
while not game.GAME_OVER:
    time.sleep(2.0/60.0)  #1.0 for janky modern snake   #4.0 for classic snake
    game.update()
