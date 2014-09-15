#! python3 ped.py <existing_file>
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
        print("no filename given -- quitting")#creating tmp empty buffer")
        return -1
    if not os.path.exists(filename):
        print("file DNE -- quitting")
        return -1

    # open and read lines into linv; establish linc
    fp = open(filename, "r+")
    for line in fp:
        linv.append(line.rstrip('\n'));
        linc = linc + 1
    fp.close()
    dot = linc

    # our buffer object
    buf = Edbuf(linc, linv)
    print(buf.byte_count())

    # command loop
    while True:
        cmd = input()
        if(len(cmd) == 0): print('?');continue
        # remove all whitespace
        p = re.compile("\s")
        cmd = p.sub("", cmd)
        r = -1

        # find the core command character
        p = re.compile("[a-zA-Z]")
        c = p.findall(cmd)
        core = ''
        if c: core = c[0]

        extra = False
        if len(c) > 1:
            extra = True

        start = dot
        end = dot

        # find line range
        p = re.compile("[0-9]+")
        m = p.findall(cmd)
        if len(m) > 0:
            start = int(m[0])
            if len(m) > 1:
                end = int(m[1])
            else:
                end = start

        # if no core command, select a line
        if not core:
            r = buf.type(end, end, False, False)
        elif core == 'i':
            r = buf.a(start-1)

        elif core == 'a':
            r = buf.a(start)

        elif core == 'd':
            r = buf.d(start, end)

        elif core == 'p' or core == 'n' or core == 'l':
            unamb = False
            if (extra and c[1] == 'l') or core == 'l': unamb = True
            if core == 'p' or core == 'l':
                r = buf.type(start, end, False, unamb)
            elif core == 'n':
                r = buf.type(start, end, True, unamb)
        
        elif core == 'w': # or core == 'W': # write file or append (W)
            mode = "w"
            # if(core == 'W'): mode = "a" #append write

            linv = buf.getlinv()
            with open(filename, mode) as f:
                for l in linv:
                    f.write(l+'\n')
            print(buf.byte_count())
            r = len(linv)
       
        elif core == 'q':
            if modified: # print '?' if changes yet to save
                print('?')
            else:
                break
        else:
            print('?')

        if r < 0: print('?')
        else: dot = r
    #end while

    fp.close();
main();

