#! python3 ped.py <file>
import sys, os, os.path, re, tempfile
from Edbuf import Edbuf

def main():
    # fundamental variables
    linc = 0    # line count
    linv = [ ]  # line vector (array)
    dot  = -1   # current working line aka '.' or "dot" in man pages
    fp = None   # file pointer
    modified = False

    # Validate args
    argc = len(sys.argv)
    filename = sys.argv[argc-1]
    if(filename == sys.argv[0]):
        print("no filename given -- creating tmp empty buffer")
    else:
        # create given filename if not exists
        if not os.path.exists(filename):
            try:
                open(filename, 'w').close();
            except:
                print("Couldn't create new file", filename)
                return -1;

        # open and read lines into linv; establish linc
        fp = open(filename, "r+")
        for line in fp:
            linv.append(line.rstrip('\n'));
            linc = linc + 1
        dot = linc
        fp.close()

    # our buffer object
    buf = Edbuf(linc, linv)

    # command loop
    while True:
        extra = False

        cmd = input()
        # remove all whitespace
        p = re.compile("\s")
        cmd = p.sub("", cmd)

        # find the core command character
        p = re.compile("[a-zA-Z]")
        c = p.findall(cmd)
        core = c[0]

        if len(c) > 1:
            extra = True

        p = re.compile("\d+")
        m = p.findall(cmd)
        print(m)
        dot = 3
        print("dot = ", dot)

        if core == 'i':
            dot = buf.a(dot-1)

        elif core == 'a':
            dot = buf.a(dot)

        elif core == 'd':
            dot = buf.d(start, end)

        elif core == 'n':
            if extra and c[1] == 'l': dot = buf.type(start, end, True, True)
            else: dot = buf.type(start, end, True, False)

        elif core == 'p':
            if extra and c[1] == 'l': dot = buf.type(start, end, False, True)
            else: dot = buf.type(start, end, False, False)

        elif core == 'w' or core == 'W': # write file or append (W)
            mode = "w"
            if(core == 'W'): mode = "a" #append write

            linv = buf.getlinv()
            with open(filename, mode) as f:
                for l in linv:
                    f.write(l+'\n')
       
        elif core == 'q':
            if modified: # print '?' if changes yet to save
                print('?')
            else:
                break
        else:
            print('?')

    fp.close();
main();

