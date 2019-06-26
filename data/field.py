import os


class GameEngine(object):

    def __init__(self):

        self.levelObjects = [[levelObject("empty") for j in range(32)] for i in range(28)]   # generate 28x32 empty objects
        self.movingObjectPacman = movingObject("Pacman")
        self.movingObjectGhosts = [movingObject("Ghost") for n in range(4)]


    def levelGenerate(self, level):
        # set a directory for the resource file
        pathCurrentDir = os.path.dirname(__file__)  # current script directory
        pathRelDir = "../resource/level{}.txt".format(level)
        pathAbsDir = os.path.join(pathCurrentDir, pathRelDir)

        levelFile = open(pathAbsDir, encoding="utf-8")
        levelLineNo = 0

        # read line by line with readlines(), 'levelLine' temporarily save the string
        for levelLine in levelFile.readlines():

            levelLineSplit = list(levelLine) # split levelLine into characters

            # generate level objects
            for i in range(28):

                if levelLineSplit[i] == "_":    # passage
                    self.levelObjects[i][levelLineNo].name = "empty"
                elif levelLineSplit[i] == "#":  # wall
                    self.levelObjects[i][levelLineNo].name = "wall"
                elif levelLineSplit[i] == "$":  # ghost spawn point
                    self.levelObjects[i][levelLineNo].name = "cage"
                elif levelLineSplit[i] == ".":  # score pellet
                    self.levelObjects[i][levelLineNo].name = "pellet"
                elif levelLineSplit[i] == "*":  # power pellet
                    self.levelObjects[i][levelLineNo].name = "powerup"

                elif levelLineSplit[i] == "@":  # pacman
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # give the starting coordinate
                    self.movingObjectPacman.CoordinateRel[0] = i
                    self.movingObjectPacman.CoordinateRel[1] = levelLineNo
                    self.movingObjectPacman.CoordinateAbs[0] = i * 3
                    self.movingObjectPacman.CoordinateAbs[1] = levelLineNo * 3


                elif levelLineSplit[i] == "&":  # ghost
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # find an inactive ghost and give the starting coordinate
                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].CoordinateRel[0] = i
                            self.movingObjectGhosts[n].CoordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].CoordinateAbs[0] = i * 3
                            self.movingObjectGhosts[n].CoordinateAbs[1] = levelLineNo * 3
                            break   # break current loop (with generator 'n')

            levelLineNo += 1 # indicate which line we are

        levelFile.close()


    def loopFunction(self):
        pass



class levelObject(object):

    def __init__(self, name):
        self.name = name
        self.isDestroyed = False

    def moveRequest(self):
        return self.name



class movingObject(object):

    def __init__(self, name):
        self.name = name
        self.isActive = False   # check this object is ingame
        self.dirCurrent = "Left" # current direction, if cannot move w/ dirNext, the object will proceed this direction
        self.dirNext = "Left"   # the object will move this direction if it can
        self.CoordinateRel = [0, 0]   # Relative Coordinate, check can the object move given direction
        self.CoordinateAbs = [0, 0]   # Absolute Coordinate, use for widget(image) and object encounters

    def MoveNext(self, GameEngine):
        ## this function will determine the object can move with given direction or not

        if self.dirNext == self.dirCurrent: # in this case, no action is required
            pass
        
        else:
            if self.dirNext == "Left":  # check the direction first
                nextObject = GameEngine.levelObjects[self.CoordinateRel[0]-1][self.CoordinateRel[1]] # levelObject placed left of this object

                # check the levelObject and allow movingObject to change its current direction
                if nextObject.name == ("empty" or "pellet" or "powerup"):
                    self.dirCurrent = "Left"
                elif nextObject.name == ("wall" or "cage"):
                    pass
                

            elif self.dirNext == "Right":
                nextObject = GameEngine.levelObjects[self.CoordinateRel[0]+1][self.CoordinateRel[1]] # levelObject placed right of this object

                # check the levelObject and allow movingObject to change its current direction
                if nextObject.name == ("empty" or "pellet" or "powerup"):
                    self.dirCurrent = "Right"
                elif nextObject.name == ("wall" or "cage"):
                    pass


            elif self.dirNext == "Up":
                nextObject = GameEngine.levelObjects[self.CoordinateRel[0]][self.CoordinateRel[1]+1] # levelObject placed up of this object

                # check the levelObject and allow movingObject to change its current direction
                if nextObject.name == ("empty" or "pellet" or "powerup"):
                    self.dirCurrent = "Up"
                elif nextObject.name == ("wall" or "cage"):
                    pass


            elif self.dirNext == "Down":
                nextObject = GameEngine.levelObjects[self.CoordinateRel[0]][self.CoordinateRel[1]-1] # levelObject placed down of this object

                # check the levelObject and allow movingObject to change its current direction
                if nextObject.name == ("empty" or "pellet" or "powerup"):
                    self.dirCurrent = "Down"
                elif nextObject.name == ("wall" or "cage"):
                    pass
        
    
    def MoveCurrent(self):
        pass
        # 3으로 나눠서 rel좌표를 건드리거나 하는 판단을 해준다


gameEngine = GameEngine()



# treading Timer
    # 주인공은 지정된 방향으로 좌표 이동, moveRequest를 해당 방향으로
    # 만약 주인공 좌표가 (x,y)이고 방향이 right라면 (x,y+1)에 해당하는 오브젝트의 moveRequest를 불러온다
    # moveRequest의 return을 받아보고 갈 수 있는지 여부를 판단하고 실제 이동에 해당하는 function을 불러온다
    # 실제 이동에 해당하는 function은 좌표계를 3개로 쪼개서 이동하면서 스프라이트를 바꿔준다

    # if문을 이용하여 wall, pellet은 pass하고 팩맨, 고스트 등 움직이는 오브젝트만 place로 좌표를 재지정한다


    # 귀신들은 ai 만들기 힘드니까 지정된 구역 순찰해놓고 v1.1.0에서 알고리즘 develop해서 릴리즈
    # 한칸씩 움직임