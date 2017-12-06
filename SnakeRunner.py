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
        self.INIT_HEIGHT = 300
        self.explanation = None
        self.root = tk.Tk()
        self.root.geometry(str(self.INIT_WIDTH)+"x"+str(self.INIT_HEIGHT))
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=BOTH, expand=1)
        self.howMany = 0
        #MAKE A FRAME OF 400X300
        
        self.header = tk.Button(self.frame, text="Snake Menu", fg="red", command=self.write_explanation)
        self.header.place(x = 200,y = 10)

        self.choice1 = tk.Button(self.frame, text="Choice1:", fg="Green", command=self.play)
        self.choice1.place(x = 150,y = 60)
        
        self.use_mouse   = True  #maybe use a mouse thing to determine snake movement

    def write_explanation(self):
        self.explanation = tk.Button(self.frame, text="<--This is the snake menu", fg="red", command=self.dont_click_me)
        self.explanation.place(x = 288, y = 10)
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






