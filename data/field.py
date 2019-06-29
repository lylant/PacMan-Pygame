import os
from random import randint


class GameEngine(object):

    def __init__(self):

        self.levelObjects = [[levelObject("empty") for j in range(32)] for i in range(28)]   # generate 28x32 empty objects
        self.movingObjectPacman = movingObject("Pacman")
        self.movingObjectGhosts = [movingObject("Ghost") for n in range(4)]

        self.levelObjectNamesBlocker = ["wall", "cage"]
        self.levelObjectNamesPassable = ["empty", "pellet", "powerup"]


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
                    self.movingObjectPacman.coordinateRel[0] = i
                    self.movingObjectPacman.coordinateRel[1] = levelLineNo
                    self.movingObjectPacman.coordinateAbs[0] = i * 4
                    self.movingObjectPacman.coordinateAbs[1] = levelLineNo * 4


                elif levelLineSplit[i] == "&":  # free ghost
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # find an inactive ghost and give the starting coordinate
                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].isCaged = False
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 4
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 4
                            break   # break current loop (with generator 'n')

                elif levelLineSplit[i] == "%":  # caged ghost
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # find an inactive ghost and give the starting coordinate
                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 4
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 4
                            break   # break current loop (with generator 'n')


            levelLineNo += 1 # indicate which line we are

        levelFile.close()


    def encounterEvent(self, x, y):
        if self.levelObjects[x][y].name == "empty":
            result = "empty"

        elif self.levelObjects[x][y].name == "pellet":
            result = "pellet"

        elif self.levelObjects[x][y].name == "powerup":
            result = "powerup"
        
        return result



    def loopFunction(self):
        self.movingObjectPacman.MoveNextPacman(self)
        self.movingObjectPacman.MoveCurrent(self)

        for i in range(4):
            if self.movingObjectGhosts[i].isActive == True:
                self.movingObjectGhosts[i].MoveNextPacman(self)
                self.movingObjectGhosts[i].MoveCurrent(self)
            
            else:
                pass






class levelObject(object):

    def __init__(self, name):
        self.name = name
        self.isDestroyed = False

    def moveRequest(self):
        return self.name




## 귀신이 stop이면, 그리고 디렉션 체인지가 가능한 곳에서 랜더마이즈


class movingObject(object):

    def __init__(self, name):
        self.name = name
        self.isActive = False   # check this object is an active ghost (not used for pacman)
        self.isCaged = True     # check this object is caged (only for ghost)
        self.dirCurrent = "Left" # current direction, if cannot move w/ dirNext, the object will proceed this direction
        self.dirNext = "Left"   # the object will move this direction if it can
        self.dirEdgePassed = False # check the object passed one of field edges
        self.coordinateRel = [0, 0]   # Relative Coordinate, check can the object move given direction
        self.coordinateAbs = [0, 0]   # Absolute Coordinate, use for widget(image) and object encounters


    def MoveNextPacman(self, GameEngine):
        ## this function will determine pacman can move with given direction or not

        if self.dirNext == self.dirCurrent: # in this case, no action is required
            pass
        
        elif self.coordinateAbs[0] % 4 != 0: # if the object is moving, prevent to change its direction
            pass

        elif self.coordinateAbs[1] % 4 != 0: # if the object is moving, prevent to change its direction
            pass

        else:
            if self.dirNext == "Left":  # check the direction first

                if self.coordinateRel[0] == 0: # at left edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Left"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]] # levelObject placed left of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Left"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass
                

            elif self.dirNext == "Right":

                if self.coordinateRel[0] == 27: # at right edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Right"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]] # levelObject placed right of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Right"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Down":

                if self.coordinateRel[1] == 31: # at bottom edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Down"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1] # levelObject placed down of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Down"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Up":

                if self.coordinateRel[1] == 0: # at top edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Up"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1] # levelObject placed up of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Up"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass



    def MoveNextGhost(self, GameEngine):
        ## this function will determine ghost's moving direction

        if self.isCaged == True:    # if ghost is caged, prevent the movement
            pass

        elif self.coordinateAbs[0] % 4 != 0: # if the object is moving, prevent to change its direction
            pass

        elif self.coordinateAbs[1] % 4 != 0: # if the object is moving, prevent to change its direction
            pass

        else:
            randNo = randint(0, 3) # generate a random number 0-3
            
            # determine ghost's direction
            while True:

                if randNo % 4 == 0: # check left
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]] # levelObject placed left of this object
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Left" # set the direction
                        break # escape the loop
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass # check the next direction (using randNo as generator)

                elif randNo % 4 == 1: # check right
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]]
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Right"
                        break
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass
                
                elif randNo % 4 == 2: # check down
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1]
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Down"
                        break
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass

                elif randNo % 4 == 3: # check up
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1]
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Up"
                        break
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass
                
                randNo += 1
            
            print("cRel:", self.coordinateRel[0], self.coordinateRel[1], "cAbs:", self.coordinateAbs[0], self.coordinateAbs[1], "dir:", self.dirCurrent)                

        
    
    def MoveCurrent(self, GameEngine):

        if self.dirCurrent == "Left":

            if self.coordinateAbs[0] == 0: # at left edge, move to right edge
                self.coordinateAbs[0] = 27*4 + 3
                self.coordinateRel[0] = 28
                self.dirEdgePassed = True
            
            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]] # levelObject placed left of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[0] -= 1 # adjust current coordinate
                    if self.coordinateAbs[0] % 4 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[0] -= 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Right":

            if self.coordinateAbs[0] == 27*4:  # at right edge, move to left edge
                self.coordinateAbs[0] = -3
                self.coordinateRel[0] = -1
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]] # levelObject placed right of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[0] += 1  # adjust current coordinate
                    if self.coordinateAbs[0] % 4 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[0] += 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Down":

            if self.coordinateAbs[1] == 31*4:  # at bottom edge, move to top edge
                self.coordinateAbs[1] = -3
                self.coordinateRel[1] = -1
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1] # levelObject placed down of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[1] += 1  # adjust current coordinate
                    if self.coordinateAbs[1] % 4 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[1] += 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Up":

            if self.coordinateAbs[1] == 0:  # at top edge, move to bottom edge
                self.coordinateAbs[1] = 31*4 + 3
                self.coordinateRel[1] = 32
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1] # levelObject placed up of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[1] -= 1  # adjust current coordinate
                    if self.coordinateAbs[1] % 4 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[1] -= 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Stop":
            pass

        if self.isActive == True and self.isCaged == False:
            print("cRel:", self.coordinateRel[0], self.coordinateRel[1], "cAbs:", self.coordinateAbs[0], self.coordinateAbs[1], "dir:", self.dirCurrent)


gameEngine = GameEngine()