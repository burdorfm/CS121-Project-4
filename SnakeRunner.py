from tkinter import *
from Game import *
from geometry import *
import math
import random
import time
import Two_Player_Snake
import tkinter as tk

class SnakeMenuRunner:
    def __init__(self, console_lines = 8):
        #Game.__init__(self,"Snake Menu",60,45,800,600,topology='wrapped',console_lines=6)
        """
        self.report("Players(s): Don't hit either snake's body or the walls.")
        self.report("Player(s): Eat to grow.")
        self.report("player1: use a,w,s,d to move.      player2: use arrow keys to move.")
        self.report("player1: press d to start.         player2: press left arrow to start.")
        """ #steal report

        self.INIT_WIDTH = 600
        self.INIT_HEIGHT = 650
        self.explanation = None
        self.root = tk.Tk()
        self.root.geometry(str(self.INIT_WIDTH)+"x"+str(self.INIT_HEIGHT))
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=BOTH, expand=1)
        self.Canvas = Canvas(self.frame, width = self.INIT_WIDTH, height = 500)
        self.Canvas.pack()
        self.x_size = 150
        self.y_size = 90
        self.n = 1.0/60
        self.trollCount = 0
        #MAKE A FRAME OF 400X300
        self.line = self.Canvas.create_line(470, 0, 470, 500, fill="#476042", width = 5)

        if console_lines > 0:
            self.text = Text(self.root,height=console_lines,bg="#000000",fg="#A0F090",width=115)
            self.text.pack()
        else:
            self.text = None

        self.currentChoice = tk.Button(self.frame, text="Current Choice", fg="red", command=self.explain_currentChoice)
        self.currentChoice.place(x = 485, y = 10)

        self.currentChoice = tk.Button(self.frame, text="(initially default)", fg="red", command=lambda: self.dont_click_me())
        self.currentChoice.place(x = 480, y = 30)

        self.Choice = tk.Button(self.frame, text = "one player", fg = "Green", command = lambda: self.report("ohmmmmmmmmmmmmm - I'm meditating")) #'self.players(1)'
        self.Choice.place(x = 485, y = 60)
        self.Choice.configure(width = 10)

        self.Choice2 = tk.Button(self.frame, text = "slider number", fg = "Green", command = lambda: self.report("The number above the slider to the left gives the current growth amount (default\n  is 5)")) #'self.players(1)'
        self.Choice2.place(x = 485, y = 100)
        self.Choice2.configure(width = 10)

        self.Choice3 = tk.Button(self.frame, text = "medium", fg = "Green", command = lambda: self.report("Do not click me")) #'self.players(1)'
        self.Choice3.place(x = 485, y = 180)
        self.Choice3.configure(width = 10)

        self.Choice4 = tk.Button(self.frame, text = "slider number", fg = "Green", command = lambda: self.report("The number above the slider to the left gives the current growth amount (default\n  is 1)")) #'self.players(1)'
        self.Choice4.place(x=485, y=140)
        self.Choice4.configure(width = 10)

        self.Choice5 = tk.Button(self.frame, text = "bullets are off", fg = "Green", command = lambda: self.dont_click_me)
        self.Choice5.place(x= 485, y = 360)
        self.Choice5.configure(width = 10)

        self.Choice6 = tk.Button(self.frame, text = "doesn't wrap", fg = "Green", command = lambda: self.report("click clack")) #'self.players(1)'
        self.Choice6.place(x = 485, y = 400)
        self.Choice6.configure(width = 10)

        self.Choice7 = tk.Button(self.frame, text = "modern", fg = "Green", command = lambda: self.report("Do not click me")) #'self.players(1)'
        self.Choice7.place(x = 485, y = 280)
        self.Choice7.configure(width = 10)

        self.Choice8 = tk.Button(self.frame, text = "Traditional", fg = "Green", command = lambda: self.report("stuff")) #'self.players(1)'
        self.Choice8.place(x = 485, y = 320)
        self.Choice8.configure(width = 10)

        self.header = tk.Button(self.frame, text="Snake Menu", fg="red", command=self.write_explanation)
        self.header.place(x = 200,y = 10)

        self.below = tk.Button(self.frame, text="Select up to one option from each row below.", fg="Red", command=self.explanatory)
        self.below.place(x=120, y=30)

        self.numP = tk.Button(self.frame, text="Number of Players:", fg="Red", command=self.dont_click_me)
        self.numP.place(x = 30,y = 60)

        self.singleplayer = tk.Button(self.frame, text = "One Player", fg = "Green", command = lambda: self.setNumPlayers(1)) #'self.players(1)'
        self.singleplayer.place(x = 180, y = 60)

        self.twoplayer = tk.Button(self.frame, text = "Two Players", fg = "Green", command = lambda: self.setNumPlayers(2))
        self.twoplayer.place(x = 275, y = 60)

        self.numPlayers = 1
        
        self.movS = tk.Button(self.frame, text="Movement Speed:", fg="Red", command= self.dont_click_me)
        self.movS.place(x = 30,y = 100)
        """
        self.slow = tk.Button(self.frame, text="Slow", fg="Green", command=lambda: self.setMovementSpeed("slow"))
        self.slow.place(x = 180, y = 100)

        self.medium = tk.Button(self.frame, text="Medium", fg="Green", command=lambda: self.setMovementSpeed("medium"))
        self.medium.place(x = 240, y = 100)

        self.fast = tk.Button(self.frame, text="Fast", fg="Green", command=lambda: self.setMovementSpeed("fast"))
        self.fast.place(x = 320, y = 100)
        """
        self.movS = Scale(self.frame, from_=1, to=10, orient=HORIZONTAL)
        self.movS.place(x = 150, y = 82)
        self.movS.configure(length = 300)
        self.movS.set(5)
        self.movementSpeed = 5

        self.tailgrowth = tk.Button(self.frame, text="Tail Growth:", fg="Red", command=lambda: self.report("sets how much you grow with 1 unit of food"))
        self.tailgrowth.place(x = 30, y = 140)
        """
        self.growone = tk.Button(self.frame, text= "One", fg="Green", command=lambda: self.setGrowth(1))
        self.growone.place(x = 180, y = 140)

        self.growtwo = tk.Button(self.frame, text="Two", fg="Green", command=lambda: self.setGrowth(2))
        self.growtwo.place(x = 245, y = 140)

        self.growthree = tk.Button(self.frame, text="Three", fg="Green", command=lambda: self.setGrowth(3))
        self.growthree.place(x = 310, y = 140)
        """
        self.grow = Scale(self.frame, from_=1, to=10, orient=HORIZONTAL)
        self.grow.configure(length = 300)
        self.grow.place(x=150, y=122)
        self.growthAmount = 1

        self.arenaisze = tk.Button(self.frame, text="Arena Size: ", fg="Red", command=self.dont_click_me)
        self.arenaisze.place(x = 30, y = 180)

        self.smallarena = tk.Button(self.frame, text="Small", fg="Green", command= lambda: self.setArenaSize('small'))
        self.smallarena.place(x = 175, y = 180)

        self.mediumarena = tk.Button(self.frame, text="Medium", fg="Green", command=lambda: self.setArenaSize('medium'))
        self.mediumarena.place(x = 235, y = 180)

        self.largearena = tk.Button(self.frame, text="Large", fg="Green", command=lambda: self.setArenaSize('large'))
        self.largearena.place(x = 310, y = 180)

        self.gametypes = tk.Button(self.frame, text="Game Modes: Pick one from each row.", fg="Green", command=self.dont_click_me)
        self.gametypes.place(x = 120, y = 240)

        self.mode1 = tk.Button(self.frame, text="Game Style:", fg="Red", command=self.dont_click_me)
        self.mode1.place(x = 30, y = 280)

        self.modern = tk.Button(self.frame, text="Modern", fg="Green", command=lambda: self.setType("modern"))
        self.modern.place(x = 180, y = 280)

        self.arcademode = tk.Button(self.frame, text="Arcade", fg="Green", command=lambda: self.setType("arcade"))
        self.arcademode.place(x = 260, y = 280)

        self.agility = .25

        self.snakestyle = tk.Button(self.frame, text="Snake Style:", fg="Red", command=self.dont_click_me)
        self.snakestyle.place(x = 30, y = 320)

        self.crazy = tk.Button(self.frame, text="Crazy", fg="Green", command=lambda: self.setGameType("Crazy"))
        self.crazy.place(x = 170, y = 320)

        self.skele = tk.Button(self.frame, text="Skeleton", fg="Green", command=lambda: self.setGameType("Skeleton"))
        self.skele.place(x = 240, y = 320)

        self.regular = tk.Button(self.frame, text="Traditional", fg="Green", command=lambda: self.setGameType("Traditional"))
        self.regular.place(x = 330, y = 320)

        self.gameType = "Traditional"

        self.bulletsnakes = tk.Button(self.frame, text="Enable Bullets?", fg="Red", command=self.dont_click_me)
        self.bulletsnakes.place(x = 30, y = 360)

        self.bullets = False

        self.yesbullets = tk.Button(self.frame, text="Yes", fg="Green", command=lambda: self.Bullets(True))
        self.yesbullets.place(x = 180, y = 360)

        self.nobullets = tk.Button(self.frame, text="No", fg="Green", command=lambda: self.Bullets(False))
        self.nobullets.place(x= 240, y = 360)

        self.wrap_or_no = tk.Button(self.frame, text="No Boundaries?", fg="Red", command=self.wrap_explain)
        self.wrap_or_no.place(x= 30, y = 400)

        self.wrapping = "maybe"

        self.yeswrap = tk.Button(self.frame, text="Yes", fg="Green", command=lambda: self.setWrap(True))
        self.yeswrap.place(x = 180, y = 400)

        self.nowrap = tk.Button(self.frame, text="No", fg="Green", command=lambda: self.setWrap(False))
        self.nowrap.place(x= 240, y = 400)

        self.playthegame = tk.Button(self.frame, text = "Play with these settings", fg = "Red", command = self.play)
        self.playthegame.place(x = 150, y = 430)

        self.count = 0
        self.hidden_game_within_game = tk.Button(self.frame, text = "Don't click me!!!", fg = "Red", command = lambda: self.hidden_game(self.count))
        self.hidden_game_within_game.place(x = 480, y = 500)

        #add settings, arena size: small, medium, large, other styles

        self.use_mouse = True  #maybe use a mouse thing to determine snake movement
    def report(self,line=""):
        line += "\n\n\n"
        a = "  " + line
        if self.text == None:
            print(a)
        else:
            self.text.insert(END, a)
            self.text.see(END)
    def setNumPlayers(self, num):
        self.numPlayers = num
        self.report("set number of sneks to " + str(num))
        if num == 1:
            self.Choice = tk.Button(self.frame, text = "One Player", fg = "Green", command = lambda: self.report("ohmmmmmmmmmmmmm - I'm meditating")) #'self.players(1)'
            self.Choice.place(x = 485, y = 60)
            self.Choice.configure(width = 10)
        else:
            self.Choice = tk.Button(self.frame, text = "Two Player", fg = "Green", command = lambda: self.report("why are you clicking around?")) #'self.players(1)'
            self.Choice.place(x = 485, y = 60)
            self.Choice.configure(width = 10)

    def setGameType(self, gameType):
        self.gameType = gameType
        if self.gameType == "Traditional":
            self.Choice = tk.Button(self.frame, text = "Traditional", fg = "Green", command = lambda: self.report("stuff")) #'self.players(1)'
            self.Choice.place(x = 485, y = 320)
            self.Choice.configure(width = 10)
        elif self.gameType == "Skeleton":
            self.Choice = tk.Button(self.frame, text = "Skeleton", fg = "Green", command = lambda: self.dont_click_me) #'self.players(1)'
            self.Choice.place(x = 485, y = 320)
            self.Choice.configure(width = 10)
        else:
            self.Choice = tk.Button(self.frame, text = "Crazy", fg = "Green", command = lambda: self.dont_click_me) #'self.players(1)'
            self.Choice.place(x = 485, y = 320)
            self.Choice.configure(width = 10)
        self.report("game type has been set to " + gameType)

    def setMovementSpeed(self):
        self.movementSpeed = self.movS.get()
        if self.agility == .25:
            if self.movementSpeed > 5:
                self.agility = .5
            timeSleep = 4.0/self.movementSpeed
        else:
            timeSleep = 6.0/self.movementSpeed

        return timeSleep

    """def setMovementSpeed(self, movString):
        self.movementSpeed = movString
        self.report("set snek movement speed to " + movString)
        self.Choice2 = tk.Button(self.frame, text = movString, fg = "Green", command = lambda: self.report("your current selection for mOVeMenT Speed")) #'self.players(1)'
        self.Choice2.place(x = 485, y = 100)
        self.Choice2.configure(width = 10)"""

    def setGrowth(self):
        self.growthAmount = self.grow.get()
        #self.report("set Tail Growth to " + str(self.growthAmount))

    def setWrap(self, boole):
        if boole:
            self.wrapping = "wrapped"
            buttonText = "wraps"
            self.report("warpin- sorry, wrapping occurs (make sure to hit the edge \n  as hard as you possibly can)")
        else:
            self.wrapping = "doesn't matter"
            buttonText = "doesn't wrap"
            self.report("wrapping does not occure (or does it)")
        self.Choice = tk.Button(self.frame, text = buttonText, fg = "Green", command = lambda: self.report("click clack")) #'self.players(1)'
        self.Choice.place(x = 485, y = 400)
        self.Choice.configure(width = 10)

    def wrap_explain(self):
        self.explanation = tk.Button(self.frame, text="With No Boundaries on, snakes will wrap around screen.", fg="Green", command= self.explain_further_DUH_DUh_duhh)
        self.explanation.place(x= 20, y = 450)
    def explain_further_DUH_DUh_duhh(self):
        self.explanation2 = tk.Button(self.frame, text="or will they???!!!", fg="Green", command= self.explain_further_DUH_DUh_duhh_anotherduhhhh)
        self.explanation2.place(x= 20, y = 470)
    def explain_further_DUH_DUh_duhh_anotherduhhhh(self):
        self.explanation3 = tk.Button(self.frame, text="they will", fg="Green", command= self.why_would_you_click_this_inconspicous_button)
        self.explanation3.place(x= 20, y = 490)
    def Bullets(self, boole):
        self.bullets = boole
        if boole:
            n = "on"
        else:
            n = "off"
        self.report("bullets are " + n)
        self.Choice5 = tk.Button(self.frame, text = "bullets are " + n, fg = "Green", command = lambda: self.dont_click_me)
        self.Choice5.place(x= 485, y = 360)
        self.Choice5.configure(width = 10)

    def why_would_you_click_this_inconspicous_button(self):
        if self.trollCount == 0:
            self.report("now why would you click this inconspicous button?")
        elif self.trollCount < 2:
            self.report("I(the button) seriously have no wisdom to offer")
            print(self.trollCount)
        else:
            self.dont_click_me()
        self.trollCount += 1
    def setArenaSize(self, the_size): 
        if the_size == 'small':
            self.x_size = 90
            self.y_size = 54
        elif the_size == 'medium':
            self.x_size = 150
            self.y_size = 90
        else:
            self.x_size = 250
            self.y_size = 150
        self.report("set arena size to " + the_size)
        self.Choice5 = tk.Button(self.frame, text = the_size, fg = "Green", command = lambda: self.report("Do not click me")) #'self.players(1)'
        self.Choice5.place(x = 485, y = 180)
        self.Choice5.configure(width = 10)
    def hidden_game(self, count):
        if count == 0:
            self.report("congratulations!!! You have discovered the extremely well concealed game within a\n  game worth about 8 points! Click this button again to play the game DodgeBall\n  (more like DodgeSquare actually lol)")
            self.count += 1
        else:
            self.play2()
    def setType(self, theType):
        if theType == "arcade":
            self.agility = 1
        else:
            self.agility = .25
        self.Choice5 = tk.Button(self.frame, text = theType, fg = "Green", command = lambda: self.report("Do not click me")) #'self.players(1)'
        self.Choice5.place(x = 485, y = 280)
        self.Choice5.configure(width = 10)
        self.report("game type has been set to " + theType)

    def explanatory(self):
        self.report("this is self explanatory")
    def explain_currentChoice(self):
        self.report("this section shows your current choice")
    def write_explanation(self):
        self.explanation4 = tk.Button(self.frame, text="<--This is the snake menu", fg="red", command=self.dont_click_me)
        self.explanation4.place(x = 285, y = 10)
    def dont_click_me(self):
        self.report("don't click me")
    def play(self):
        self.setGrowth()
        a = self.setMovementSpeed()
        game = Two_Player_Snake.PlaySnake(self.numPlayers, self.growthAmount, self.x_size, self.y_size, 1000,600, self.wrapping, self.agility, self.bullets, self.gameType)
        while not game.GAME_OVER:
            time.sleep(a/60.0)  # 1.0 is placeholder for variable that changes snake from arcade to modern
            game.update()
        game.removeThis()
    def play2(self):
        game = Two_Player_Snake.PlayDodgeBall(200, 120, 1000, 600)
        while not game.GAME_OVER:
            time.sleep(1.0/60.0)  # 1.0 is placeholder for variable that changes snake from arcade to modern
            game.update() 
        game.removeThis()     

a = SnakeMenuRunner()
