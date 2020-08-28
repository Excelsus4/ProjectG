class Test():
    def __init__(self, fls):
        self.fls = fls

    def display(self):
        ret = 0.
        for f in self.fls:
            ret= ret + f;
        return ret