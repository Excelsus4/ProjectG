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

        #f = open("6. QTableFile.txt", 'w')
        #for i in range(0, 8):
        #    for j in range(0, int(self.yLength)):
        #        for k in range(0, int(self.xLength)):
        #            for l in range(0, int(self.numGoal)):
        #                f.write(str(self.QTable[l][k][j][i]))
        #    f.write("\n")
        #f.close

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
            tempTuple.append(int(self.exitP[i * 3] + 200))
            tempTuple.append(int(200 - self.exitP[i * 3 + 2]))
            self.goalList.append(tempTuple)

        return self.buildingList


    def solve(self, a, b):
        startPoint = [int(a[0] + 400), int(400 - a[2])]
        endPoint = [int(b[0] + 400), int(400 - b[2])]
        endNum = self.findTabel(endPoint)
        result = self.QL(endNum, startPoint)                 #need CHANGE!!!!!!!!!!!!!!!!!

        return result

    def makeMap(self):
        
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
                else:
                    if self.mapTable[i-1][j] == 0 and self.mapTable[i+1][j] == 0 and self.mapTable[i][j-1] == 0 and self.mapTable[i][j+1] == 0:
                        self.mapTable[i][j] = 0


    #def takeSeta(self, pointX1, pointY1, pointX2, pointY2):
    #if pointX1 == pointX2:
    #    return 90
    #return math.atan(abs((pointY2 - pointY1) / (pointX2 - pointX1)))*180/math.pi

    #def takeTable(self, seta):
    #    if (seta >= 0 and seta < 22.5) or (seta >= 337.5 and seta < 360):
    #        return 2
    #    elif seta >= 22.5 and seta < 67.5:
    #        return 1
    #    elif seta >= 67.5 and seta < 112.5:
    #        return 0
    #    elif seta >= 112.5 and seta < 157.5:
    #        return 7
    #    elif seta >= 157.5 and seta < 202.5:
    #        return 6
    #    elif seta >= 202.5 and seta < 247.5:
    #        return 5
    #    elif seta >= 247.5 and seta < 292.5:
    #        return 4
    #    elif seta >= 292.5 and seta < 337.5:
    #        return 3

    # 7 0 1
    # 6 * 2
    # 5 4 3

    def findTabel(self, endPoint):
        temp = 0
        for i in range(0, int(len(self.goalList))):
            if self.goalList[i] == endPoint:
                temp = i
                break
        return temp


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
        maxDi = int(random.randrange(0, 8))

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
            #for i in range(1, n):
            i = 0
            myPoint = [0, 0]
            while i < n:
                #myPoint = (int(random.randrange(5, self.xLength)), int(random.randrange(5, self.yLength)))
                myPoint = [int(random.randrange(int(max(5, int(self.goalList[j][0] - 10 - i))), int(min(395, int(self.goalList[j][0] + 10 + i))))), int(random.randrange(int(max(5, int(self.goalList[j][1] - 10 - i))), int(min(395, int(self.goalList[j][1] + 10 + i)))))]
                #if myPoint type is block do again
                while self.mapTable[myPoint[0]][myPoint[1]] != 0:
                    #myPoint = (int(random.randrange(5, self.xLength)), int(random.randrange(5, self.yLength)))
                    myPoint = [int(random.randrange(int(max(5, int(self.goalList[j][0] - 10 - i))), int(min(395, int(self.goalList[j][0] + 10 + i))))), int(random.randrange(int(max(5, int(self.goalList[j][1] - 10 - i))), int(min(395, int(self.goalList[j][1] + 10 + i)))))]
                firstStartPoint = myPoint
                checkLoop = 0
                checkStep = 0
                nextPoint = [0, 0]
                while myPoint != self.goalList[j]:
                    #randomChoose = random.randrange(0, 100)
                    #if randomChoose < 30:
                    #    nextDi = takeTable(takeSeta(myPoint[0], myPoint[1], self.goalList[j][0], self.goalList[j][1]))
                    #else:
                    nextDi = random.randrange(0, 8)
                    nextDi = int(round(nextDi))
                    checkFailStart = 0

                    while self.RTable[j][myPoint[0]][myPoint[1]][nextDi] == -1:
                        nextDi = random.randrange(0, 8)
                        nextDi = int(round(nextDi))
                        checkFailStart = checkFailStart + 1
                        if checkFailStart > 50:
                            break
                    if checkFailStart > 50:
                        break

                    nextPoint[0], nextPoint[1] = self.nextLoc(myPoint[0], myPoint[1], nextDi)

                    self.QTable[j][myPoint[0]][myPoint[1]][nextDi] = self.RTable[j][myPoint[0]][myPoint[1]][nextDi] + alpha * self.maxQValue(j, nextPoint)
                    myPoint[0] = nextPoint[0]
                    myPoint[1] = nextPoint[1]
                    
                    checkStep = checkStep + 1
                    if checkStep > 1000:
                        myPoint = self.goalList[j]
                        f.write("check fail\n")
                        i = i - 1

                    if myPoint == firstStartPoint:
                        checkLoop = checkLoop + 1
                        f.write("check loop\n")
                    if checkLoop > 100:
                        myPoint = self.goalList[j]
                        f.write("check loop on\n")
                    
                
                i = i + 1

                f.write("check 1\n")

                    #pass nextpoint
        
        for i in range(0, 8):
            for j in range(0, int(self.yLength)):
                for k in range(0, int(self.xLength)):
                    for l in range(0, int(self.numGoal)):
                        f.write(str(self.QTable[l][k][j][i]))
            f.write("\n")

        f.write("check close\n")
        f.close()

        return 1
        #state


    def QL(self, tableNum, myPoint):
        lootList = []

        f = open("8. QLCheck.txt", 'w')

        myPoint[0] = int(myPoint[0])
        myPoint[1] = int(myPoint[1])
        nextPoint = [0, 0]

        while myPoint != self.goalList[tableNum]:
            nextDi = int(self.maxQDi(tableNum, myPoint))
            nextPoint[0], nextPoint[1] = self.nextLoc(myPoint[0], myPoint[1], nextDi)
            lootList.append(nextPoint)
            myPoint = nextPoint
            #pass nextpoint
        
        
        for i in range(0, len(lootList)):
            f.write(str(lootList[i][0]))
            f.write(" ")
            f.write(str(lootList[i][1]))
            f.write("\n")
        f.close
        
        return lootList