import re

class Edbuf:
    """Edbuf methods return dot (line index) upon success"""
    def __init__(self, linc, linv):
        self.linc = linc
        self.linv = linv

    def byte_count():
        bc = 0
        for line in linv:
            bc = bc + len(line)
        return bc

    def type(self, start, end, numbers=False, unamb=False):
        if start < 1 or end > self.linc or end < start:
            return False
        for i in range(start-1, end):
            line = self.linv[i]
            if numbers:
                n = str(i+1) + "\t"
            else: n = ''
            if unamb:
                p = re.compile("\s$")
                line = p.sub("$\n", self.linv[i])
            print("{0}{1}".format(n, line), end='')
        return end
        
    def a(self, dot): # const
        if dot < 0 or dot > self.linc+1:
            print("out of bounds")
            return -1

        text = input() + '\n'
        if len(text) > 0:
            self.linv.insert(dot, text)
            self.linc = len(self.linv)
        lastline = dot # TODO
        return lastline

    def d(self, dot):
        if dot < 1 or dot > self.linc:
            return [dot, False]

        self.linv.pop(dot-1)
        self.linc = self.linc - 1
        if dot > self.linc: # if we removed the last line, make dot
            dot = self.linc # the new last line
        return [dot, True]

