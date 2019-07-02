from tkinter import Tk, Label, Entry, Button, PhotoImage, messagebox, END, Canvas
from threading import Timer
from time import sleep
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

        # call the next phase of initialization: loading resources
        self.__initResource()


    def __initResource(self):
        ## read the sprite files
        # all sprites will saved in this dictionary
        self.wSprites = {
            'wall': PhotoImage(file="resource/sprite_wall.png"),
            'cage': PhotoImage(file="resource/sprite_cage.png"),
            'pellet': PhotoImage(file="resource/sprite_pellet.png")
        }

        # bind sprites for moving objects
        for i in range(4):
            # pacman: pacman(direction)(index)
            if i == 3:
                pass
            else:
                self.wSprites['pacmanL{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_left{}.png".format(i+1))
                self.wSprites['pacmanR{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_right{}.png".format(i+1))
                self.wSprites['pacmanU{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_up{}.png".format(i+1))
                self.wSprites['pacmanD{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_down{}.png".format(i+1))
            # ghosts: ghost(index1)(direction)(index2)
            self.wSprites['ghost{}L1'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_left1.png".format(i+1))
            self.wSprites['ghost{}L2'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_left2.png".format(i+1))
            self.wSprites['ghost{}R1'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_right1.png".format(i+1))
            self.wSprites['ghost{}R2'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_right2.png".format(i+1))
            self.wSprites['ghost{}U1'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_up1.png".format(i+1))
            self.wSprites['ghost{}U2'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_up2.png".format(i+1))
            self.wSprites['ghost{}D1'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_down1.png".format(i+1))
            self.wSprites['ghost{}D2'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_down2.png".format(i+1))


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
        self.root.protocol("WM_DELETE_WINDOW", self.inputResponseExit)

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
            # removing level selection features
            self.wLvLabel.destroy()
            self.wLvEntry.destroy()
            self.wLvBtn.destroy()
            # place the canvas and set isPlaying True
            self.wGameCanv.place(x=0, y=30)
            self.isPlaying = True
            self.wGameLabelScore.place(x=10, y=5)


        # check the name of the object and bind the sprite, adjust their coordinate
        for j in range(32):
            for i in range(28):

                if field.gameEngine.levelObjects[i][j].name == "empty":
                    pass
                elif field.gameEngine.levelObjects[i][j].name == "wall":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'])
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 30+j*17+8)
                elif field.gameEngine.levelObjects[i][j].name == "cage":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['cage'])
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 30+j*17+8)
                elif field.gameEngine.levelObjects[i][j].name == "pellet":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['pellet'])
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 30+j*17+8)

        # bind the sprite and give it current coord. for pacman
        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL1'])
        self.wGameCanv.move(self.wGameCanvMovingObjects[0],
                            field.gameEngine.movingObjectPacman.coordinateRel[0]*17+8,
                            30+field.gameEngine.movingObjectPacman.coordinateRel[1]*17+8)
        
        # bind the sprite give them current coord. for ghosts
        for i in range(4):
            if field.gameEngine.movingObjectGhosts[i].isActive == True:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[i+1], image=self.wSprites['ghost{}L1'.format(i+1)])
                self.wGameCanv.move(self.wGameCanvMovingObjects[i+1],
                                    field.gameEngine.movingObjectGhosts[i].coordinateRel[0]*17+8,
                                    30+field.gameEngine.movingObjectGhosts[i].coordinateRel[1]*17+8)

        self.loopTimer = PerpetualTimer(0.06, self.loopFunction)
        self.loopTimer.start()
            


    def inputResponseLeft(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Left"
        #field.gameEngine.movingObjectGhosts[0].dirNext = "Left"
        #field.gameEngine.movingObjectGhosts[1].dirNext = "Left"
        #field.gameEngine.movingObjectGhosts[2].dirNext = "Left"
        #field.gameEngine.movingObjectGhosts[3].dirNext = "Left"

    def inputResponseRight(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Right"
        #field.gameEngine.movingObjectGhosts[0].dirNext = "Right"
        #field.gameEngine.movingObjectGhosts[1].dirNext = "Right"
        #field.gameEngine.movingObjectGhosts[2].dirNext = "Right"
        #field.gameEngine.movingObjectGhosts[3].dirNext = "Right"

    def inputResponseUp(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Up"
        #field.gameEngine.movingObjectGhosts[0].dirNext = "Up"
        #field.gameEngine.movingObjectGhosts[1].dirNext = "Up"
        #field.gameEngine.movingObjectGhosts[2].dirNext = "Up"
        #field.gameEngine.movingObjectGhosts[3].dirNext = "Up"
    
    def inputResponseDown(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Down"
        #field.gameEngine.movingObjectGhosts[0].dirNext = "Down"
        #field.gameEngine.movingObjectGhosts[1].dirNext = "Down"
        #field.gameEngine.movingObjectGhosts[2].dirNext = "Down"
        #field.gameEngine.movingObjectGhosts[3].dirNext = "Down"


    def inputResponseEsc(self, event):
        self.loopTimer.stop() 
        messagebox.showinfo("Game Over!", "You hit the escape key!")

    def inputResponseExit(self):
        self.loopTimer.stop()


    def loopFunction(self):

        field.gameEngine.loopFunction()

        coordGhosts = {}

        for i in range(4):
            coordGhosts['RelG{}'.format(i+1)] = field.gameEngine.movingObjectGhosts[i].coordinateRel    # ghosts relative coordinate
            coordGhosts['AbsG{}'.format(i+1)] = field.gameEngine.movingObjectGhosts[i].coordinateAbs    # ghosts absolute coordinate

        self.spritePacman(field.gameEngine.movingObjectPacman.coordinateRel, field.gameEngine.movingObjectPacman.coordinateAbs)
        self.spriteGhost(coordGhosts)
        self.encounterEvent(field.gameEngine.movingObjectPacman.coordinateRel, field.gameEngine.movingObjectPacman.coordinateAbs)




    def spritePacman(self, coordRelP, coordAbsP):
        ## pacman sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        if field.gameEngine.movingObjectPacman.dirCurrent == "Left":

            # check the object passed field edges
            if field.gameEngine.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 17*27+17, 0)    # notice this will move the sprite 17*27+17 (not 17*27+12) as the sprite will move once again below
                field.gameEngine.movingObjectPacman.dirEdgePassed = False
            else:
                pass

            if coordAbsP[0] % 4 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
            elif coordAbsP[0] % 4 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL3'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
            elif coordAbsP[0] % 4 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
            elif coordAbsP[0] % 4 == 3:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL1'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -5, 0)


        elif field.gameEngine.movingObjectPacman.dirCurrent == "Right":

            # check the object passed field edges
            if field.gameEngine.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -(17*27+17), 0)
                field.gameEngine.movingObjectPacman.dirEdgePassed = False
            else:
                pass

            if coordAbsP[0] % 4 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
            elif coordAbsP[0] % 4 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
            elif coordAbsP[0] % 4 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
            elif coordAbsP[0] % 4 == 3:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR1'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 5, 0)


        elif field.gameEngine.movingObjectPacman.dirCurrent == "Up":

            # check the object passed field edges
            if field.gameEngine.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 17*27+17)
                field.gameEngine.movingObjectPacman.dirEdgePassed = False
            else:
                pass

            if coordAbsP[1] % 4 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
            elif coordAbsP[1] % 4 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU3'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
            elif coordAbsP[1] % 4 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
            elif coordAbsP[1] % 4 == 3:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU1'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -5)


        elif field.gameEngine.movingObjectPacman.dirCurrent == "Down":

            # check the object passed field edges
            if field.gameEngine.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -(17*27+17))
                field.gameEngine.movingObjectPacman.dirEdgePassed = False
            else:
                pass

            if coordAbsP[1] % 4 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
            elif coordAbsP[1] % 4 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD3'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
            elif coordAbsP[1] % 4 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
            elif coordAbsP[1] % 4 == 3:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD1'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 5)


    def encounterEvent(self, coordRelP, coordAbsP):
        ## encounter features

        encounterMov = field.gameEngine.encounterMoving(coordAbsP[0], coordAbsP[1]) # call encounterEvent for moving objects

        if encounterMov == 'dead':
            self.loopTimer.stop() 
            messagebox.showinfo("Game Over!", "You encountered a ghost!")

        else:
            pass

        # check the object reaches grid coordinate
        if coordAbsP[0] % 4 == 0 and coordAbsP[1] % 4 == 0:
            encounterFix = field.gameEngine.encounterFixed(coordRelP[0], coordRelP[1]) # call encounterEvent function

            if encounterFix == "empty":
                pass
            elif encounterFix == "pellet":
                if field.gameEngine.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed == False:  # check the pellet is alive
                    field.gameEngine.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed = True # destroy the pellet
                    self.wGameCanv.delete(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]]) # remove from the canvas
                    self.statusScore += 10 # adjust the score
                    self.wGameLabelScore.configure(text=("Score: " + str(self.statusScore))) # showing on the board
                else:   # the pellet is already taken
                    pass

        else: # pacman is not on grid coordinate
            pass

        


    def spriteGhost(self, coordGhosts):
        ## ghosts sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        for ghostNo in range(4):
            if field.gameEngine.movingObjectGhosts[ghostNo].isActive == True:   # only active ghost will be shown
                if field.gameEngine.movingObjectGhosts[ghostNo].dirCurrent == "Left":

                    # check the object passed field edges
                    if field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 17*27+17, 0)
                        field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed = False
                    else:
                        pass

                    if coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 0:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}L1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 1:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}L2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 2:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}L1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 3:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}L2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -5, 0)


                elif field.gameEngine.movingObjectGhosts[ghostNo].dirCurrent == "Right":

                    # check the object passed field edges
                    if field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -(17*27+17), 0)
                        field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed = False
                    else:
                        pass

                    if coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 0:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}R1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 1:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}R2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 2:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}R1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 3:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}R2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 5, 0)


                elif field.gameEngine.movingObjectGhosts[ghostNo].dirCurrent == "Up":

                    # check the object passed field edges
                    if field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 17*27+17)
                        field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed = False
                    else:
                        pass

                    if coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 0:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}U1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 1:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}U2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 2:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}U1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 3:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}U2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -5)


                elif field.gameEngine.movingObjectGhosts[ghostNo].dirCurrent == "Down":

                    # check the object passed field edges
                    if field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -(17*27+17))
                        field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed = False
                    else:
                        pass

                    if coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 0:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}D1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 1:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}D2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 2:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}D1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 3:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}D2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 5)
            
            else:   # inactive ghost
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