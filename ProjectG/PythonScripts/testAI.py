import math
import random

class TestAI():
    #mapTable = np.zeros((xLength,yLength))
    #QTable = np.zeros((numGoal, xLength, yLength, 8))
    #RTable = np.zeros((numGoal, xLength, yLength, 8))

    def __init__(self, fls, exitP):
        self.fls = fls          #building float list
        self.fls = [ 1.00 , -49.20 , 0.25 , 70.10 , 32.61 , 0.50 , 63.70 , 17.46 , 1.00 , -66.10 , 0.25 , 67.30 , 47.60 , 0.50 , 63.70 , 1.60 , 1.00 , 0.79 , 0.25 , 52.87 , 19.90 , 0.50 , 39.60 , 20.00 , 1.00 , 12.91 , 0.25 , 42.71 , 38.90 , 0.50 , 30.60 , 10.00 , 1.00 , -10.34 , 0.25 , 36.05 , 9.50 , 0.50 , 5.00 , 45.90 , 1.00 , 22.49 , 0.25 , 59.50 , 12.16 , 0.50 , 23.40 , 320.00 , 1.00 , 8.55 , 0.25 , 69.57 , 8.20 , 0.50 , 21.46 , 276.78 , 1.00 , 26.50 , 0.25 , -10.00 , 10.00 , 0.50 , 40.80 , 7.00 , 1.00 , 6.31 , 0.25 , 7.61 , 35.60 , 0.50 , 8.79 , 4.00 , 1.00 , 6.95 , 0.25 , -9.57 , 45.80 , 0.50 , 8.79 , 47.90 , 1.00 , 11.30 , 0.25 , -0.30 , 25.85 , 0.50 , 8.79 , 4.00 , 2.00 , -27.50 , 0.01 , 42.20 , 5.00 , 10.00 , 38.30 , 282.30 , 2.00 , -7.89 , 0.01 , 23.27 , 5.00 , 10.00 , 21.10 , 4.02 ]
        self.exitP = exitP      #exitpoint float list
        self.exitP = [ 15.00 , 0.00 , -1.00 ]

        self.numGoal = int(len(exitP) // 3)
        #self.numGoal = 4
        self.xLength = 400
        self.yLength = 400
        self.goalList = []
        self.buildingList = []
        self.mapTable = [[0 for i in range(0, int(self.yLength))] for j in range(0, int(self.xLength))]
        self.QTable = [[[[0 for i in range(0,8)] for j in range(0, int(self.yLength))] for k in range(0, int(self.xLength))] for l in range(0, int(self.numGoal))]
        #self.RTable = [[[[0 for i in range(0,8)] for j in range(0, 8)] for k in range(0, 8)] for l in range(0, 8)]
        self.RTable = [[[[0 for i in range(0,8)] for j in range(0, int(self.yLength))] for k in range(0, int(self.xLength))] for l in range(0, int(self.numGoal))]

        f = open("1. check.txt", 'w')
        f.write("check")
        f.write(str(5.55))
        f.write("\n")
        f.write(str(len(self.fls)))
        f.write("\n")
        f.write(str(len(self.exitP)))
        f.close

        self.passing()

        f = open("2. buildFile.txt", 'w')
        for i in range(0, int(len(self.buildingList))):
            for j in range(0, 8):
                f.write(str(self.buildingList[i][j]))
                f.write(" ")
            f.write("\n")
        f.close

        f = open("3. goalFile.txt", 'w')
        for i in range(0, int(len(self.goalList))):
            f.write(str(self.goalList[i]))
            f.write(" ")
        f.close

        self.makeMap()

        f = open("4. mapFile.txt", 'w')
        for i in range(0, int(self.yLength)):
            for j in range(0, int(self.xLength)):
                f.write(str(self.mapTable[j][i]))
            f.write("\n")
        f.close

        self.makeTable()

        f = open("5. RTableFile.txt", 'w')
        for i in range(0, 8):
            for j in range(0, int(self.yLength)):
                for k in range(0, int(self.xLength)):
                    for l in range(0, int(self.numGoal)):
                        f.write(str(self.RTable[l][k][j][i]))
            f.write("\n")
        f.close

        f = open("6. QTableFile.txt", 'w')
        for i in range(0, 8):
            for j in range(0, int(self.yLength)):
                for k in range(0, int(self.xLength)):
                    for l in range(0, int(self.numGoal)):
                        f.write(str(self.QTable[l][k][j][i]))
            f.write("\n")
        f.close

        self.QLTrain()


    def passing(self):
        tempTuple = []
        for i in range(0, int(len(self.fls) // 8)):
            tempTuple = []
            for j in range(0, 8):
                tempTuple.append(float(self.fls[i * 8 + j]))
            self.buildingList.append(tempTuple)
        
        tempTuple = []
        for i in range(0, int((len(self.exitP) // 3))):
            tempTuple = []
            tempTuple.append(float(self.exitP[i * 3]))
            tempTuple.append(float(self.exitP[i * 3 + 2]))
            self.goalList.append(tempTuple)

        return self.buildingList


    def solve(self, a, b):
        startPoint = [int(a[0]), int(a[2])]
        result = self.QL(0, startPoint)                 #need CHANGE!!!!!!!!!!!!!!!!!

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

                x = j
                z = k
                x = x * math.cos(seta) - z * math.sin(seta)
                z = x * math.sin(seta) + z * math.cos(seta)
                x = x + pointX
                z = z + pointZ
                x = int(round(x)) + 200
                z = int(round(z)) + 200
        
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
            seta = seta / 180 * math.pi * -1

            #turn & put map
            for j in range(int(round(-1 * sizeX//2)), int(round(sizeX//2 + 1))):
                for k in range(int(round(-1 * sizeZ//2)), int(round(sizeZ//2 + 1))):
                    x = j * math.cos(seta) - k * math.sin(seta)
                    z = j * math.sin(seta) + k * math.cos(seta)
                    x = x + pointX
                    z = z + pointZ
                    x = int(round(x)) + 200
                    z = 200 - int(round(z))
                    self.mapTable[x][z] = int(typeCode)
        
        for i in range(1, int(self.xLength) - 1):
            for j in range(1, int(self.yLength) - 1):
                if self.mapTable[i][j] == 0:
                    if self.mapTable[i-1][j] == 1 and self.mapTable[i+1][j] == 1 and self.mapTable[i][j-1] == 1 and self.mapTable[i][j+1] == 1:
                        self.mapTable[i][j] = 1
                    elif self.mapTable[i-1][j] == 2 and self.mapTable[i+1][j] == 2 and self.mapTable[i][j-1] == 2 and self.mapTable[i][j+1] == 2:
                        self.mapTable[i][j] = 2

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

        return x, y


    def checkValue(self, goalNum, pointX, pointY, di):
        x, y = self.nextLoc(pointX, pointY, di)
        
        if x == self.goalList[goalNum][0] and y == self.goalList[goalNum][1]:
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
                        if self.checkValue(w, i, j, k) != -2:
                            self.RTable[w][i][j][k] = self.checkValue(w, i, j, k)
                        #self.RTable[w][i][j][k] = self.checkValue(w, i, j, k)

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

        f = open("7. QLTrainCheck.txt", 'w')
        f.write("check open\n")

        for j in range(1, int(len(self.goalList))):
            for i in range(1, n):
                myPoint = (int(random.randrange(5, self.xLength)), int(random.randrange(5, self.yLength)))
                #if myPoint type is block do again
                while self.mapTable[myPoint[0]][myPoint[1]] != 0:
                    myPoint = (int(random.randrange(5, self.xLength)), int(random.randrange(5, self.yLength)))
                firstStartPoint = myPoint
                checkLoop = 0
                while myPoint != self.goalList[j]:
                    nextPoint = random.randrange(0, 8)
                    nextPoint = int(round(nextPoint))
                    while self.RTable[j][myPoint[0]][myPoint[1]][nextPoint] == -1:
                        nextPoint = random.randrange(0, 8)
                        nextPoint = round(nextPoint)
                    nextState = self.nextLoc(myPoint[0], myPoint[1], nextPoint)
                    
                    self.QTable[j][myPoint[0]][myPoint[1]][nextPoint] = self.RTable[j][myPoint[0]][myPoint[1]][nextPoint] + alpha * self.maxQValue(j, nextState)
                    myPoint = nextPoint
                    if myPoint == firstStartPoint:
                        checkLoop = checkLoop + 1
                    if checkLoop > 100:
                        myPoint = self.goalList[j]

                    #pass nextpoint
        
        f.close()

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
        
        f = open("8. QLCheck.txt", 'w')
        for i in range(0, len(lootList)):
            f.write(str(lootList[i]))
            f.write("\n")
        f.close
        
        return lootList