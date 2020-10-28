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
            tempTuple.append(int(self.exitP[i * 3] + self.xLength // 2))
            tempTuple.append(int(self.yLength // 2 - self.exitP[i * 3 + 2]))
            self.goalList.append(tempTuple)

        return self.buildingList


    def solve(self, a, b):
        startPoint = [int(a[0] + self.xLength // 2), int(self.yLength // 2 - a[2])]
        endPoint = [int(b[0] + self.xLength // 2), int(self.yLength // 2 - b[2])]
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
                    x = int(round(x)) + self.xLength // 2
                    z = self.yLength // 2 - int(round(z))
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
            if int(self.goalList[i][0]) == int(endPoint[0]) or int(self.goalList[i][1]) == int(endPoint[1]):
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
        x = int(x)
        y = int(y)
        
        if x == int(self.goalList[goalNum][0]) and y == int(self.goalList[goalNum][1]):
            return 300

        if x < 0 or y < 0 or x >= self.xLength or y >= self.yLength:
            return -2
        elif int(self.mapTable[x][y]) == 0:
            return -1
        elif int(self.mapTable[x][y]) == 1 or int(self.mapTable[x][y]) == 2:
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
        canMoveDi = []

        print(myState)

        for i in range(0, 8):
            tempDi = i
            if self.QTable[tableNum][myState[0]][myState[1]][i] > maxValue:
                maxValue = self.QTable[tableNum][myState[0]][myState[1]][i]
                canMoveDi = [tempDi]
            elif self.QTable[tableNum][myState[0]][myState[1]][i] == maxValue:
                canMoveDi.append(tempDi)

        if int(len(canMoveDi)) > 1:
            temp = int(random.randrange(0, int(len(canMoveDi))))
        else:
            temp = 0
        maxDi = int(canMoveDi[temp])

        print(canMoveDi)
        print(maxDi)
        print(maxValue)

        return maxDi


    #point pass def
    def passPoint(self):
        pass


    def QLTrain(self):
        #repeat n
        n = 100
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
                while self.mapTable[myPoint[0]][myPoint[1]] == 0:
                    #myPoint = (int(random.randrange(5, self.xLength)), int(random.randrange(5, self.yLength)))
                    myPoint = [int(random.randrange(int(max(5, int(self.goalList[j][0] - 10 - i))), int(min(395, int(self.goalList[j][0] + 10 + i))))), int(random.randrange(int(max(5, int(self.goalList[j][1] - 10 - i))), int(min(395, int(self.goalList[j][1] + 10 + i)))))]
                
                firstStartPoint = myPoint
                checkLoop = 0
                checkStep = 0
                nextPoint = [0, 0]

                while int(myPoint[0]) != int(self.goalList[j][0]) or int(myPoint[1]) != int(self.goalList[j][1]):
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
                    if int(nextPoint[0]) == int(self.goalList[j][0]) and int(nextPoint[1]) == int(self.goalList[j][1]):
                        break

                    self.QTable[j][myPoint[0]][myPoint[1]][nextDi] = self.RTable[j][myPoint[0]][myPoint[1]][nextDi] + alpha * self.maxQValue(j, nextPoint)
                    myPoint[0] = int(nextPoint[0])
                    myPoint[1] = int(nextPoint[1])
                    
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
                        i = i - 1
                    
                
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

        while int(myPoint[0]) != int(self.goalList[tableNum][0]) or int(myPoint[1]) != int(self.goalList[tableNum][1]):
            nextDi = int(self.maxQDi(tableNum, myPoint))
            nextPoint[0], nextPoint[1] = self.nextLoc(myPoint[0], myPoint[1], nextDi)
            lootList.append(float(nextPoint[0] - self.xLength//2))
            lootList.append(0.0)
            lootList.append(float(self.yLength//2 - nextPoint[1]))
            myPoint[0] = int(nextPoint[0])
            myPoint[1] = int(nextPoint[1])
            #pass nextpoint
        
        
        for i in range(0, int(len(lootList) // 3)):
            f.write(str(lootList[i*3]))
            f.write(" ")
            f.write(str(lootList[i*3 + 1]))
            f.write(" ")
            f.write(str(lootList[i*3 + 2]))
            f.write("\n")
        f.close
        
        return lootList

testAi = TestAI([ 2.00 , -38.40 , 0.01 , 23.80 , 7.80 , 10.00 , 38.30 , 328.00,
2.00 , -27.50 , 0.01 , 42.20 , 5.00 , 10.00 , 38.30 , 282.30,
2.00 , -7.89 , 0.01 , 23.27 , 5.00 , 10.00 , 21.10 , 4.02,
2.00 , -57.20 , 0.01 , 26.70 , 7.70 , 10.00 , 21.10 , 6.20,
2.00 , -45.60 , 0.01 , 7.40 , 7.70 , 10.00 , 18.90 , 282.30,
2.00 , -63.40 , 0.01 , -66.90 , 3.90 , 10.00 , 23.30 , 282.30,
1.00 , -49.20 , 0.25 , 70.10 , 32.61 , 0.50 , 63.70 , 17.46,
1.00 , -66.10 , 0.25 , 67.30 , 47.60 , 0.50 , 63.70 , 1.60,
1.00 , -32.22 , 0.25 , -40.65 , 30.00 , 0.50 , 70.00 , 12.00,
1.00 , -6.92 , 0.25 , -23.51 , 20.00 , 0.50 , 74.00 , 316.65,
1.00 , 8.02 , 0.25 , -60.85 , 20.00 , 0.50 , 45.00 , 21.70,
1.00 , -32.71 , 0.25 , 1.53 , 11.80 , 0.50 , 20.00 , 11.00,
1.00 , -18.25 , 0.25 , -69.23 , 60.00 , 0.50 , 20.00 , 12.00,
1.00 , -82.27 , 0.25 , -29.62 , 36.50 , 0.50 , 100.00 , 15.00,
1.00 , -58.83 , 0.25 , 13.95 , 10.00 , 0.50 , 10.00 , 45.00,
1.00 , -74.20 , 0.25 , 17.37 , 30.00 , 0.50 , 10.00 , 5.00,
1.00 , 0.79 , 0.25 , 52.87 , 19.90 , 0.50 , 39.60 , 20.00,
1.00 , 12.91 , 0.25 , 42.71 , 38.90 , 0.50 , 30.60 , 10.00,
1.00 , -10.34 , 0.25 , 36.05 , 9.50 , 0.50 , 5.00 , 45.90,
1.00 , 22.49 , 0.25 , 59.50 , 12.16 , 0.50 , 23.40 , 320.00,
1.00 , 8.55 , 0.25 , 69.57 , 8.20 , 0.50 , 21.46 , 276.78,
1.00 , 26.50 , 0.25 , -10.00 , 10.00 , 0.50 , 40.80 , 7.00,
1.00 , 6.31 , 0.25 , 7.61 , 35.60 , 0.50 , 8.79 , 4.00,
1.00 , 6.95 , 0.25 , -9.57 , 45.80 , 0.50 , 8.79 , 47.90,
1.00 , 11.30 , 0.25 , -0.30 , 25.85 , 0.50 , 8.79 , 4.00,
0.00 , -82.99 , 7.00 , -84.70 , 18.00 , 14.00 , 15.00 , 6.00,
0.00 , -68.06 , 2.00 , 69.23 , 12.00 , 4.00 , 12.00 , 350.00,
0.00 , -89.92 , 4.00 , 65.38 , 13.00 , 8.00 , 48.00 , 354.00,
0.00 , -70.15 , 6.00 , 94.35 , 50.00 , 12.00 , 25.00 , 350.00,
0.00 , -20.32 , 5.00 , -25.61 , 30.00 , 10.00 , 10.00 , 15.00,
0.00 , -23.10 , 8.00 , -32.12 , 12.00 , 16.00 , 13.00 , 15.00,
0.00 , -25.31 , 3.50 , -48.09 , 35.00 , 7.00 , 50.00 , 15.00,
0.00 , -3.28 , 3.00 , -50.88 , 30.00 , 6.00 , 30.00 , 45.00,
0.00 , -3.94 , 2.50 , -61.06 , 30.00 , 5.00 , 30.00 , 23.00,
0.00 , -30.62 , 1.50 , 3.54 , 8.00 , 3.00 , 3.50 , 350.00,
0.00 , -72.50 , 3.50 , -27.16 , 15.00 , 7.00 , 72.50 , 15.00,
0.00 , -77.97 , 4.50 , -20.52 , 15.00 , 9.00 , 60.00 , 3.50,
0.00 , -59.38 , 1.50 , 14.64 , 8.00 , 3.00 , 3.50 , 47.00,
0.00 , -74.35 , 1.50 , 18.70 , 8.00 , 3.00 , 3.50 , 6.00,
0.00 , 17.66 , 7.00 , 42.58 , 25.00 , 14.00 , 25.00 , 10.00,
0.00 , 20.14 , 9.00 , 53.77 , 17.00 , 18.00 , 17.00 , 320.00,
0.00 , 13.94 , 10.00 , 57.99 , 13.00 , 20.00 , 20.00 , 10.00,
0.00 , 14.08 , 2.00 , -14.68 , 8.00 , 4.00 , 26.00 , 320.00,
0.00 , 17.76 , 2.50 , -7.19 , 20.00 , 5.00 , 10.00 , 350.00,
0.00 , 22.68 , 3.00 , -14.03 , 11.00 , 6.00 , 19.00 , 10.00,
0.00 , 33.92 , 10.00 , 76.73 , 8.00 , 20.00 , 14.00 , 325.00,
0.00 , 56.81 , 10.00 , 81.53 , 8.00 , 20.00 , 14.00 , 325.00,
0.00 , 45.54 , 8.00 , 79.50 , 22.00 , 16.00 , 11.00 , 350.00,
0.00 , 54.40 , 12.00 , 57.50 , 30.00 , 24.00 , 10.00 , 342.00,
0.00 , 45.30 , 7.00 , 44.30 , 12.00 , 14.00 , 22.00 , 3.00,
0.00 , 69.50 , 4.00 , 52.90 , 9.00 , 8.00 , 22.00 , 330.00,
0.00 , 57.70 , 3.50 , 45.80 , 22.00 , 7.00 , 16.00 , 339.00,
0.00 , 73.42 , 10.00 , -14.82 , 16.00 , 20.00 , 25.00 , 25.00,
0.00 , 63.85 , 7.00 , -6.71 , 10.00 , 14.00 , 16.00 , 20.00,
0.00 , 49.65 , 5.00 , -15.87 , 22.00 , 10.00 , 35.00 , 5.00,
0.00 , 58.75 , 6.00 , -21.44 , 32.00 , 12.00 , 26.00 , 18.00 ], [ 3.00 , 0.00 , 42.00,
15.00 , 0.00 , -1.00 ])
print(testAi.solve([ 25.00 , 0.00 , -27.00 ], [15, 0, -1]))
