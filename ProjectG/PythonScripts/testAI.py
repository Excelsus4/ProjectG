class TestAI():
    def __init__(self, fls):
        self.fls = fls

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


        return 1