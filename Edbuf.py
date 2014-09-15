import re

class Edbuf:
    """Edbuf methods return dot (line index) upon success"""
    def __init__(self, linc, linv):
        self.linc = linc
        self.linv = linv

    def byte_count(self): # const
        bc = 0
        for line in self.linv:
            bc = bc + len(line) + 1 #+1 for \n byte
        return bc

    def getlinv(self): # const
        return self.linv

    def type(self, start, end, numbers=False, unamb=False):
        if start < 1 or end > self.linc or end < start:
            return -1

        for i in range(start-1, end):
            line = self.linv[i]
            if numbers:
                n = str(i+1) + "\t"
            else: n = ''
            if unamb: # replace EOL with '$'
                p = re.compile("$")
                line = p.sub("$", self.linv[i])
            print("{0}{1}".format(n, line))
        return end
        
    def a(self, dot): # const
        if dot < 0 or dot > self.linc+1:
            return -1

        text = input()
        if len(text) > 0:
            self.linv.insert(dot, text)
            self.linc = len(self.linv)
        return dot+1

    def d(self, start, end):
        if start < 1 or end > self.linc or end < start:
            return -1

        for i in range(start-1, end):
            self.linv.pop(i)
            self.linc = self.linc - 1

        return start

