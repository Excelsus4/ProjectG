import math
import random
import os

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

        self.makeRTable()

        f = open("5. RTableFile.txt", 'w')
        for i in range(0, 8):
            for j in range(0, int(self.yLength)):
                for k in range(0, int(self.xLength)):
                    for l in range(0, int(self.numGoal)):
                        f.write(str(self.RTable[l][k][j][i]))
            f.write("\n")
        f.close

        self.checkQTableFile()

        self.QLTrain()



    #main activity---------------------------------------------------------------------------------------------------------------
    def solve(self, a, b):
        startPoint = [int(a[0] + self.xLength // 2), int(self.yLength // 2 - a[2])]
        endPoint = [int(b[0] + self.xLength // 2), int(self.yLength // 2 - b[2])]
        endNum = self.findTabel(endPoint)
        result = self.QL(endNum, startPoint)                 
        result = self.skipLoot(result)

        return result
    

    def QLTrain(self):
        #repeat n
        n = 500
        alpha = 0.5
        diWeight = 0.7

        f = open("7. QLTrainCheck.txt", 'w')
        f.write("check open\n")

        for j in range(0, int(len(self.goalList))):
            i = 0
            myPoint = [0, 0]
            

            while i < n:
                myPoint = [int(random.randrange(int(max(5, int(self.goalList[j][0] - 10 - i))), int(min(395, int(self.goalList[j][0] + 10 + i))))), int(random.randrange(int(max(5, int(self.goalList[j][1] - 10 - i))), int(min(395, int(self.goalList[j][1] + 10 + i)))))]
                #if myPoint type is block do again
                while self.mapTable[myPoint[0]][myPoint[1]] == 0 or (int(myPoint[0]) == int(self.goalList[j][0]) and int(myPoint[1]) == int(self.goalList[j][1])):
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
                    
                    if int(self.maxQValue(j, myPoint)) == 0:
                        nextDi = random.randrange(0, 8)
                        nextDi = int(round(nextDi))
                        checkFailStart = 0

                        while self.RTable[j][myPoint[0]][myPoint[1]][nextDi] == -1:
                            nextDi = random.randrange(0, 8)
                            nextDi = int(nextDi)
                            checkFailStart = checkFailStart + 1
                            if checkFailStart > 50:
                                break
                    else:
                        nextDi = int(self.maxQDi(j, myPoint))
                        
                    if checkFailStart > 50:
                        break

                    nextPoint[0], nextPoint[1] = self.nextLoc(myPoint[0], myPoint[1], nextDi)
                    nextPoint[0] = int(nextPoint[0])
                    nextPoint[1] = int(nextPoint[1])
                    
                    #break check code (not need)
                    if int(nextPoint[0]) == int(self.goalList[j][0]) and int(nextPoint[1]) == int(self.goalList[j][1]):
                        break
                    if int(self.RTable[j][myPoint[0]][myPoint[1]][nextDi]) == 1000:
                        break

                    if nextDi == 1 or nextDi == 3 or nextDi == 5 or nextDi == 7:
                        self.QTable[j][myPoint[0]][myPoint[1]][nextDi] = self.RTable[j][myPoint[0]][myPoint[1]][nextDi] + alpha * diWeight * self.maxQValue(j, nextPoint)
                    else:
                        self.QTable[j][myPoint[0]][myPoint[1]][nextDi] = self.RTable[j][myPoint[0]][myPoint[1]][nextDi] + alpha * self.maxQValue(j, nextPoint)

                    myPoint[0] = int(nextPoint[0])
                    myPoint[1] = int(nextPoint[1])

                    if myPoint == firstStartPoint:
                        checkLoop = checkLoop + 1
                    if checkLoop > 100:
                        i = i - 1
                        break
                    #break check code (not need)
                    if myPoint == self.goalList[j]:
                        break
                    
                i = i + 1
        #pass nextpoint
    
        #text check
        #for i in range(0, 8):
        #    for j in range(0, int(self.yLength)):
        #        for k in range(0, int(self.xLength)):
        #            for l in range(0, int(self.numGoal)):
        #                f.write(str(self.QTable[l][k][j][i]))
        #                f.write(" ")
        #            f.write("\n")

        f.write("check close\n")
        f.close()
        self.writeQTableFie()

        return 1
    

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



    #sub activity-----------------------------------------------------------------------------------------------

    def checkQTableFile(self):
        if os.path.isfile('QTableFile.txt'):
            f = open("QTableFile.txt", 'r')
            for i in range(0, 8):
                for j in range(0, int(self.yLength)):
                    for k in range(0, int(self.xLength)):
                        line = f.readline()
                        data = line.split(' ')
                        for l in range(0, int(self.numGoal)):
                            self.QTable[l][k][j][i] = float(data[l])
            f.close
        else:
            for w in range(0, int(len(self.goalList))):
                for i in range(0, int(self.xLength)):
                    for j in range(0, int(self.yLength)):
                        for k in range(0, 8):
                            if self.checkValue(w, i, j, k) != -2:
                                self.QTable[w][i][j][k] = self.checkValue(w, i, j, k)

            self.writeQTableFie()
        

    def writeQTableFie(self):
        f = open("QTableFile.txt", 'w')
        for i in range(0, 8):
            for j in range(0, int(self.yLength)):
                for k in range(0, int(self.xLength)):
                    for l in range(0, int(self.numGoal)):
                        f.write(str(self.QTable[l][k][j][i]))
                        f.write(" ")
                    f.write("\n")
        f.close
        

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


    def makeRTable(self):
        for w in range(0, int(len(self.goalList))):
            for i in range(0, int(self.xLength)):
                for j in range(0, int(self.yLength)):
                    for k in range(0, 8):
                        if self.checkValue(w, i, j, k) != -2:
                            self.RTable[w][i][j][k] = self.checkValue(w, i, j, k)

    
    def skipLoot(self, putList):
        i = 0
        j = 0
        while i < int(len(putList)):
            j = i + 6
            if j >= int(len(putList)):
                break

            checkMapCode = 0
            passForPoint = 0

            #same to x
            if putList[i] == putList[j]:
                x = int(putList[i])
                passForPoint = 1
                for y in range(int(min(putList[i + 2], putList[j + 2])), int(max(putList[i + 2], putList[j + 2]))):
                    if self.mapTable[x][y] == 0:
                        checkMapCode = checkMapCode + 1
        
            #same to y
            elif putList[i + 2] == putList[j + 2]:
                y = int(putList[i + 2])
                passForPoint = 1
                for x in range(int(min(putList[i], putList[j])), int(max(putList[i], putList[j]))):
                    if self.mapTable[x][y] == 0:
                        checkMapCode = checkMapCode + 1
                
            #not same
            elif putList[i] < putList[j]:
                startX = putList[i]
                startY = putList[i + 2]
                endX = putList[j]
                endY = putList[j + 2]
            else:
                startX = putList[j]
                startY = putList[j + 2]
                endX = putList[i]
                endY = putList[i + 2]
            delta = (endY - startY) / (endX - startX)

            if passForPoint == 0:
                for x in range(int(startX), int(endX)):
                    if delta > 0:
                        pointS = int(math.floor(startY + delta * (x - startX)))
                        pointE = int(math.ceil(startY + delta * (x + 1 - startX)))
                        for y in range(pointS, pointE + 1):
                            if self.mapTable[x][y] == 0:
                                checkMapCode = checkMapCode + 1
                    else:
                        pointS = int(math.floor(startY + delta * (x - startX)))
                        pointE = int(math.ceil(startY + delta * (x + 1 - startX)))
                        for y in range(pointS, pointE + 1, -1):
                            if self.mapTable[x][y] == 0:
                                checkMapCode = checkMapCode + 1

            if checkMapCode == 0:
                del putList[3:6]
            else:
                i = i + 3
    
        return putList
            
        


    #calculation----------------------------------------------------------------------------------------------------

    def findTabel(self, endPoint):
        temp = 0
        for i in range(0, int(len(self.goalList))):
            if int(self.goalList[i][0]) == int(endPoint[0]) or int(self.goalList[i][1]) == int(endPoint[1]):
                temp = i
                break
        return temp


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
        x = int(x)
        y = int(y)
        
        if x == int(self.goalList[goalNum][0]) and y == int(self.goalList[goalNum][1]):
            return 1000

        if x < 0 or y < 0 or x >= self.xLength or y >= self.yLength:
            return -2
        elif int(self.mapTable[x][y]) == 0:
            return -1
        elif int(self.mapTable[x][y]) == 1 or int(self.mapTable[x][y]) == 2:
            return 0
        
        return 0


    def maxQValue(self, tableNum, myState):
        maxValue = 0

        for i in range(0, 8):
            if self.QTable[tableNum][myState[0]][myState[1]][i] > maxValue:
                maxValue = self.QTable[tableNum][myState[0]][myState[1]][i]
        return maxValue


    def maxQDi(self, tableNum, myState):
        maxValue = 0
        maxDi = 0
        canMoveDi = []

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

        return maxDi


    #point pass def
    def passPoint(self):
        pass
