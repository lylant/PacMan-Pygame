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
        self.currentLv = 1              # default: level 1
        self.isLevelGenerated = False   # check the level (map) is generated or not
        self.isPlaying = False          # check the game is actually started (moving) or not
        self.statusStartingTimer = 0    # countdown timer for 'get ready' feature
        self.statusDeadTimer = 0        # countdown timer for dead event
        self.statusScore = 0            # score
        self.statusLife = 2             # life

        # call the next phase of initialization: loading resources
        self.__initResource()


    def __initResource(self):
        ## read the sprite files
        # all sprites will saved in this dictionary
        self.wSprites = {
            'getready': PhotoImage(file="resource/sprite_get_ready.png"),
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

        for i in range(11):
            self.wSprites['pacmanDeath{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_death{}.png".format(i+1))

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
        self.wGameCanvLabelGetReady = self.wGameCanv.create_image(240,328,image=None)
        self.wGameCanvObjects = [[self.wGameCanv.create_image(0,0,image=None) for j in range(32)] for i in range(28)]
        self.wGameCanv.config(background="black")
        self.wGameCanvMovingObjects = [self.wGameCanv.create_image(0,0,image=None) for n in range(5)] # 0: pacman, 1-4: ghosts

        # key binds for the game control
        self.root.bind('<Left>', self.inputResponseLeft)
        self.root.bind('<Right>', self.inputResponseRight)
        self.root.bind('<Up>', self.inputResponseUp)
        self.root.bind('<Down>', self.inputResponseDown)
        self.root.bind('<Escape>', self.inputResponseEsc)
        self.root.bind('<Return>', self.inputResponseReturn)
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
            self.__initLevelOnce(self.wLvEntry.get())
        
        except FileNotFoundError:
            self.wLvEntry.delete(0, END)  # clear the text box
            messagebox.showinfo("Error!", "Enter a valid level.")




## 죽고나면 initLevel 기능과 같은 것을 다시 불러오되, isDestroyed를 체크해서 스프라이트를 불러올지 판단한다


    def __initLevelOnce(self, level):
        ## this function will be called only once

        # removing level selection features
        self.wLvLabel.destroy()
        self.wLvEntry.destroy()
        self.wLvBtn.destroy()
        # place the canvas and set isPlaying True
        self.wGameCanv.place(x=0, y=30)
        self.wGameLabelScore.place(x=10, y=5)
        self.wGameLabelLife.place(x=420, y=5)

        self.__initLevel(level)


    def __initLevel(self, level):

        self.currentLv = level

        if self.isLevelGenerated == False:
            field.gameEngine.levelGenerate(level)   # generate selected/passed level
        else:
            pass

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
        
        # advance to next phase: get ready!
        self.isLevelGenerated = True
        self.readyTimer = PerpetualTimer(0.70, self.__initLevelStarting)
        self.readyTimer.start()
            


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

    def inputResponseReturn(self, event):
        # skip feature
        if self.isLevelGenerated == True and self.isPlaying == False:
            self.gameStartingTrigger()
        else:
            pass

    def inputResponseExit(self):
        self.loopTimer.stop()




    def __initLevelStarting(self):
        self.statusStartingTimer += 1   # countdown timer for this function

        # bind the sprite for the widget
        self.wGameCanv.itemconfig(self.wGameCanvLabelGetReady, image=self.wSprites['getready'])

        if self.statusStartingTimer < 8:
            # blinking function
            if self.statusStartingTimer % 2 == 1:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='normal')
            else:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='hidden')

        else:   # after 8 loop, the main game will be started with loopFunction
            self.gameStartingTrigger()
        

    def gameStartingTrigger(self):
        ## stop to print out 'get ready' and start the game
        self.readyTimer.stop()
        self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='hidden')
        self.statusStartingTimer = 0
        self.isPlaying = True

        self.loopTimer = PerpetualTimer(0.06, self.loopFunction)
        self.loopTimer.start()


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
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR3'])
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


    def encounterEvent(self, coordRelP, coordAbsP):
        ## encounter features

        encounterMov = field.gameEngine.encounterMoving(coordAbsP[0], coordAbsP[1]) # call encounterEvent for moving objects

        if encounterMov == 'dead':
            self.encounterEventDead()

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

        
    def encounterEventDead(self):

        self.statusLife -= 1    # subtract remaining life
        self.wGameLabelLife.configure(text=("Life: " + str(self.statusLife))) # showing on the board

        # pause the game
        self.isPlaying = False
        self.loopTimer.stop()

        for i in range(4):  # hide the ghost sprite
            self.wGameCanv.itemconfigure(self.wGameCanvMovingObjects[i+1], state='hidden')

        # call the death sprite loop
        self.deathTimer = PerpetualTimer(0.12, self.encounterEventDeadLoop)
        self.deathTimer.start()


    def encounterEventDeadLoop(self):

        self.statusDeadTimer += 1   # countdown timer for this function

        if self.statusDeadTimer <= 11:
            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0],
                                        image=self.wSprites['pacmanDeath{}'.format(self.statusDeadTimer)])  # animate the death sprite
        else:
            self.encounterEventDeadRestart()

    
    def encounterEventDeadRestart(self):
        ## stop the death event and restart the game
        self.deathTimer.stop()




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