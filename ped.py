#! python3 ped.py <existing_file>
# ped -- by Jeffrey Cook.
# ped implements a subset of the standard UNIX editor, `ed'.
# please see the man pages to learn the command syntax:
#     http://man.cat-v.org/unix_8th/1/ed
#
# In `ped', the usual basic line and range selection is supported and
# dot is remembered properly. The commands a, i, j, p, d, n, l, and w
# are supported. An existing filename must be passed to ped.py to edit,
# and only 'w' (overwrite) is supported, not 'W' (append).

import sys, os, os.path, re
from Edbuf import Edbuf

def main():
    # fundamental variables
    linc = 0    # line count
    linv = [ ]  # line vector (array)
    dot  = -1   # current working line aka '.' or "dot" in man pages
    modified = False

    # Validate args
    argc = len(sys.argv)
    filename = sys.argv[argc-1]
    if(filename == sys.argv[0]):
        print("no filename given -- quitting")
        return -1
    if not os.path.exists(filename):
        print("file DNE -- quitting")
        return -1

    with open(filename, "r+") as fp: # open and read lines into linv; establish linc
        for line in fp:
            linv.append(line.rstrip('\n'));
            linc = linc + 1
    dot = linc

    buf = Edbuf(linc, linv) # our buffer object
    print(buf.byte_count()) # standard behaviour

    while True: # command loop
        cmd = input()
        if(len(cmd) == 0): print('?');continue
        p = re.compile("\s") # remove all whitespace
        cmd = p.sub("", cmd)
        r = -1

        p = re.compile("[a-zA-Z]") # find the core command character
        c = p.findall(cmd)
        core = ''
        if c: core = c[0]

        extra = False # some commands like 'n' can be followed by an
        if len(c) > 1:# extra command char, such as 'l'
            extra = True

        start = dot
        end = dot

        p = re.compile("[0-9]+") # find line range
        m = p.findall(cmd)
        if len(m) > 0:
            start = int(m[0])
            if len(m) > 1:
                end = int(m[1])
            else:
                end = start

        if not core: # if no core command, just print dot line
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
        
        elif core == 'w':
            r = buf.w(filename, "w")
            print(buf.byte_count())

        elif core == 'j':
            r = buf.j(start)

        elif core == 'q':
            if buf.modified(): # print '?' if changes yet to save
                print('? (unsaved buffer modified)')
            else:
                break
        else:
            print('?')

        if r < 0: print('?') # print '?' on any error condition
        else: dot = r        # otherwise use returned dot from method call
    #end while
main();

