import math
import random


def turn(typeCode, pointX, pointZ, sizeX, sizeZ, seta):
    pointList = []

    for i in range(round(-1 * sizeX/2), round(sizeX/2 + 1)):
        for j in range(round(-1 * sizeZ/2), round(sizeZ/2 + 1)):
            x = i * math.cos(seta) - j * math.sin(seta)
            x = round(x) + pointX
            z = i * math.sin(seta) + j * math.cos(seta)
            z = round(z) + pointZ
            pointList.append([x, z])
    
    return pointList

def makeTable():
    pass

def maxQValue():
    pass

def passPoint():
    pass

#Tabel
#QTable[1~x][0~1500][0~1500][0~1500][0~1500]
#RTable[0~1500][0~1500][0~1500][0~1500]


def QLTrain():
    #반복횟수 n
    n = 1000
    #목표지점
    goal = [(5, 5), (5, 1495)]

    for j in range(1, len(goal)):
        for i in range(1, n):
            myPoint = (random.randrange(5, 1500), random.randrange(5, 1500))
            while myPoint == goal[j]:
                nextPoint = (random.randrange(5, 1500), random.randrange(5, 1500))
                while RTable[myPoint[0]][myPoint[1]][nextPoint[0]][nextPoint[1]] is not -1:
                    nextPoint = (random.randrange(5, 1500), random.randrange(5, 1500))
                QTable[j][myPoint[0]][myPoint[1]][nextPoint[0]][nextPoint[1]] = 
                    RTable[myPoint[0]][myPoint[1]][nextPoint[0]][nextPoint[1]] +
                    alpha * max()#max(Q(next state, all actions))
                myPoint = nextPoint
                #다음포인트 전송

    return 1
    #state

def QL(myPoint):
    while myPoint == goal[j]:
        nextPoint = max()#max(Q(next state, all actions))
        myPoint = nextPoint
        #다음 포인트 전송


def main():
    print(turn(0, -84.79, -5.93, 6.00, 160.00, 356.00))
    #print(takeSeta(0, 0, 1, 1))
    print("check")
    pass
    
if __name__ == "__main__":
    main()