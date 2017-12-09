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


"""

#a = [ "FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", "00FFFF", "000000", "800000", "008000", "000080", "808000", "800080", "008080", "808080", "C00000", "00C000", "0000C0", "C0C000", "C000C0", "00C0C0", "C0C0C0", "400000", "004000", "000040", "404000", "400040", "004040", "404040", "200000", "002000", "000020", "202000", "200020", "002020", "202020", "600000", "006000", "000060", "606000", "600060", "006060", "606060", "A00000", "00A000", "0000A0", "A0A000", "A000A0", "00A0A0", "A0A0A0", "E00000", "00E000", "0000E0", "E0E000", "E000E0", "00E0E0", "E0E0E0"]

class SnakeHead(Agent):

    WIDTH     = 1
    LENGTH    = 1

    def __init__(self,world, xpos, ypos, direction, color, agility):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.frontSeg = None
        self.direction = direction
        self.agility = agility  #/4 for janky modern snake  #/1 for classic snake
        self.position = world.bounds.point_at(xpos,ypos)
        self.initColor = color#"#%06x" % random.randint(0, 0xFFFFFF)
        self.storedDirection = direction
        Agent.__init__(self,self.position,world)

    def color(self):
        return self.initColor
    
    def shape(self): #shape of the head
        p1 = self.position + Vector2D( self.width, self.length)       
        p2 = self.position + Vector2D(-self.width, self.length)        
        p3 = self.position + Vector2D(-self.width,-self.length)       
        p4 = self.position + Vector2D( self.width,-self.length)       
        return [p1, p2, p3, p4]

    def outOfBounds(self): #determines whether the head is out of bounds or not
        if self.position.y - self.length/2.0 < self.world.bounds.ymin:
            return True
        if self.position.y + self.length/2.0 > self.world.bounds.ymax:
            return True
        if self.position.x - self.width/2.0 < self.world.bounds.xmin:
            return True
        if self.position.x + self.width/2.0 > self.world.bounds.xmax:
            return True

        
    def move_down(self): #snake movements
        self.position.y -= self.agility
    def move_up(self):
        self.position.y += self.agility
    def move_left(self):
        self.position.x -= self.agility
    def move_right(self):
        self.position.x += self.agility

    def updatePos(self, direction): #tells snake to change directions
        if direction == "up":
            self.move_up()
        elif direction == "down":           
            self.move_down()
        elif direction == "right":
            self.move_right()
        elif direction == "left":
            self.move_left()

    def changeDirection(self, direction): #gives snake the new direction attribute 
        self.storedDirection = self.direction
        self.direction = direction
        
    def update(self):
        self.updatePos(self.direction)

class SnakeBody(Agent): # objects that follow the head. each follows the object in front of it.
    def __init__(self,world,followObject, color, minAdd, maxAdd):
        self.position = self.initPosition(followObject, minAdd, maxAdd)
        self.length = followObject.length
        self.width = followObject.width
        self.direction = followObject.direction
        self.frontSeg = followObject
        self.storedFrontSegDirection = self.direction
        self.turnPositions = [[],[],[]]
        self.storedDirection = self.direction
        self.agility = followObject.agility #followObject.agility
        self.initColor = color#"#%06x" % random.randint(0, 0xFFFFFF)

        Agent.__init__(self,self.position,world)
        #instantiates

    def initPosition(self, followObject, minAdd, maxAdd): #initializes the position of the tail segment, tells it to follow object in front of it
        a = random.randint(minAdd,maxAdd)
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
    
    def outOfBounds(self): #checks to see if tail segment is out of bounds
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

    def shape(self): #shaoe of tail segment
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
        if self.frontSeg.storedDirection != self.frontSeg.direction: #segment turns at point where segment in front of it turns
            self.turnPositions[0].append(self.frontSeg.position.x)
            self.turnPositions[1].append(self.frontSeg.position.y)
            self.turnPositions[2].append(self.frontSeg.direction)
            self.frontSeg.storedDirection = self.frontSeg.direction

        if len(self.turnPositions[0]) > 0: # tells segment where to turn
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
        if (self.direction == "up" and direction == "down") or (self.direction == "down" and direction == "up") or (self.direction == "left" and direction == "right") or (self.direction == "right" and direction == "left"):
            return # prevents snake from moving backwards
        self.storedDirection = self.direction
        self.direction = direction

    def update(self):
        self.updatePos(self.direction)

class Bullet(Agent): # bullet that the snake can shoot as weapon (useful for two player snake)
    def __init__(self, world, head):
        self.length = head.length*1.5
        self.width  = head.width*1.5
        self.direction = head.direction
        self.agility = 2*head.agility
        self.position = self.initPosition(head)
        self.initColor = "#%06x" % random.randint(0, 0xFFFFFF)
        Agent.__init__(self,self.position,world)

    def color(self):
        return self.initColor

    def initPosition(self, followObject):
        a = 4
        if followObject.direction == None:
            return
        if followObject.direction == "left":
            return followObject.position + Vector2D(-a*followObject.width, 0)
        elif followObject.direction == "right":
            return followObject.position + Vector2D(a*followObject.width, 0)
        elif followObject.direction == "down":
            return followObject.position + Vector2D(0, -a*followObject.length)
        elif followObject.direction == "up":
            return followObject.position + Vector2D(0, a*followObject.length)

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
    

class Snake: #the snake
    def __init__(self, world, init_xpos, init_ypos, agility, minAdd, maxAdd):
        self.headColor = "#%06x" % random.randint(0, 0xFFFFFF)
        self.tailColor = "#%06x" % random.randint(0, 0xFFFFFF)
        self.head = SnakeHead(world, init_xpos, init_ypos, None, self.headColor, agility)
        self.tail = SnakeBody(world, self.head, self.tailColor, minAdd, maxAdd)
        self.minAdd = minAdd
        self.maxAdd = maxAdd
        self.snakeList = []
        self.snakeList.append(self.head)
        self.snakeList.append(self.tail)
        self.world = world
        self.length = 2
        self.dead = False
    def shoot(self): #shoots a bullet in direction of snake
        if self.head.direction == None:
            return
        if self.length == 1:
            return
        temp = self.tail
        self.tail = self.tail.frontSeg
        self.world.remove(temp)
        self.snakeList.remove(temp)
        self.length -= 1
        a = Bullet(self.world, self.head)
        self.snakeList.append(a)
    def shrink(self): # for snake dodge ball
        self.length -= 1
        temp = self.tail
        self.tail = self.tail.frontSeg
        self.world.remove(temp)
    def grow(self): # for snake dodge ball
        newTail = SnakeBody(self.world, self.tail, self.tailColor, self.minAdd, self.maxAdd)
        self.tail = newTail
        self.length += 1
        self.snakeList.append(self.tail)
    def kill(self):
        self.dead = True
    def changeDir(self, direction):
        if self.dead:
            return
        if self.head.direction == direction:
            return

        self.head.changeDirection(direction)
    def outOfBounds(self):
        if self.head.outOfBounds() == True:
            return True
        return False

class Apple(Agent): # food for the snake
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

    def __init__(self, numSnakes, foodNumber, bw, bh, ww, wh, topology, agility, bullets, gameType):
        Game.__init__(self,"Snake",bw,bh,ww,wh,topology,console_lines=6)
        if gameType == "Crazy":
            self.minAdd = 1
            self.maxAdd = 20
            self.minDist =2.01# 1.1 / self.minAdd 
        elif gameType == "Traditional":
            self.minAdd = 1
            self.maxAdd = 1
            self.minDist =2.01
        else:
            self.minAdd = 2
            self.maxAdd = 2
            self.minDist =1.01
        self.numAlive = numSnakes
        self.numStarted = numSnakes
        self.bullets = bullets
        self.numSnakes = numSnakes
        self.snakeList = []
        for x in range(0, self.numSnakes):
            self.snakeList.append(Snake(self, .5 + (-1)**(x+1)*.2, .5+(-1)**(x+1)*.2, agility, self.minAdd, self.maxAdd))
        self.food = Apple(self)
        self.foodNumber = foodNumber
        self.game_over = False
        if self.numSnakes == 2:
            self.report("player1: use a,w,s,d to move.      player2: use j,k,i,l keys to move.")
            if self.bullets:
                self.report("player1 shoots with 'f' and player2 shoots with ';'")
            if topology != "wrapped":
                self.report("do not hit walls or any snake's body. that will kill you")
            else:
                self.report("passing into a wall will let you wrap around the screen")
            self.report("player1: press d to start, player2: press left arrow to start, collect food to grow")
        elif self.numSnakes == 1:
            self.report("use a,w,s,d to move.")
            if self.bullets:
                self.report("you shoot with 'f'")
            if topology != "wrapped":
                self.report("do not hit walls or your body. that will kill you")
            else:
                self.report("passing into a wall will let you wrap around the screen")
            self.report("collect food to grow, press d to start")
            

    def handle_keypress(self,event):       # relates keypress to action
        Game.handle_keypress(self,event)
        """if event.char == ' ':
            for snakes in self.snakeList:
                snakes.grow()"""
        if event.char == 'f':
            if self.bullets:
                self.snakeList[0].shoot()
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
        elif event.char == ';':
            if self.bullets:
                self.snakeList[1].shoot()
        elif event.char == "k": 
            if self.snakeList[1].head.direction != "up":
                if self.snakeList[1].head.direction != None:
                    self.snakeList[1].changeDir("down")
        elif event.char == "j": 
            if self.snakeList[1].head.direction != "right":
                self.snakeList[1].changeDir("left")
        elif event.char == "i": 
            if self.snakeList[1].head.direction != "down":
                if self.snakeList[1].head.direction != None:
                    self.snakeList[1].changeDir("up")
        elif event.char == "l": 
            if self.snakeList[1].head.direction != "left":
                if self.snakeList[1].head.direction != None:
                    self.snakeList[1].changeDir("right")
                    
    def display_length(self, a): #displays length of snake
        self.report(str(self.snakeList[a]) + " is now length: " + str(self.snakeList[a].length))

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
                self.report(str(self.snakeList[x]) + " has eaten " + str(self.foodNumber) + " apple" + o + "!")
                self.display_length(x)

            for y in range(0, len(self.snakeList)):
                if y == x:
                    h = 0
                    currentSnakeHead = currentSnake.head
                    for otherSnakeTail in self.snakeList[y].snakeList:
                        if h == 0:
                            h+=1
                            continue
                        difVector = otherSnakeTail.position - currentSnakeHead.position
                        if currentSnakeHead.agility / otherSnakeTail.agility < 1:
                            difVector = otherSnakeTail.position - currentSnakeHead.position
                            print(difVector)
                            if abs(difVector.dx) <= currentSnakeHead.width/.34 and abs(difVector.dy) <= currentSnakeHead.length/.34: #2.01 for janky modern snake #2.00 for classic snake
                                if currentSnakeHead in self.agents: 
                                    self.report()
                                    self.report()
                                    self.report()
                                    self.report("Snake" + str(self.snakeList[x]) + " has missiled Snake" + str(self.snakeList[y]) + " and is now dead.")
                                    self.remove(currentSnakeHead)
                                    self.snakeList[x].kill()
                                    self.numAlive -= 1
                            #self.GAME_OVER = True
                            continue
                        if abs(difVector.dx) <= currentSnakeHead.width/self.minDist and abs(difVector.dy) <= currentSnakeHead.length/self.minDist: #2.01 for janky modern snake #2.00 for classic snake
                            #ADD AN IF STATEMENT!!!!!!!!!!!!!! FOR IF HEADS COLLLIDE!!!!
                            if currentSnakeHead in self.agents: 
                                self.report()
                                self.report()
                                self.report()
                                self.report("Snake" + str(self.snakeList[x]) + " has hit Snake" + str(self.snakeList[y]) + " and is now dead.")
                                self.remove(currentSnakeHead)
                                self.snakeList[x].kill()
                                self.numAlive -= 1
                            #self.GAME_OVER = True
                    
                else:
                    currentSnakeHead = currentSnake.head
                    for otherSnakeTail in self.snakeList[y].snakeList:
                        if currentSnakeHead.agility / otherSnakeTail.agility < 1:
                            difVector = otherSnakeTail.position - currentSnakeHead.position
                            if abs(difVector.dx) <= currentSnakeHead.width/.34 and abs(difVector.dy) <= currentSnakeHead.length/.34: #2.01 for janky modern snake #2.00 for classic snake
 
                                if currentSnakeHead in self.agents: 
                                    self.report()
                                    self.report()
                                    self.report()
                                    self.report("Snake" + str(self.snakeList[x]) + " has missiled Snake" + str(self.snakeList[y]) + " and is now dead.")
                                    self.remove(currentSnakeHead)
                                    self.snakeList[x].kill()
                                    self.numAlive -= 1
                            #self.GAME_OVER = True
                            continue
                        difVector = otherSnakeTail.position - currentSnakeHead.position
                        if abs(difVector.dx) <= currentSnakeHead.width/self.minDist and abs(difVector.dy) <= currentSnakeHead.length/self.minDist: #2.01 for janky modern snake #2.00 for classic snake
                            #ADD AN IF STATEMENT!!!!!!!!!!!!!! FOR IF HEADS COLLLIDE!!!!
                            if currentSnakeHead in self.agents: 
                                self.report()
                                self.report()
                                self.report()
                                self.report("Snake" + str(self.snakeList[x]) + " has hit Snake" + str(self.snakeList[y]) + " and is now dead.")
                                self.remove(currentSnakeHead)
                                self.snakeList[x].kill()
                                self.numAlive -= 1
                            #self.GAME_OVER = True
        
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
                    self.numAlive -= 1

        i = 0
        for x in self.snakeList:
            quiklist = []
            if x.dead == True:
                continue
            quiklist.append(x)
        if self.numAlive == 1 and self.numStarted == 2:
            if not self.game_over:
                if len(quiklist) == 1:
                    self.report(str(quiklist[0]) + "has won the game!!!" + "\nGAME IS OVER. GOOD JOB WINNER!")
            self.game_over = True
        if self.numAlive == 0:
            self.report("everybody ded, this game instance will now close (please wait)")
            self.GAME_OVER = True
        Game.update(self)
    def removeThis(self):
        time.sleep(3.0)
        self.canvas.pack_forget()
        self.root.destroy()

class PlayDodgeBall(Game): #our game within our main gamee
    def __init__(self, bw, bh, ww, wh, topology = "wrapped"):
        Game.__init__(self,"Snake",bw,bh,ww,wh,topology,console_lines=6)
        self.dodger = Snake(self, .3, .3, .5, 1, 1)
        self.dodger.shrink()
        self.game_over = False
        self.time0 = time.time()
        self.counter = 1
        self.report("this is dodgeball!!! dodge the balls")
        self.report("plot twist! you are throwing them")
        self.report("press w,a,s or d to start")
        self.report("try to survive")

    def handle_keypress(self,event):
        Game.handle_keypress(self,event)
        if (event.char == 'w' or event.char == 's' or event.char == 'd' or event.char == 'a') and self.dodger.head.direction == None:
            self.time0 = time.time()
        if event.char == 'w': 
            self.dodger.changeDir("up")
        elif event.char == 's': 
            self.dodger.changeDir("down")
        if event.char == 'd':
            self.dodger.changeDir("right")
        if event.char == 'a':
            self.dodger.changeDir("left")
                
    def update(self):
        if self.dodger.head.direction == None:
            doNothing = None
        else:
            self.time1 = time.time()
            if self.time1 - self.time0 > self.counter:
                self.dodger.grow()
                self.dodger.shoot()
                self.counter += 1
                self.report("Snake has survived for " + str(int(self.time1 - self.time0)) + " seconds")

            for segments in self.dodger.snakeList:
                if segments.outOfBounds():
                    segments.position = Bounds.wrap(self.bounds, segments.position)
    

            i = 0
            for x in self.dodger.snakeList:
                if i == 0:
                    i+=1
                    continue
                if len(self.dodger.snakeList) == 1:
                    continue
                if x.agility / self.dodger.head.agility > 1:
                    difVector = x.position - self.dodger.head.position
                    if abs(difVector.dx) <= 1/.30 and abs(difVector.dy) <= 1/.30:
                        self.report("you have died")
                        self.report("Congrats! You survived for " + str(int(self.time1 - self.time0)) + " seconds.")
                        self.GAME_OVER = True

        Game.update(self)
    def removeThis(self):
        time.sleep(4.5)
        #self.destroy()
        #self.canvas.destroy()
        self.canvas.pack_forget()
        self.root.destroy()
        
        
    
