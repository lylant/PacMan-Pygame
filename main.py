from tkinter import Tk, Label, Entry, Button, PhotoImage, messagebox, END
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
        self.statusCoordinateRel = [0, 0]   # Relative Coordinate, check can the player move given direction
        self.statusCoordinateAbs = [0, 0]   # Absolute Coordinate, use for widget(image) and ghost encounters

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
        self.wGameLabelLineTop = Label(self.root, text="- " * 48)
        self.wGameLabelLineBot = Label(self.root, text="- " * 48)
        self.wGameLabelObjects = [[Label(self.root, image=None) for j in range(32)] for i in range(28)]


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
            self.isPlaying = True

        ## bind the sprite on widgets with generated map
        # read the sprites from resource folder
        self.imgWall = PhotoImage(file="resource/sprite_wall.png")
        self.imgCage = PhotoImage(file="resource/sprite_wall.png")
        self.imgPellet = PhotoImage(file="resource/sprite_pellet.png")
        self.imgGhost = PhotoImage(file="resource/sprite_ghost_temp.png")
        self.imgPacman = PhotoImage(file="resource/sprite_pacman_left1.png")

        # check the name of the object and bind the sprite
        for j in range(32):
            for i in range(28):

                if field.gameEngine.levelObjects[i][j].name == "empty":
                    pass
                elif field.gameEngine.levelObjects[i][j].name == "wall":
                    self.wGameLabelObjects[i][j] = Label(self.root, image=self.wSpriteWall)
                elif field.gameEngine.levelObjects[i][j].name == "cage":
                    self.wGameLabelObjects[i][j] = Label(self.root, image=self.wSpriteCage)
                elif field.gameEngine.levelObjects[i][j].name == "pellet":
                    self.wGameLabelObjects[i][j] = Label(self.root, image=self.wSpritePellet)
                elif field.gameEngine.levelObjects[i][j].name == "ghost":
                    self.wGameLabelObjects[i][j] = Label(self.root, image=self.wSpriteGhost)
                elif field.gameEngine.levelObjects[i][j].name == "pacman":
                    self.wGameLabelObjects[i][j] = Label(self.root, image=self.wSpritePacmanL1)
                    # pass the current Pac-Man's coordinate
                    self.statusCoordinateRel[0] = i
                    self.statusCoordinateRel[1] = j
                    self.statusCoordinateAbs[0] = 3*i
                    self.statusCoordinateAbs[1] = 3*j
            
                self.wGameLabelObjects[i][j].place(x=i*17, y=40+j*17)



    def inputResponseLeft(self, event):
        pass

    def inputResponseRight(self, event):
        pass

    def inputResponseUp(self, event):
        pass
    
    def inputResponseDown(self, event):
        pass

    def inputResponseEsc(self, event):
        pass



mainEngine = MainEngine()



# treading Timer
    # 주인공은 지정된 방향으로 좌표 이동, moveRequest를 해당 방향으로
    # 만약 주인공 좌표가 (x,y)이고 방향이 right라면 (x,y+1)에 해당하는 오브젝트의 moveRequest를 불러온다
    # moveRequest의 return을 받아보고 갈 수 있는지 여부를 판단하고 실제 이동에 해당하는 function을 불러온다
    # 실제 이동에 해당하는 function은 좌표계를 3개로 쪼개서 이동하면서 스프라이트를 바꿔준다

    # if문을 이용하여 wall, pellet은 pass하고 팩맨, 고스트 등 움직이는 오브젝트만 place로 좌표를 재지정한다


    # 귀신들은 ai 만들기 힘드니까 지정된 구역 순찰해놓고 v1.1.0에서 알고리즘 develop해서 릴리즈
    # 한칸씩 움직임