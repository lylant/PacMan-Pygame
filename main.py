from tkinter import Tk, Label, Entry, Button, PhotoImage, messagebox, END, Canvas
from threading import Timer
from data import field
import os


class MainEngine(object):

    def __init__(self):
        
        # initialize tkinter window parameters
        self.root = Tk()
        self.root.title("Pac-Man")
        self.root.geometry("480x640")
        self.root.resizable(0, 0)

        # initialize some engine variables
        self.currentLv = 1   # default: level 1
        self.isPlaying = False
        self.statusScore = 0
        self.statusLife = 2

        # call the next phase of initialization: read the sprites
        self.__initSprites()


    def __initSprites(self):
        # read the sprite files, this can be reduced with loops, maybe?
        self.wSpriteWall = PhotoImage(file="resource/sprite_wall.png")
        self.wSpriteCage = PhotoImage(file="resource/sprite_wall.png")
        self.wSpritePellet = PhotoImage(file="resource/sprite_pellet.png")
        self.wSpriteGhost = PhotoImage(file="resource/sprite_ghost_temp.png")
        self.wSpritePacmanL1 = PhotoImage(file="resource/sprite_pacman_left1.png")
        self.wSpritePacmanL2 = PhotoImage(file="resource/sprite_pacman_left2.png")
        self.wSpritePacmanL3 = PhotoImage(file="resource/sprite_pacman_left3.png")
        self.wSpritePacmanR1 = PhotoImage(file="resource/sprite_pacman_right1.png")
        self.wSpritePacmanR2 = PhotoImage(file="resource/sprite_pacman_right2.png")
        self.wSpritePacmanR3 = PhotoImage(file="resource/sprite_pacman_right3.png")
        self.wSpritePacmanU1 = PhotoImage(file="resource/sprite_pacman_up1.png")
        self.wSpritePacmanU2 = PhotoImage(file="resource/sprite_pacman_up2.png")
        self.wSpritePacmanU3 = PhotoImage(file="resource/sprite_pacman_up3.png")
        self.wSpritePacmanD1 = PhotoImage(file="resource/sprite_pacman_down1.png")
        self.wSpritePacmanD2 = PhotoImage(file="resource/sprite_pacman_down2.png")
        self.wSpritePacmanD3 = PhotoImage(file="resource/sprite_pacman_down3.png")

        # call the next phase of initialization: generate widgets
        self.__initWidgets()


    def __initWidgets(self):
        # initialize widgets for level selection
        self.wLvLabel = Label(self.root, text="Select the level.")
        self.wLvEntry = Entry(self.root)
        self.wLvBtn = Button(self.root, text="Select", command=self.lvSelect, width=5, height=1)

        # initialize widgets for the game
        self.wGameLabelScore = Label(self.root, text=("Score: " + str(self.statusScore)))
        self.wGameLabelLife = Label(self.root, text=("Life: " + str(self.statusLife)))
        self.wGameCanv = Canvas(width=480, height=600)
        self.wGameCanvObjects = [[self.wGameCanv.create_image(0,0,image=None) for j in range(32)] for i in range(28)]
        self.wGameCanv.config(background="black")
        self.wGameCanvMovingObjects = [self.wGameCanv.create_image(0,0,image=None) for n in range(5)] # 0: pacman, 1-4: ghosts

        # key binds for the game control
        self.root.bind('<Left>', self.inputResponseLeft)
        self.root.bind('<Right>', self.inputResponseRight)
        self.root.bind('<Up>', self.inputResponseUp)
        self.root.bind('<Down>', self.inputResponseDown)
        self.root.bind('<Escape>', self.inputResponseEsc)

        # call the next phase of initialization: level selection
        self.__initLevelSelect()


    def __initLevelSelect(self):
        ## level selection, showing all relevant widgets
        self.wLvLabel.pack()
        self.wLvEntry.pack()
        self.wLvBtn.pack()

        # execute the game
        self.root.mainloop()



    def lvSelect(self):
        try:
            self.__initLevel(self.wLvEntry.get())
        
        except FileNotFoundError:
            self.wLvEntry.delete(0, END)  # clear the text box
            messagebox.showinfo("Error!", "Enter a valid level.")




## 죽고나면 initLevel 기능과 같은 것을 다시 불러오되, isDestroyed를 체크해서 스프라이트를 불러올지 판단한다


    def __initLevel(self, level):

        field.gameEngine.levelGenerate(level)   # generate selected/passed level

        if self.isPlaying == False:
            self.wLvLabel.destroy()
            self.wLvEntry.destroy()
            self.wLvBtn.destroy()
            self.wGameCanv.place(x=0, y=30)
            self.isPlaying = True

            self.wGameLabelScore.place(x=10, y=5)

            self.loopTimer = PerpetualTimer(0.08, self.loopFunction)
            self.loopTimer.start()


        # check the name of the object and bind the sprite, adjust their coordinate
        for j in range(32):
            for i in range(28):

                if field.gameEngine.levelObjects[i][j].name == "empty":
                    pass
                elif field.gameEngine.levelObjects[i][j].name == "wall":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSpriteWall)
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 30+j*17+8)
                elif field.gameEngine.levelObjects[i][j].name == "cage":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSpriteCage)
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 30+j*17+8)
                elif field.gameEngine.levelObjects[i][j].name == "pellet":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSpritePellet)
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 30+j*17+8)

        # bind the sprite for pacman
        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanL1)
        self.wGameCanv.move(self.wGameCanvMovingObjects[0],
                            field.gameEngine.movingObjectPacman.coordinateRel[0]*17+8,
                            30+field.gameEngine.movingObjectPacman.coordinateRel[1]*17+8)


    def inputResponseLeft(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Left"

    def inputResponseRight(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Right"

    def inputResponseUp(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Up"
    
    def inputResponseDown(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Down"

    def inputResponseEsc(self, event):
        self.loopTimer.stop() 
        messagebox.showinfo("Game Over!", "You hit the escape key!")


    def loopFunction(self):

        field.gameEngine.loopFunction()

        coordRelP = field.gameEngine.movingObjectPacman.coordinateRel   # pacman relative coordinate
        coordAbsP = field.gameEngine.movingObjectPacman.coordinateAbs   # pacman absolute coordinate


        ## pacman sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        if field.gameEngine.movingObjectPacman.dirCurrent == "Left":
            if coordAbsP[0] % 3 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanL2)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -6, 0)
            elif coordAbsP[0] % 3 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanL3)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -6, 0)
            elif coordAbsP[0] % 3 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanL1)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -5, 0)

        elif field.gameEngine.movingObjectPacman.dirCurrent == "Right":
            if coordAbsP[0] % 3 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanR2)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 6, 0)
            elif coordAbsP[0] % 3 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanR3)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 6, 0)
            elif coordAbsP[0] % 3 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanR1)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 5, 0)

        elif field.gameEngine.movingObjectPacman.dirCurrent == "Up":
            if coordAbsP[1] % 3 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanU2)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -6)
            elif coordAbsP[1] % 3 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanU3)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -6)
            elif coordAbsP[1] % 3 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanU1)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -5)

        elif field.gameEngine.movingObjectPacman.dirCurrent == "Down":
            if coordAbsP[1] % 3 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanD2)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 6)
            elif coordAbsP[1] % 3 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanD3)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 6)
            elif coordAbsP[1] % 3 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanD1)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 5)

        ## encounter features
        if coordAbsP[0] % 3 == 0 and coordAbsP[1] % 3 == 0:
            encounter = field.gameEngine.encounterEvent(coordRelP[0], coordRelP[1])

            if encounter == "empty":
                pass
            elif encounter == "pellet":                
                if field.gameEngine.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed == False:
                    field.gameEngine.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed = True
                    self.wGameCanv.delete(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]])
                    self.statusScore += 10
                    self.wGameLabelScore.configure(text=("Score: " + str(self.statusScore)))
                else:
                    pass

        else:
            pass



class PerpetualTimer(object):
    
    def __init__(self, interval, function, *args):
        self.thread = None
        self.interval = interval
        self.function = function
        self.args = args
        self.isRunning = False

    
    def _handleFunction(self):
        self.isRunning = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.isRunning:
            self.thread = Timer(self.interval, self._handleFunction)
            self.thread.start()
            self.isRunning = True

    def stop(self):
            self.thread.cancel()
            self.isRunning = False


mainEngine = MainEngine()