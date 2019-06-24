import os


class GameEngine(object):

    def __init__(self):

        self.levelObjects = [[levelObject("empty") for j in range(32)] for i in range(28)]   # generate 28x32 empty objects


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
                if levelLineSplit[i] == "_":
                    self.levelObjects[i][levelLineNo].name = "empty"
                elif levelLineSplit[i] == "#":
                    self.levelObjects[i][levelLineNo].name = "wall"
                elif levelLineSplit[i] == "$":
                    self.levelObjects[i][levelLineNo].name = "cage"
                elif levelLineSplit[i] == ".":
                    self.levelObjects[i][levelLineNo].name = "pellet"
                elif levelLineSplit[i] == "@":
                    self.levelObjects[i][levelLineNo].name = "pacman"
                elif levelLineSplit[i] == "&":
                    self.levelObjects[i][levelLineNo].name = "ghost"


            levelLineNo += 1 # indicate which line we are
                    




                # .strip() will remove any character with passed argument
                # nothing is passed so whitespace will removed (default)


        levelFile.close()


class levelObject(object):

    def __init__(self, name):
        self.name = name

    def moveRequest(self):
        return self.name



# 오브젝트 클래스
    # def moveRequest
        # 벽: return Wall
        # 콩알: return Score, 자신 파괴


gameEngine = GameEngine()