from tkinter import *
from Game import *
from geometry import *
import math
import random
import time
import Two_Player_Snake
import tkinter as tk

class SnakeMenuRunner:
    def __init__(self):
        #Game.__init__(self,"Snake Menu",60,45,800,600,topology='wrapped',console_lines=6)
        """
        self.report("Players(s): Don't hit either snake's body or the walls.")
        self.report("Player(s): Eat to grow.")
        self.report("player1: use a,w,s,d to move.      player2: use arrow keys to move.")
        self.report("player1: press d to start.         player2: press left arrow to start.")
        """ #steal report
        self.INIT_WIDTH = 500
        self.INIT_HEIGHT = 600
        self.explanation = None
        self.root = tk.Tk()
        self.root.geometry(str(self.INIT_WIDTH)+"x"+str(self.INIT_HEIGHT))
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=BOTH, expand=1)
        self.howMany = 0
        #MAKE A FRAME OF 400X300
        
        self.header = tk.Button(self.frame, text="Snake Menu", fg="red", command=self.write_explanation)
        self.header.place(x = 200,y = 10)

        self.below = tk.Button(self.frame, text="Select one option from each row below.", fg="Red", command=None)
        self.below.place(x=120, y=30)

        self.choice1 = tk.Button(self.frame, text="Number of Players:", fg="Red", command=None)
        self.choice1.place(x = 30,y = 60)

        self.singleplayer = tk.Button(self.frame, text = "One Player", fg = "Green", command = None) #'self.players(1)'
        self.singleplayer.place(x = 180, y = 60)

        self.twoplayer = tk.Button(self.frame, text = "Two Players", fg = "Green", command = None)
        self.twoplayer.place(x = 275, y = 60)
        
        self.choice2 = tk.Button(self.frame, text="Movement Speed:", fg="Red", command=None)
        self.choice2.place(x = 30,y = 100)

        self.slow = tk.Button(self.frame, text="Slow", fg="Green", command=None)
        self.slow.place(x = 180, y = 100)

        self.medium = tk.Button(self.frame, text="Medium", fg="Green", command=None)
        self.medium.place(x = 240, y = 100)

        self.fast = tk.Button(self.frame, text="Fast", fg="Green", command=None)
        self.fast.place(x = 320, y = 100)

        self.tailgrowth = tk.Button(self.frame, text="Tail Growth:", fg="Red", command=None)
        self.tailgrowth.place(x = 30, y = 140)

        self.growone = tk.Button(self.frame, text= "One", fg="Green", command=None)
        self.growone.place(x = 180, y = 140)

        self.growtwo = tk.Button(self.frame, text="Two", fg="Green", command=None)
        self.growtwo.place(x = 245, y = 140)

        self.growthree = tk.Button(self.frame, text="Three", fg="Green", command=None)
        self.growthree.place(x = 310, y = 140)

        self.arenaisze = tk.Button(self.frame, text="Arena Size: ", fg="Red", command=None)
        self.arenaisze.place(x = 30, y = 180)

        self.smallarena = tk.Button(self.frame, text="Small", fg="Green", command=None)
        self.smallarena.place(x = 175, y = 180)

        self.mediumarena = tk.Button(self.frame, text="Medium", fg="Green", command=None)
        self.mediumarena.place(x = 235, y = 180)

        self.largearena = tk.Button(self.frame, text="Large", fg="Green", command=None)
        self.largearena.place(x = 310, y = 180)

        self.gametypes = tk.Button(self.frame, text="Game Modes: Pick one from each row.", fg="Green", command=None)
        self.gametypes.place(x = 120, y = 240)

        self.mode1 = tk.Button(self.frame, text="Game Style:", fg="Red", command=None)
        self.mode1.place(x = 30, y = 280)

        self.modern = tk.Button(self.frame, text="Modern", fg="Green", command=None)
        self.modern.place(x = 180, y = 280)

        self.arcademode = tk.Button(self.frame, text="Arcade", fg="Green", command=None)
        self.arcademode.place(x = 260, y = 280)

        self.snakestyle = tk.Button(self.frame, text="Snake Style:", fg="Red", command=None)
        self.snakestyle.place(x = 30, y = 320)

        self.crazy = tk.Button(self.frame, text="Crazy", fg="Green", command=None)
        self.crazy.place(x = 170, y = 320)

        self.skele = tk.Button(self.frame, text="Skeleton", fg="Green", command=None)
        self.skele.place(x = 240, y = 320)

        self.regular = tk.Button(self.frame, text="Regular", fg="Green", command=None)
        self.regular.place(x = 330, y = 320)

        self.bulletsnakes = tk.Button(self.frame, text="Enable Bullets?", fg="Red", command=None)
        self.bulletsnakes.place(x = 30, y = 360)

        self.yesbullets = tk.Button(self.frame, text="Yes", fg="Green", command=None)
        self.yesbullets.place(x = 180, y = 360)

        self.nobullets = tk.Button(self.frame, text="No", fg="Green", command=None)
        self.nobullets.place(x= 240, y = 360)

        self.wrap_or_no = tk.Button(self.frame, text="No Boundries?", fg="Red", command=self.wrap_explain)
        self.wrap_or_no.place(x= 30, y = 400)

        self.yeswrap = tk.Button(self.frame, text="Yes", fg="Green", command=None)
        self.yeswrap.place(x = 180, y = 400)

        self.nowrap = tk.Button(self.frame, text="No", fg="Green", command=None)
        self.nowrap.place(x= 240, y = 400)

        self.playthegame = tk.Button(self.frame, text = "Play with these settings", fg = "Red", command = self.play)
        self.playthegame.place(x = 150, y = 500)

        #add settings, arena size: small, medium, large, other styles

        self.use_mouse = True  #maybe use a mouse thing to determine snake movement

    def wrap_explain(self):
        self.explanation = tk.Button(self.frame, text="Running into the wall will cause you to enter on the other side of the map.", fg="Green", command= self.dont_click_me)
        self.explanation.place(x= 20, y = 430)
    def write_explanation(self):
        self.explanation = tk.Button(self.frame, text="<--This is the snake menu", fg="red", command=self.dont_click_me)
        self.explanation.place(x = 295, y = 10)
    def setHowMany1(self):
        self.howMany = 1
    def setHowMany2(self):
        self.howMany = 2
    def dont_click_me(self):
        print("don't click me")
    def play(self):
        #game = chosen_game
        game = Two_Player_Snake.PlaySnake(2, 3, 200, 150, 800, 600, 'yguyjgjkyhgjk')
        while not game.GAME_OVER:
            time.sleep(.1/60.0)  # 1.0 is placeholder for variable that changes snake from arcade to modern
            game.update()

a = SnakeMenuRunner()






