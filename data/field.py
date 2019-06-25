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


gameEngine = GameEngine()