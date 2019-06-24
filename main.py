from tkinter import Tk, Label, Entry, Button
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
        self.root.configure(background="black")

        # initialize some engine variables
        self.currentLv = 1   # default: level 1
        self.isPlaying = False
        self.statusScore = 0
        self.statusLife = 2

        # call the next phase of initialization: generate widgets
        self.__initWidgets()

    def __initWidgets(self):
        ## initialize widgets for level selection
        self.wLvLabel = Label(self.root, text="Select the level.")
        self.wLvEntry = Entry(self.root)
        self.wLvBtn = Button(self.root, text="Select", command=self.lvSelect, width=5, height=1)

        ## initialize widgets for the game
        self.wGameLabelScore = Label(self.root, text=("Score: " + str(self.statusScore)))
        self.wGameLabelLife = Label(self.root, text=("Life: " + str(self.statusLife)))
        self.wGameLabelLineTop = Label(self.root, text="- " * 48)
        self.wGameLabelLineBot = Label(self.root, text="- " * 48)
        self.wGameLabelObjects = [[Label(self.root, image=None) for j in range(32)] for i in range(28)]



        ## key binds for the game control
        self.root.bind('<Left>', self.inputResponseLeft)
        self.root.bind('<Right>', self.inputResponseRight)
        self.root.bind('<Up>', self.inputResponseUp)
        self.root.bind('<Down>', self.inputResponseDown)
        self.root.bind('<Escape>', self.inputResponseEsc)

        self.root.mainloop()

    def lvSelect(self):
        pass

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



main = MainEngine()

# initialize map
    # field에서 generate된 맵을 받아와서 widget을 배치한다
    # 각 오브젝트의 개수를 받는다?


# treading Timer
    # 주인공은 지정된 방향으로 좌표 이동, moveRequest를 해당 방향으로
    # 만약 주인공 좌표가 (x,y)이고 방향이 right라면 (x,y+1)에 해당하는 오브젝트의 moveRequest를 불러온다
    # moveRequest의 return을 받아보고 갈 수 있는지 여부를 판단, 좌표 이동을 시켜준다

    # 주인공을 이미지파일로 만들어서 쓰겠다면
    # 입을 벌린것과 다문 것 두개를 번갈아 나타나게끔 한다

    # 귀신들은 ai 만들기 힘드니까 지정된 구역 순찰해놓고 v1.1.0에서 알고리즘 develop해서 릴리즈
    # 한칸씩 움직임