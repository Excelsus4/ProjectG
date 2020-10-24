class TestAI():
    def __init__(self, fls, exitP):
        self.fls = fls
        self.exitP = exitP

    def display(self):
        tempTuple = []
        result = []

        for i in range(0, len(self.fls) / 8):
            for j in range(0, 7):
                tempTuple.append(self.fls[i * 8 + j])
            result.append(tempTuple)
        
        #print(result)
        #checkPoint = "check1"

        return result

    def solve(self, a, b):
        result = [0., 0., 0.]

        #for i in range(0, 3):
        #    result[i] = (a[i] + b[i]) / 2
        
        #print(result)
        #checkPoint = "check2"

        return b