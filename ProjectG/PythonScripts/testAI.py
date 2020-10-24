import math
import random

class TestAI():
    #mapTable = np.zeros((xLength,yLength))
    #QTable = np.zeros((numGoal, xLength, yLength, 8))
    #RTable = np.zeros((numGoal, xLength, yLength, 8))

    def __init__(self, fls, exitP):
        self.fls = fls          #building float list
        self.exitP = exitP      #exitpoint float list

        self.numGoal = len(exitP) / 3
        self.xLength = 400
        self.yLength = 400
        self.goalList = []
        self.buildingList = []
        self.mapTable = [[0 for i in range(yLength)] for j in range(xLength)]
        self.QTable = [[[[0 for i in range(8)] for j in range(yLength)] for k in range(xLength)] for l in range(numGoal)]
        self.RTable = [[[[0 for i in range(8)] for j in range(yLength)] for k in range(xLength)] for l in range(numGoal)]
        
        #passing()
        #makeMap()
        #makeTable()
        #QLTrain()


    def passing(self):
        tempTuple = []
        for i in range(0, len(self.fls) / 8):
            for j in range(0, 7):
                tempTuple.append(self.fls[i * 8 + j])
            buildingList.append(tempTuple)
        
        tempTuple = []
        for i in range(0, len(self.exitP) / 3):
            tempTuple.append(self.exitP[i * 3])
            tempTuple.append(self.exitP[i * 3 + 2])
            goalList.append(tempTuple)

        return buildingList


    def solve(self, a, b):
        result = QL()

        return result
    

    def turn(self, typeCode, pointX, pointZ, sizeX, sizeZ, seta):
        pointList = []

        for i in range(round(-1 * sizeX/2), round(sizeX/2 + 1)):
            for j in range(round(-1 * sizeZ/2), round(sizeZ/2 + 1)):
                x = i * math.cos(seta) - j * math.sin(seta)
                x = round(x + pointX)
                z = i * math.sin(seta) + j * math.cos(seta)
                z = round(z + pointZ)
                pointList.append([x, z])
        
        return pointList

    def makeMap(self):
        #not tuple
        #for i in range(0, len(buildingList) / 8):
        #    typeCode = buildingList[i * 8]
        #    pointX = buildingList[i * 8 + 1]
        #    pointY = buildingList[i * 8 + 3]
        #    sizeX = buildingList[i * 8 + 4]
        #    sizeZ = buildingList[i * 8 + 6]
        #    seta = buildingList[i * 8 + 7]
        
        #tuple
        for i in range(0, len(buildingList)):
            typeCode = buildingList[i][0]
            pointX = buildingList[i][1]
            pointY = buildingList[i][3]
            sizeX = buildingList[i][4]
            sizeZ = buildingList[i][6]
            seta = buildingList[i][7]

            #turn & put map
            for j in range(round(-1 * sizeX/2), round(sizeX/2 + 1)):
                for k in range(round(-1 * sizeZ/2), round(sizeZ/2 + 1)):
                    x = j * math.cos(seta) - k * math.sin(seta)
                    x = round(x + pointX) + 200
                    z = j * math.sin(seta) + k * math.cos(seta)
                    z = round(z + pointZ) + 200
                    mapTable[x][z] = typeCode

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
        [x, y] = nextLoc(pointX, pointY, di)
        
        if [x,y] is goalList[goalNum]:
            return 1000

        if x < 0 or y < 0 or x > xLength or y > yLength:
            return -2
        elif mapTable[x][y] == 0:
            return -1
        elif mapTable[x][y] == 1 or mapTable[x][y] == 2:
            return 0
        
        return 0


    def makeTable(self):
        for w in range(0, len(goalList)):
            for i in range(0, xLength):
                for j in range(0, yLength):
                    for k in range(0, 8):
                        if checkValue(i, j, k) is not -2:
                            RTable[w][i][j][k] = checkValue(w, i, j, k)

        QTable = RTable


    def maxQValue(self, tableNum, nextState):
        maxValue = 0

        for i in range(0, 8):
            if QTable[tableNum][nextState[0]][nextState[1]][i] > maxValue:
                maxValue = QTable[tableNum][nextState[0]][nextState[1]][i]
        return maxValue


    def maxQDi(self, tableNum, myState):
        maxValue = 0
        maxDi = 0

        for i in range(0, 8):
            if QTable[tableNum][myState[0]][myState[1]][i] > maxValue:
                maxValue = QTable[tableNum][myState[0]][myState[1]][i]
                maxDi = i
        return maxDi


    #point pass def
    def passPoint(self):
        pass


    def QLTrain(self):
        #repeat n
        n = 1000
        alpha = 0.5

        for j in range(1, len(goalList)):
            for i in range(1, n):
                myPoint = (random.randrange(5, xLength), random.randrange(5, yLength))
                while myPoint == goalList[j]:
                    nextPoint = random.randrange(0, 8)
                    while RTable[j][myPoint[0]][myPoint[1]][nextPoint] is not -1:
                        nextPoint = random.randrange(0, 8)
                    nextState = nextLoc(myPoint[0], myPoint[1], nextPoint)
                    
                    QTable[j][myPoint[0]][myPoint[1]][nextPoint] = RTable[j][myPoint[0]][myPoint[1]][nextPoint] + alpha * maxQValue(j, nextState)
                    myPoint = nextPoint
                    #pass nextpoint

        return 1
        #state


    def QL(self, tableNum, myPoint):
        lootList = []

        while myPoint == goalList[tableNum]:
            nextDi = maxQDi(tableNum, myPoint)
            nextPoint = nextLoc(myPoint[0], myPoint[1], nextDi)
            lootList.append(myPoint)
            myPoint = nextPoint
            #pass nextpoint
        
        return lootList