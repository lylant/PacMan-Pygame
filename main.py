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
        self.wSpriteEmpty = PhotoImage(file="resource/sprite_dummy.png")
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
        self.wGameCanv = Canvas(width=480, height=640)
        self.wGameCanvObjects = [[self.wGameCanv.create_image(0,0,image=None) for j in range(32)] for i in range(28)]
        self.wGameCanvMovingObjects = [self.wGameCanv.create_image(0,0,image=None) for n in range(5)] # 0: pacman, 1-4: ghosts
        #self.fuk=self.wGameCanv.create_image(30,30,image=self.wSpriteGhost)

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




    def __initLevel(self, level):

        field.gameEngine.levelGenerate(level)   # generate selected/passed level

        if self.isPlaying == False:
            self.wLvLabel.destroy()
            self.wLvEntry.destroy()
            self.wLvBtn.destroy()
            self.wGameCanv.pack()
            self.isPlaying = True



        # check the name of the object and bind the sprite
        for j in range(32):
            for i in range(28):

                if field.gameEngine.levelObjects[i][j].name == "empty":
                    pass
                elif field.gameEngine.levelObjects[i][j].name == "wall":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSpriteWall)
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 40+j*17+8)
                elif field.gameEngine.levelObjects[i][j].name == "cage":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSpriteCage)
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 40+j*17+8)
                elif field.gameEngine.levelObjects[i][j].name == "pellet":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSpritePellet)
                    self.wGameCanv.move(self.wGameCanvObjects[i][j], i*17+8, 40+j*17+8)

        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanL1)
        self.wGameCanv.move(self.wGameCanvMovingObjects[0],
                            field.gameEngine.movingObjectPacman.coordinateRel[0]*17+8,
                            40+field.gameEngine.movingObjectPacman.coordinateRel[1]*17+8)


    def inputResponseLeft(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Left"

    def inputResponseRight(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Right"

    def inputResponseUp(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Up"
    
    def inputResponseDown(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Down"

    def inputResponseEsc(self, event):
        field.gameEngine.loopFunction()
        self.loopFunction()

    def loopFunction(self):

        #coordRelP = field.gameEngine.movingObjectPacman.coordinateRel   # pacman relative coordinate
        coordAbsP = field.gameEngine.movingObjectPacman.coordinateAbs   # pacman absolute coordinate



        ## pacman sprite feature
        if field.gameEngine.movingObjectPacman.dirCurrent == "Left":
            if coordAbsP[0] % 3 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanL1)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -6, 0)
            elif coordAbsP[0] % 3 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanL2)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -6, 0)
            elif coordAbsP[0] % 3 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanL3)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -5, 0)

        elif field.gameEngine.movingObjectPacman.dirCurrent == "Right":
            if coordAbsP[0] % 3 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanR1)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 6, 0)
            elif coordAbsP[0] % 3 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanR2)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 6, 0)
            elif coordAbsP[0] % 3 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanR3)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 5, 0)

        elif field.gameEngine.movingObjectPacman.dirCurrent == "Up":
            if coordAbsP[1] % 3 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanU1)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -6)
            elif coordAbsP[1] % 3 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanU2)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -6)
            elif coordAbsP[1] % 3 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanU3)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -5)

        elif field.gameEngine.movingObjectPacman.dirCurrent == "Down":
            if coordAbsP[1] % 3 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanD1)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 6)
            elif coordAbsP[1] % 3 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanD2)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 6)
            elif coordAbsP[1] % 3 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSpritePacmanD3)
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 5)




mainEngine = MainEngine()



# treading Timer
    # 주인공은 지정된 방향으로 좌표 이동, moveRequest를 해당 방향으로
    # 만약 주인공 좌표가 (x,y)이고 방향이 right라면 (x,y+1)에 해당하는 오브젝트의 moveRequest를 불러온다
    # moveRequest의 return을 받아보고 갈 수 있는지 여부를 판단하고 실제 이동에 해당하는 function을 불러온다
    # 실제 이동에 해당하는 function은 좌표계를 3개로 쪼개서 이동하면서 스프라이트를 바꿔준다

    # if문을 이용하여 wall, pellet은 pass하고 팩맨, 고스트 등 움직이는 오브젝트만 place로 좌표를 재지정한다


    # 귀신들은 ai 만들기 힘드니까 지정된 구역 순찰해놓고 v1.1.0에서 알고리즘 develop해서 릴리즈
    # 한칸씩 움직임