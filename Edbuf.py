import re

class Edbuf:
    """Edbuf methods return new dot (line index) upon success, -1 on error.
        function names of only 1 letter are named after `ed' commands."""
    def __init__(self, linc, linv):
        self.linc = linc
        self.linv = linv
        self.mod = False

    def modified(self): # is buffer modified? ; const
        return self.mod

    def w(self, filename, mode="w"):
        if self.mod:
            with open(filename, mode) as f:
                for l in self.linv:
                    f.write(l+'\n')
            self.mod = False
        return self.linc


    def byte_count(self): # count bytes in file ; const
        bc = 0
        for line in self.linv:
            bc = bc + len(line) + 1 #+1 for \n byte
        return bc

    def getlinv(self): # gett for linv ; const
        return self.linv

    def type(self, start, end, numbers=False, unamb=False): # type text ; const
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
        
    def a(self, dot): # append/insert text
        if dot < 0 or dot > self.linc+1:
            return -1

        text = input()
        if len(text) > 0:
            self.linv.insert(dot, text)
            self.linc = len(self.linv)
            self.mod = True
        return dot+1

    def d(self, start, end): # delete lines
        if start < 1 or end > self.linc or end < start:
            return -1

        for i in range(start-1, end):
            self.linv.pop(i)
            self.linc = self.linc - 1
        self.mod = True
        return start

    def j(self, dot): # join lines
        if dot < 1 or dot > self.linc-1:
            return -1

        self.linv[dot-1] = self.linv[dot-1].rstrip() + self.linv[dot]
        self.linv.pop(dot)
        self.mod = True
        return dot

