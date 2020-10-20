import math
import random
import numpy as np

numGoal = 2
mapTable = np.zeros((1500,1500))
QTable = np.zeros((numGoal, 1500, 1500, 8))
RTable = np.zeros((numGoal, 1500, 1500, 8))
goalList = [(5, 5), (5, 1495)]

#[ 0.00 , -84.79 , 3.00 , -5.93 , 6.00 , 6.00 , 160.00 , 356.00]
#타입코드, 중심점(3차원플롯벡터), 크기(3차원플롯벡터), 회전(플롯)
#타입코드 0(벽), 1(인도), 2(횡단보도)

def turn(typeCode, pointX, pointZ, sizeX, sizeZ, seta):
    pointList = []

    for i in range(round(-1 * sizeX/2), round(sizeX/2 + 1)):
        for j in range(round(-1 * sizeZ/2), round(sizeZ/2 + 1)):
            x = i * math.cos(seta) - j * math.sin(seta)
            x = round(x + pointX)
            z = i * math.sin(seta) + j * math.cos(seta)
            z = round(z + pointZ)
            pointList.append([x, z])
    
    return pointList

def putGoal():
    global goalList
    global numGoal

    numGoal = input("number of Goal : ")
    for i in range(0, numGoal):
        x = input("x location : ")
        z = input("z location : ")
        goalList.append((x, z))


def makeMap(putList):
    global mapTable

    for i in range(0, len(putList) / 8):
        typeCode = putList[i * 8]
        pointX = putList[i * 8 + 1]
        pointY = putList[i * 8 + 3]
        sizeX = putList[i * 8 + 4]
        sizeZ = putList[i * 8 + 6]
        seta = putList[i * 8 + 7]

        #turn & put map
        for j in range(round(-1 * sizeX/2), round(sizeX/2 + 1)):
            for k in range(round(-1 * sizeZ/2), round(sizeZ/2 + 1)):
                x = j * math.cos(seta) - k * math.sin(seta)
                x = round(x + pointX)
                z = j * math.sin(seta) + k * math.cos(seta)
                z = round(z + pointZ)
                mapTable[x][z] = typeCode

# 7 0 1
# 6 * 2
# 5 4 3

def nextLoc(pointX, pointY, di):
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

    return (x, y)


def checkValue(goalNum, pointX, pointY, di):
    global mapTable
    global goalList

    (x, y) = nextLoc(pointX, pointY, di)
    
    if (x,y) is goalList[goalNum]:
        return 1000

    if x < 0 or y < 0 or x > 1500 or y > 1500:
        return -2
    elif mapTable[x][y] == 0:
        return -1
    elif mapTable[x][y] == 1 or mapTable[x][y] == 2:
        return 0
    
    return 0


def makeTable():
    global mapTable
    global numGoal
    global QTable
    global RTable
    global goalList

    for w in range(0, len(goalList)):
        for i in range(0, 1500):
            for j in range(0, 1500):
                for k in range(0, 8):
                    if checkValue(i, j, k) is not -2:
                        RTable[w][i][j][k] = checkValue(w, i, j, k)

    QTable = RTable



def maxQValue(tableNum, nextState):
    global QTable

    maxValue = 0

    for i in range(0, 8):
        if QTable[tableNum][nextState[0]][nextState[1]][i] > maxValue:
            maxValue = QTable[tableNum][nextState[0]][nextState[1]][i]
    return maxValue

def maxQDi(tableNum, myState):
    global QTable

    maxValue = 0
    maxDi = 0

    for i in range(0, 8):
        if QTable[tableNum][myState[0]][myState[1]][i] > maxValue:
            maxValue = QTable[tableNum][myState[0]][myState[1]][i]
            maxDi = i
    return maxDi

#포인트전송 함수
def passPoint():
    pass


def QLTrain():
    global numGoal
    global QTable
    global RTable
    global goalList
    #반복횟수 n
    n = 1000

    for j in range(1, len(goalList)):
        for i in range(1, n):
            myPoint = (random.randrange(5, 1500), random.randrange(5, 1500))
            while myPoint == goalList[j]:
                nextPoint = random.randrange(0, 8)
                while RTable[j][myPoint[0]][myPoint[1]][nextPoint] is not -1:
                    nextPoint = random.randrange(0, 8)
                nextState = nextLoc(myPoint[0], myPoint[1], nextPoint)
                
                QTable[j][myPoint[0]][myPoint[1]][nextPoint] = 
                    RTable[j][myPoint[0]][myPoint[1]][nextPoint] +
                    alpha * maxQValue(j, nextState)
                myPoint = nextPoint
                #다음포인트 전송

    return 1
    #state

def QL(tableNum, myPoint):
    global QTable
    global goalList

    while myPoint == goalList[tableNum]:
        nextDi = maxQDi(tableNum, myPoint)
        nextPoint = nextLoc(myPoint[0], myPoint[1], nextDi)
        myPoint = nextPoint
        #다음 포인트 전송


def main():
    #print(turn(0, -84.79, -5.93, 6.00, 160.00, 356.00))
    #print(takeSeta(0, 0, 1, 1))
    print("check")
    pass
    
if __name__ == "__main__":
    main()