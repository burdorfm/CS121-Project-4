from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time

class Paddle(Agent):

    START_X   = 0.8
    START_Y   = 0.8
    WIDTH     = 3
    LENGTH    = 3
    AGILITY   = .1

    def __init__(self,world,left_paddle=True):
        self.on_left = left_paddle
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.direction = "right"
        xoffset = -self.START_X if left_paddle else  self.START_X
        yoffset =  self.START_Y if left_paddle else -self.START_Y
        position = world.bounds.point_at((xoffset+1.0)/2.0,(yoffset+1.0)/2.0)
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
        if self.on_left:
            return "#FF8040"
        else:
            return "#FF8040"

    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)       
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1,p2,p3,p4]
        
    def move_down(self):
        self.position.y -= self.length * self.AGILITY
        self.keep_within_bounds()
    def move_up(self):
        self.position.y += self.length * self.AGILITY
        self.keep_within_bounds()
    def move_left(self):
        self.position.x -= self.length * self.AGILITY
        self.keep_within_bounds()
    def move_right(self):
        self.position.x += self.length * self.AGILITY
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
                
class Ball(Agent):

    START_X   = 0.75
    SPEED     = 0.25

    def __init__(self,world,left_serve=True):
        dx = 1.0 if left_serve else -1.0
        dy = random.uniform(-3.0,3.0)
        self.heading = Vector2D(dx,dy)
        offset = -self.START_X if left_serve else self.START_X
        position = world.bounds.point_at((1.0+offset)/2.0,random.random())
        Agent.__init__(self,position,world)

    def check_bounce_horizontal(self,y_value,from_above=True):
        if from_above:
            if self.position.y >= y_value:
                self.position.y = y_value - abs(self.position.y-y_value)
                self.heading.dy = -self.heading.dy
        else:
            if self.position.y <= y_value:
                self.position.y = y_value + abs(self.position.y-y_value)
                self.heading.dy = -self.heading.dy

    def check_bounce_vertical(self,x_value,from_left=True):
        if from_left:
            if self.position.x >= x_value:
                self.position.x = x_value - abs(self.position.x-x_value)
                self.heading.dx = -self.heading.dx
        else:
            if self.position.x <= x_value:
                self.position.x = x_value + abs(self.position.x-x_value)
                self.heading.dx = -self.heading.dx
            
    def update(self):
        if not self.world.serving:
            old_position = self.position
            new_position = self.position + self.heading * self.SPEED
            self.position = new_position
            if self.world.left_paddle.hits_between(old_position,new_position):
                self.check_bounce_vertical(self.world.left_paddle.position.x,from_left=False)
            if self.world.right_paddle.hits_between(old_position,new_position):
                self.check_bounce_vertical(self.world.right_paddle.position.x,from_left=True)
            self.check_bounce_horizontal(self.world.bounds.ymin,from_above=False)
            self.check_bounce_horizontal(self.world.bounds.ymax,from_above=True)
        else:
            if self.world.left_turn: 
                paddle = self.world.left_paddle
            else:
                paddle = self.world.right_paddle
            self.position = Point2D(paddle.position.x,paddle.position.y)

    def color(self):
        return "#B0F080"

    def shape(self):
        p1 = self.position + Vector2D( 0.5, 0.5)       
        p2 = self.position + Vector2D(-0.5, 0.5)        
        p3 = self.position + Vector2D(-0.5,-0.5)        
        p4 = self.position + Vector2D( 0.5,-0.5)
        return [p1,p2,p3,p4]
            

class PlayPong(Game):

    def __init__(self):
        Game.__init__(self,"PONG",60.0,45.0,800,600,topology='bound',console_lines=6)
        
        self.report("Left player:  hit 'a' or 'z'.")
        self.report("Right player: hit apostrophe or '/'.")
        self.report("Hit SPACE to switch mouse mode on/off.")
        self.report("Mac users will want to make this window full screen.")

        self.left_score  = 0
        self.right_score = 0
        self.use_mouse   = False

        self.left_paddle  = Paddle(self,left_paddle=True)
        print("hello")

    def handle_keypress(self,event):
        Game.handle_keypress(self,event)
        if event.char == ' ':
            self.use_mouse = not self.use_mouse
        elif event.char == 'w' and not self.use_mouse: #SNEK UP
            self.left_paddle.changeDirection("up")
        elif event.char == 's' and not self.use_mouse: #SNEK DOWN
            self.left_paddle.changeDirection("down")
        elif event.char == 'd' and not self.use_mouse:
            self.left_paddle.changeDirection("right")
        elif event.char == 'a' and not self.use_mouse:
            self.left_paddle.changeDirection("left")

        #NEED A CHECK FOR IF EVENT 180 degrees from movement vector

    #def reset()

    #def populate????

    def display_score(self):
        self.report("LEFT:"+str(self.left_score)+"\tRIGHT:"+str(self.right_score))

    def update(self):
        Game.update(self)

game = PlayPong()
while not game.GAME_OVER:
    time.sleep(1.0/60.0)
    game.update()
