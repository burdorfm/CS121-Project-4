from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time

#Versions:
"""
2*2 head and 1*1 body (with body segments init-ed at width of head segment or not!!!

Crazy snake (with random variable length between each tail segment

Massive crazy snake (2*2)

Headless horseman

random- block sized headless horseman

normal snake

skeleton snake

arcade vs non-arcade snake (whether or not you can turn in less than .length

battle snake (2-player)

maybe variable sized arena
maybe more than 2-player snake
maybe fix bug with changing directions
maybe make it an io game and call it not slither

"""

#a = [ "FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", "00FFFF", "000000", "800000", "008000", "000080", "808000", "800080", "008080", "808080", "C00000", "00C000", "0000C0", "C0C000", "C000C0", "00C0C0", "C0C0C0", "400000", "004000", "000040", "404000", "400040", "004040", "404040", "200000", "002000", "000020", "202000", "200020", "002020", "202020", "600000", "006000", "000060", "606000", "600060", "006060", "606060", "A00000", "00A000", "0000A0", "A0A000", "A000A0", "00A0A0", "A0A0A0", "E00000", "00E000", "0000E0", "E0E000", "E000E0", "00E0E0", "E0E0E0"]

class SnakeHead(Agent):

    WIDTH     = 1
    LENGTH    = 1

    def __init__(self,world, xpos, ypos, direction):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.frontSeg = None
        self.direction = direction
        self.agility = self.length/2  #/4 for janky modern snake  #/1 for classic snake
        self.position = world.bounds.point_at(xpos,ypos)
        self.initColor = "#%06x" % random.randint(0, 0xFFFFFF)
        Agent.__init__(self,self.position,world)

    def color(self):
        return self.initColor
    
    def shape(self):
        p1 = self.position + Vector2D( self.width, self.length)       
        p2 = self.position + Vector2D(-self.width, self.length)        
        p3 = self.position + Vector2D(-self.width,-self.length)       
        p4 = self.position + Vector2D( self.width,-self.length)       
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
        self.initColor = "#%06x" % random.randint(0, 0xFFFFFF)

        Agent.__init__(self,self.position,world)
        #instantiates

    def initPosition(self, followObject):
        a = random.randint(2,2)
        if followObject.direction == None:
            if followObject.position.x > .5:
                return followObject.position + Vector2D(a*followObject.width, 0)
            else:
                return followObject.position + Vector2D(-a*followObject.width, 0)               
        if followObject.direction == "right":
            return followObject.position + Vector2D(-a*followObject.width, 0)
        elif followObject.direction == "left":
            return followObject.position + Vector2D(a*followObject.width, 0)
        elif followObject.direction == "up":
            return followObject.position + Vector2D(0, -a*followObject.length)
        elif followObject.direction == "down":
            return followObject.position + Vector2D(0, a*followObject.length)

    def color(self):
        return self.initColor

    def shape(self):
        p1 = self.position + Vector2D( self.width/2, self.length/2)       
        p2 = self.position + Vector2D(-self.width/2, self.length/2)        
        p3 = self.position + Vector2D(-self.width/2,-self.length/2)       
        p4 = self.position + Vector2D( self.width/2,-self.length/2)       
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
        self.head = SnakeHead(world, .1, .1, None)
        self.head2 = SnakeHead(world, .9, .9, None)
        self.tail = SnakeBody(world, self.head)
        self.tail2 = SnakeBody(world, self.head2)
        self.snakeList = []
        self.snakeList.append(self.head)
        self.snakeList.append(self.tail)
        self.snakeList.append(self.head2)
        self.snakeList.append(self.tail2)
        self.world = world
        self.length = 2
        self.length2 = 2

    def grow(self):
        newTail = SnakeBody(self.world, self.tail)
        self.tail = newTail
        self.length += 1
        self.snakeList.append(self.tail)
    def grow2(self):
        newTail = SnakeBody(self.world, self.tail2)
        self.tail2 = newTail
        self.length2 += 1
        self.snakeList.append(self.tail2)
    def changeDir(self, direction):
        self.head.changeDirection(direction)
    def changeDir2(self, direction):
        self.head2.changeDirection(direction)
    def outOfBounds(self):
        if self.head.outOfBounds() == True:
            return 1
        if self.head2.outOfBounds()==True:
            return 2
        return 3

class Apple(Agent):
    def __init__(self, world):
        self.position = world.bounds.point_at(random.uniform(.015,.99),random.uniform(.013,.98))  #.99, .98
        self.width = 1
        self.length = 1
        Agent.__init__(self,self.position,world)

    def shape(self):
        p1 = self.position + Vector2D( self.width, self.length)       
        p2 = self.position + Vector2D(-self.width, self.length)        
        p3 = self.position + Vector2D(-self.width,-self.length)       
        p4 = self.position + Vector2D( self.width,-self.length)       
        return [p1, p2, p3, p4]
    def color(self):
        return "white"
    def update(self):
        return

class PlaySnake(Game):

    def __init__(self):
        Game.__init__(self,"2PSnake",60,45,800,600,topology='wrapped',console_lines=6)
        self.report("Players(s): Don't hit either snake's body or the walls.")
        self.report("Player(s): Eat to grow.")
        self.report("player1: use a,w,s,d to move.      player2: use arrow keys to move.")
        self.report("player1: press d to start.         player2: press left arrow to start.")

        self.use_mouse   = False  #maybe use a mouse thing to determine snake movement
        self.snake = Snake(self)
        self.food = Apple(self)


    def handle_keypress(self,event):       #requires changes!!!
        Game.handle_keypress(self,event)
        if event.char == ' ':
            self.snake.grow2()
            self.snake.grow()
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
        elif event.keysym_num == 65364 and not self.use_mouse: #SNEK UP
            if self.snake.head2.direction != "up":
                if self.snake.head2.direction != None:
                    self.snake.changeDir2("down")
        elif event.keysym_num == 65361 and not self.use_mouse: #SNEK UP
            if self.snake.head2.direction != "right":
                self.snake.changeDir2("left")
        elif event.keysym_num == 65362 and not self.use_mouse: #SNEK UP
            if self.snake.head2.direction != "down":
                if self.snake.head2.direction != None:
                    self.snake.changeDir2("up")
        elif event.keysym_num == 65363 and not self.use_mouse: #SNEK UP
            if self.snake.head2.direction != "left":
                if self.snake.head2.direction != None:
                    self.snake.changeDir2("right")
                    
    def display_length(self, a):
        if a == "1":
            self.report("Snake1 is now length: " + str(self.snake.length))
        else:
            self.report("Snake2 is now length: " + str(self.snake.length2))

            

    def update(self):
        n = 3                #Determines how much eats per food
        if n == 1:
            o = ""
        else:
            o = "s"
        difVector = self.snake.head.position - self.food.position        #CHECK FOR EATING FOR SNAKE
        if abs(difVector.dx) <= 2*self.food.width and abs(difVector.dy) <= 2*self.food.length:
            i = 0
            while i < n:
                self.snake.grow()
                i+=1
            self.remove(self.food)
            self.food = Apple(self)
            self.report()
            self.report()
            self.report()
            self.report("Snake1 has eaten " + str(n) + " apple" + o + "!")
            self.display_length("1")
        difVector = self.snake.head2.position - self.food.position              #CHECK FOR EATING FOR SNAKE2
        if abs(difVector.dx) <= 2*self.food.width and abs(difVector.dy) <= 2*self.food.length:
            i = 0
            while i < n:
                self.snake.grow2()
                i+=1
            self.remove(self.food)
            self.food = Apple(self)
            self.report()
            self.report()
            self.report()
            self.report("Snake2 has eaten " + str(n) + " apple" + o + "!")
            self.display_length("2")

        c = self.snake.outOfBounds()       #FULL OUT OF BOUNDS CHECK FOR BOTH SNAKES
        if c == 1:
            d = 2
        else:
            d = 1
        if c == 1 or c == 2:
            self.report()
            self.report()
            self.report("Snek" + str(c) + " has crashed into a wall and is now ded! Snek" + str(d) + " wins!")
            self.report("Final Lengths:\nSnek1: " + str(self.snake.length) + "\nSnek2: " + str(self.snake.length2))
            self.GAME_OVER = True

        a = self.snake.tail   #MAYBE IGNORE SEFMENT 1 BEFORE HEAD DUE TO TURNING ISSUES!!!
        while a.frontSeg != None:
            difVector = a.position - self.snake.head.position
            if abs(difVector.dx) <= self.snake.head.width/1.01 and abs(difVector.dy) <= self.snake.head.length/1.01: #2.01 for janky modern snake #2.00 for classic snake
                self.report()
                self.report()
                self.report()
                self.report("Snek1 has crashed into itself and is now ded! Snake2 Wins")
                self.remove(self.snake.head)
                self.GAME_OVER = True
            a = a.frontSeg
        b = self.snake.tail2   #MAYBE IGNORE SEFMENT 1 BEFORE HEAD DUE TO TURNING ISSUES!!!
        while b.frontSeg != None:
            difVector = b.position - self.snake.head.position
            if abs(difVector.dx) <= self.snake.head.width/1.01 and abs(difVector.dy) <= self.snake.head.length/1.01: #2.01 for janky modern snake #2.00 for classic snake
                self.report()
                self.report()
                self.report()
                self.report("Snek1 has crashed into Snek2 and is now ded! Snek2 Wins")
                self.remove(self.snake.head)
                self.GAME_OVER = True
            b = b.frontSeg
        b = self.snake.tail2
        while b.frontSeg != None:
            difVector = b.position - self.snake.head2.position
            if abs(difVector.dx) <= self.snake.head.width/1.01 and abs(difVector.dy) <= self.snake.head.length/1.01: #2.01 for janky modern snake #2.00 for classic snake
                self.report()
                self.report()
                self.report()
                self.report("Snek2 has crashed into itself and is now ded! Snek1 Wins")
                self.remove(self.snake.head2)
                self.GAME_OVER = True
            b = b.frontSeg
        a = self.snake.tail   #MAYBE IGNORE SEFMENT 1 BEFORE HEAD DUE TO TURNING ISSUES!!!
        while a.frontSeg != None:
            difVector = a.position - self.snake.head2.position
            if abs(difVector.dx) <= self.snake.head.width/1.01 and abs(difVector.dy) <= self.snake.head.length/1.01: #2.01 for janky modern snake #2.00 for classic snake
                self.report()
                self.report()
                self.report()
                self.report("Snek2 has crashed into Snek1 and is now ded! Snek2 Wins")
                self.remove(self.snake.head2)
                self.GAME_OVER = True
            a = a.frontSeg
        difVector = self.snake.head2.position - self.snake.head.position
        if abs(difVector.dx) <= self.snake.head.width/1.01 and abs(difVector.dy) <= self.snake.head.length/1.01:
            self.report()
            self.report()
            self.report()
            self.report("Sneks have bumped heads! Tis a tie.")
            self.remove(self.snake.head)
            self.remove(self.snake.head2)
            self.GAME_OVER = True
            
        Game.update(self)

game = PlaySnake()
while not game.GAME_OVER:
    time.sleep(1.0/60.0)  #1.0 for janky modern snake   #4.0 for classic snake
    game.update()
