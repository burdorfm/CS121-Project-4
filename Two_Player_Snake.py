from tkinter import *
from Game import *
from geometry import *
import math
import random
import time
import copy

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

    def __init__(self,world, xpos, ypos, direction, color):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.frontSeg = None
        self.direction = direction
        self.agility = self.length/2  #/4 for janky modern snake  #/1 for classic snake
        self.position = world.bounds.point_at(xpos,ypos)
        self.initColor = color#"#%06x" % random.randint(0, 0xFFFFFF)
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
    def __init__(self,world,followObject, color):
        self.position = self.initPosition(followObject)
        self.length = followObject.length
        self.width = followObject.width
        self.direction = followObject.direction
        self.frontSeg = followObject
        self.turnPositions = [[],[],[]]
        self.storedDirection = self.direction
        self.agility = followObject.agility #followObject.agility
        self.initColor = color#"#%06x" % random.randint(0, 0xFFFFFF)

        Agent.__init__(self,self.position,world)
        #instantiates

    def initPosition(self, followObject):
        a = random.randint(30,30)
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
    
    def outOfBounds(self):
        if self.position.y - self.length/2.0 < self.world.bounds.ymin:
            return True
        if self.position.y + self.length/2.0 > self.world.bounds.ymax:
            return True
        if self.position.x - self.width/2.0 < self.world.bounds.xmin:
            return True
        if self.position.x + self.width/2.0 > self.world.bounds.xmax:
            return True

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
            if a < .003 or b < .003:
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
    def __init__(self, world, init_xpos, init_ypos):
        self.headColor = "#%06x" % random.randint(0, 0xFFFFFF)
        self.tailColor = "#%06x" % random.randint(0, 0xFFFFFF)
        self.head = SnakeHead(world, init_xpos, init_ypos, None, self.headColor)
        self.tail = SnakeBody(world, self.head, self.tailColor)
        self.snakeList = []
        self.snakeList.append(self.head)
        self.snakeList.append(self.tail)
        self.world = world
        self.length = 2
        self.dead = False

    def grow(self):
        newTail = SnakeBody(self.world, self.tail, self.tailColor)
        self.tail = newTail
        self.length += 1
        self.snakeList.append(self.tail)
    def kill(self):
        self.dead = True
    def changeDir(self, direction):
        if self.dead:
            return

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

    def __init__(self, numSnakes, foodNumber, bw, bh, ww, wh, topology):
        Game.__init__(self,"2PSnake",bw,bh,ww,wh,topology,console_lines=6)
        self.numSnakes = numSnakes
        self.snakeList = []
        for x in range(0, self.numSnakes):
            self.snakeList.append(Snake(self, .5 + (-1)**(x+1)*.2, .5+(-1)**(x+1)*.2))    
        self.food = Apple(self)
        self.foodNumber = foodNumber
        self.game_over = False
        self.report("Players(s): Don't hit either snake's body or the walls.")
        self.report("Player(s): Eat to grow.")
        self.report("player1: use a,w,s,d to move.      player2: use arrow keys to move.")
        self.report("player1: press d to start.         player2: press left arrow to start.")



    def handle_keypress(self,event):       #requires changes!!!

        Game.handle_keypress(self,event)
        if event.char == ' ':
            for snakes in self.snakeList:
                snakes.grow()
        if len(self.snakeList) < 1:
            return
        elif event.char == 'w': #SNEK UP
            if self.snakeList[0].head.direction != "down":
                if self.snakeList[0].head.direction != None:
                    self.snakeList[0].changeDir("up")

        elif event.char == 's': #SNEK DOWN
            if self.snakeList[0].head.direction != "up":
                if self.snakeList[0].head.direction != None:
                    self.snakeList[0].changeDir("down")

        elif event.char == 'd':
            if self.snakeList[0].head.direction != "left":
                self.snakeList[0].changeDir("right")

        elif event.char == 'a':
            if self.snakeList[0].head.direction != "right":
                if self.snakeList[0].head.direction != None:
                    self.snakeList[0].changeDir("left")
        elif len(self.snakeList) < 2:
            return
        elif event.keysym_num == 65364: #SNEK UP
            if self.snakeList[1].head.direction != "up":
                if self.snakeList[1].head.direction != None:
                    self.snakeList[1].changeDir("down")

        elif event.keysym_num == 65361: #SNEK UP
            if self.snakeList[1].head.direction != "right":
                self.snakeList[1].changeDir("left")

        elif event.keysym_num == 65362: #SNEK UP
            if self.snakeList[1].head.direction != "down":
                if self.snakeList[1].head.direction != None:
                    self.snakeList[1].changeDir("up")

        elif event.keysym_num == 65363: #SNEK UP
            if self.snakeList[1].head.direction != "left":
                if self.snakeList[1].head.direction != None:
                    self.snakeList[1].changeDir("right")
                    
    def display_length(self, a):
        self.report("Snake" + str(a) + " is now length: " + str(self.snakeList[a].length))

    def update(self):                #Determines how much eats per food

        if self.foodNumber == 1:
            o = ""
        else:
            o = "s"
        for x in range(0, len(self.snakeList)):
            currentSnake = self.snakeList[x]
            difVector = currentSnake.head.position - self.food.position        #CHECK FOR EATING FOR SNAKE
            if abs(difVector.dx) <= 2*self.food.width and abs(difVector.dy) <= 2*self.food.length:
                i = 0
                while i < self.foodNumber:
                    currentSnake.grow()
                    i+=1
                self.remove(self.food)
                self.food = Apple(self)
                self.report()
                self.report()
                self.report()
                self.report("Snake" + str(x) + " has eaten " + str(self.foodNumber) + " apple" + o + "!")
                self.display_length(x)

            for y in range(0, len(self.snakeList)):
                if y == x:
                    otherSnakeTail = self.snakeList[y].tail
                    currentSnakeHead = currentSnake.head   #MAYBE IGNORE SEFMENT 1 BEFORE HEAD DUE TO TURNING ISSUES!!!
                    while otherSnakeTail.frontSeg != None:
                        difVector = otherSnakeTail.position - currentSnakeHead.position
                        if abs(difVector.dx) <= currentSnakeHead.width/1.1 and abs(difVector.dy) <= currentSnakeHead.length/1.1: #2.01 for janky modern snake #2.00 for classic snake
                            #ADD AN IF STATEMENT!!!!!!!!!!!!!! FOR IF HEADS COLLLIDE!!!!
                            if currentSnakeHead in self.agents: 
                                self.report()
                                self.report()
                                self.report()
                                self.report("Snake" + str(self.snakeList[x]) + " has hit itself and is now dead.")
                                self.remove(currentSnakeHead)
                                self.snakeList[x].kill()
                            #self.GAME_OVER = True
                        otherSnakeTail = otherSnakeTail.frontSeg
                else:
                    otherSnakeTail = self.snakeList[y].tail
                    currentSnakeHead = currentSnake.head   #MAYBE IGNORE SEFMENT 1 BEFORE HEAD DUE TO TURNING ISSUES!!!
                    while otherSnakeTail.frontSeg != None:
                        difVector = otherSnakeTail.position - currentSnakeHead.position
                        if abs(difVector.dx) <= currentSnakeHead.width/1.1 and abs(difVector.dy) <= currentSnakeHead.length/1.1: #2.01 for janky modern snake #2.00 for classic snake
                            #ADD AN IF STATEMENT!!!!!!!!!!!!!! FOR IF HEADS COLLLIDE!!!!
                            if currentSnakeHead in self.agents: 
                                self.report()
                                self.report()
                                self.report()
                                self.report("Snake" + str(self.snakeList[x]) + " has hit Snake" + str(self.snakeList[y]) + " and is now dead.")
                                self.remove(currentSnakeHead)
                                self.snakeList[x].kill()
                            #self.GAME_OVER = True
                        otherSnakeTail = otherSnakeTail.frontSeg
                    difVector = otherSnakeTail.position - currentSnakeHead.position
                    if abs(difVector.dx) <= currentSnakeHead.width/1.1 and abs(difVector.dy) <= currentSnakeHead.length/1.1: #2.01 for janky modern snake #2.00 for classic snake
                        if otherSnakeTail in self.agents:
                            self.report()
                            self.report()
                            self.report()
                            self.report("Snakes " + str(self.snakeList[x]) + " and " + str(self.snakeList[y]) + " have bumped heads and are now dead.")
                            self.remove(otherSnakeTail)
                            self.snakeList[y].kill()
                        if currentSnakeHead in self.agents:
                            self.remove(currentSnakeHead)
                            self.snakeList[x].kill()
        
        if self.topology == 'wrapped':
            for x in self.snakeList:
                for segments in x.snakeList:
                    if segments.outOfBounds():
                        segments.position = Bounds.wrap(self.bounds, segments.position)
        else:
            for x in self.snakeList:
                if x.head in self.agents and x.head.outOfBounds() == True:
                    self.remove(x.head)
                    self.report(str(x) + " has run into a wall")

        i = 0
        for x in self.snakeList:
            if x.dead == True:
                i+=1
        if len(self.snakeList)-i == 1:
            if not self.game_over:
                self.report("GAME IS OVER. GOOD JOB WINNER!" + "\n" + "FIX THIS FOR TIED GAMES!!!")
            self.game_over = True
        elif len(self.snakeList)-i == 0:
            self.report("everybody ded")
            self.GAME_OVER = True

        Game.update(self)
"""
game = PlaySnake()
while not game.GAME_OVER:
    time.sleep(4.0/60.0)  #1.0 for janky modern snake   #4.0 for classic snake
    game.update()
"""
