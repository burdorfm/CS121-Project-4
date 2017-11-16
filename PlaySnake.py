from tkinter import *
from Game import *
from geometry import *
from LinkedList import *

import math
import random
import time

class Snake(Agent):
    START_X = """X position of bottom left"""
    START_Y = """Y position of bottom left"""
    WRAPPING = True
    SPEED = """arbitrary number for now"""

    def __init__(self, world, scaleList):
        scaleList = LinkedList()
        scaleList.first = Segment("""with information maybe""")
        


        Agent.__init__(self,position,world)

class Segment(Snake):

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
        self.left_turn   = random.choice([True,False])
        self.reset()

        self.left_paddle  = Paddle(self,left_paddle=True)
        self.right_paddle = Paddle(self,left_paddle=False)

    def handle_keypress(self,event):
        Game.handle_keypress(self,event)
        if event.char == ' ':
            self.use_mouse = not self.use_mouse
        elif event.char == 'a' and not self.use_mouse:
            self.left_paddle.move_up()
        elif event.char == 'z' and not self.use_mouse:
            self.left_paddle.move_down()
        elif event.char == '\'' and not self.use_mouse:
            self.right_paddle.move_up()
        elif event.char == '/' and not self.use_mouse:
            self.right_paddle.move_down()
        elif event.char == 'x' and not self.use_mouse:
            if self.left_turn and self.serving:
                self.serving = False
        elif event.char == '.' and not self.use_mouse:
            if (not self.left_turn) and self.serving:
                self.serving = False

    def handle_mouse_release(self,event):
        Game.handle_mouse_release(self,event)
        if self.use_mouse:
            self.serving = False

    def reset(self):
        self.ticks_before_start = 100
        self.ball = None

    def serve(self):
        self.ball = Ball(self,left_serve=self.left_turn)
        if self.left_turn:
            if self.use_mouse:
                self.report("It's LEFT's serve. Click to send the ball.")
            else:
                self.report("It's LEFT's serve. Hit 'x' to send the ball.")
        else:
            if self.use_mouse:
                self.report("It's RIGHT's serve. Click to send the ball.")
            else:
                self.report("It's RIGHT's serve. Hit '.' to send the ball.")
        self.serving = True

    def display_score(self):
        self.report("LEFT:"+str(self.left_score)+"\tRIGHT:"+str(self.right_score))

    def update(self):
        if self.ball == None:
            self.ticks_before_start -= 1
            if self.ticks_before_start <= 0:
                self.serve()

        Game.update(self)

        if self.ball != None:
            if self.ball.position.x <= self.bounds.xmin:
                self.ball.leave()
                self.right_score += 1
                self.report()
                self.report()
                self.report()
                self.report()
                self.report("RIGHT SCORES A POINT!")
                self.display_score()
                self.left_turn = not self.left_turn
                self.reset()
            elif self.ball.position.x >= self.bounds.xmax:
                self.ball.leave()
                self.left_score += 1
                self.report()
                self.report()
                self.report()
                self.report()
                self.report("LEFT SCORES A POINT!")
                self.display_score()
                self.left_turn = not self.left_turn
                self.reset()
            
game = PlayPong()
while not game.GAME_OVER:
    time.sleep(1.0/60.0)
    game.update()








class SnakeList:
        self.scaleList = scaleList #stores all scales

        position = world.bounds.point_at() #head scale position
        scaleList.append(Scale("""FILL!!!"""))
        scaleList[0] = 
        Agent.__init__(self,position,world)    


"""linked list of snek segments"""

class Segment:


        
