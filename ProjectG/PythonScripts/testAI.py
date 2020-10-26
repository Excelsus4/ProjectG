import math
import random

class TestAI():
    #mapTable = np.zeros((xLength,yLength))
    #QTable = np.zeros((numGoal, xLength, yLength, 8))
    #RTable = np.zeros((numGoal, xLength, yLength, 8))

    def __init__(self, fls, exitP):
        self.fls = fls          #building float list
        self.exitP = exitP      #exitpoint float list

        self.numGoal = int(len(exitP) // 3)
        self.xLength = 400
        self.yLength = 400
        self.goalList = []
        self.buildingList = []
        self.mapTable = [[0 for i in range(0, int(self.yLength))] for j in range(0, int(self.xLength))]
        self.QTable = [[[[0 for i in range(0,8)] for j in range(0, int(self.yLength))] for k in range(0, int(self.xLength))] for l in range(0, int(self.numGoal))]
        self.RTable = [[[[0 for i in range(0,8)] for j in range(0, int(self.yLength))] for k in range(0, int(self.xLength))] for l in range(0, int(self.numGoal))]
        
        self.passing()
        self.makeMap()
        self.makeTable()
        self.QLTrain()


    def passing(self):
        tempTuple = []
        for i in range(0, int(len(self.fls) // 8)):
            for j in range(0, 7):
                tempTuple.append(int(self.fls[i * 8 + j]))
            self.buildingList.append(tempTuple)
        
        tempTuple = []
        for i in range(0, int((len(self.exitP) // 3))):
            tempTuple.append(int(self.exitP[i * 3]))
            tempTuple.append(int(self.exitP[i * 3 + 2]))
            self.goalList.append(tempTuple)

        return self.buildingList


    def solve(self, a, b):
        #startPoint = [int(a[0]), int(a[2])]
        result = [0]
        #result = self.QL(0, startPoint)                 #need CHANGE!!!!!!!!!!!!!!!!!

        return result
    

    def turn(self, typeCode, pointX, pointZ, sizeX, sizeZ, seta):
        pointList = []

        for i in range(int(round(-1 * sizeX//2)), int(round(sizeX//2 + 1))):
            for j in range(int(round(-1 * sizeZ//2)), int(round(sizeZ//2 + 1))):
                x = i * math.cos(seta) - j * math.sin(seta)
                x = int(round(x + pointX))
                z = i * math.sin(seta) + j * math.cos(seta)
                z = int(round(z + pointZ))
                pointList.append([x, z])
        
        return pointList

    def makeMap(self):
        #not tuple
        #for i in range(0, len(self.buildingList) / 8):
        #    typeCode = self.buildingList[i * 8]
        #    pointX = self.buildingList[i * 8 + 1]
        #    pointY = self.buildingList[i * 8 + 3]
        #    sizeX = self.buildingList[i * 8 + 4]
        #    sizeZ = self.buildingList[i * 8 + 6]
        #    seta = self.buildingList[i * 8 + 7]
        
        #tuple
        for i in range(0, int(len(self.buildingList))):
            typeCode = self.buildingList[i][0]
            pointX = self.buildingList[i][1]
            pointZ = self.buildingList[i][3]
            sizeX = self.buildingList[i][4]
            sizeZ = self.buildingList[i][6]
            seta = self.buildingList[i][7]

            #turn & put map
            for j in range(int(round(-1 * sizeX//2)), int(round(sizeX//2 + 1))):
                for k in range(int(round(-1 * sizeZ//2)), int(round(sizeZ//2 + 1))):
                    x = j * math.cos(seta) - k * math.sin(seta)
                    x = int(round(x + pointX)) + 200
                    z = j * math.sin(seta) + k * math.cos(seta)
                    z = int(round(z + pointZ)) + 200
                    self.mapTable[x][z] = typeCode

    # 7 0 1
    # 6 * 2
    # 5 4 3

    def nextLoc(self, pointX, pointY, di):
        if di == 0:
            x = pointX
            y = pointY - 1
        elif di == 1:
            x = pointX + 1
            y = pointY - 1
        elif di == 2:
            x = pointX + 1
            y = pointY
        elif di == 3:
            x = pointX + 1
            y = pointY + 1
        elif di == 4:
            x = pointX
            y = pointY + 1
        elif di == 5:
            x = pointX - 1
            y = pointY + 1
        elif di == 6:
            x = pointX - 1
            y = pointY
        elif di == 7:
            x = pointX - 1
            y = pointY - 1

        return [x, y]


    def checkValue(self, goalNum, pointX, pointY, di):
        [x, y] = self.nextLoc(pointX, pointY, di)
        
        if [x,y] is self.goalList[goalNum]:
            return 1000

        if x < 0 or y < 0 or x >= self.xLength or y >= self.yLength:
            return -2
        elif self.mapTable[x][y] == 0:
            return -1
        elif self.mapTable[x][y] == 1 or self.mapTable[x][y] == 2:
            return 0
        
        return 0


    def makeTable(self):
        for w in range(0, int(len(self.goalList))):
            for i in range(0, int(self.xLength)):
                for j in range(0, int(self.yLength)):
                    for k in range(0, 8):
                        if self.checkValue(w, i, j, k) is not -2:
                            self.RTable[w][i][j][k] = self.checkValue(w, i, j, k)

        self.QTable = self.RTable


    def maxQValue(self, tableNum, nextState):
        maxValue = 0

        for i in range(0, 8):
            if self.QTable[tableNum][nextState[0]][nextState[1]][i] > maxValue:
                maxValue = self.QTable[tableNum][nextState[0]][nextState[1]][i]
        return maxValue


    def maxQDi(self, tableNum, myState):
        maxValue = 0
        maxDi = 0

        for i in range(0, 8):
            if self.QTable[tableNum][myState[0]][myState[1]][i] > maxValue:
                maxValue = self.QTable[tableNum][myState[0]][myState[1]][i]
                maxDi = i
        return maxDi


    #point pass def
    def passPoint(self):
        pass


    def QLTrain(self):
        #repeat n
        n = 10
        alpha = 0.5

        for j in range(1, int(len(self.goalList))):
            for i in range(1, n):
                myPoint = (int(random.randrange(5, self.xLength)), int(random.randrange(5, self.yLength)))
                #if myPoint type is block do again
                while self.mapTable[myPoint[0]][myPoint[1]] != 0:
                    myPoint = (int(random.randrange(5, self.xLength)), int(random.randrange(5, self.yLength)))
                while myPoint != self.goalList[j]:
                    nextPoint = random.randrange(0, 8)
                    nextPoint = int(round(nextPoint))
                    while self.RTable[j][myPoint[0]][myPoint[1]][nextPoint] == -1:
                        nextPoint = random.randrange(0, 8)
                        nextPoint = round(nextPoint)
                    nextState = self.nextLoc(myPoint[0], myPoint[1], nextPoint)
                    
                    self.QTable[j][myPoint[0]][myPoint[1]][nextPoint] = self.RTable[j][myPoint[0]][myPoint[1]][nextPoint] + alpha * self.maxQValue(j, nextState)
                    myPoint = nextPoint
                    #pass nextpoint

        return 1
        #state


    def QL(self, tableNum, myPoint):
        lootList = []

        while myPoint == self.goalList[tableNum]:
            nextDi = self.maxQDi(tableNum, myPoint)
            nextPoint = self.nextLoc(myPoint[0], myPoint[1], nextDi)
            lootList.append(myPoint)
            myPoint = nextPoint
            #pass nextpoint
        
        return lootList