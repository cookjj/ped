#! python3 ped.py <existing_file>
# ped -- by Jeffrey Cook.
# ped implements a subset of the _standard_ UNIX editor, `ed'.
# please see the man pages to learn about the command syntax:
#     http://man.cat-v.org/unix_8th/1/ed
#
# In `ped', the usual basic line and range selection by numbers is supported
# and dot (current line) is remembered properly.
# Support for '$', '%' and '.' implemented, but not other special indices.
# The commands a, i, j, p, d, n, l, and w are supported.
# An existing filename must be passed to ped.py to edit,
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
    if(filename == sys.argv[0]) or not os.path.exists(filename):
        print("no filename given or file DNE -- quitting")
        return -1

    with open(filename, "r+") as fp: # read lines into linv; establish linc
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

        p = re.compile("%"); m = p.findall(cmd) # all lines wildcard '%'
        if len(m) > 0: start=1; end=len(buf.getlinv())
        p = re.compile(r"\$"); m = p.findall(cmd) # last line '$'
        if len(m) > 0: end = len(buf.getlinv())

        if not core: # if no core command, just print the dot line
            r = buf.type(end, end, False, False)

        elif core == 'a' or core == 'i':
            if core == 'i': start = start-1
            r = buf.a(start)

        elif core == 'd':
            r = buf.d(start, end)

        elif core == 'p' or core == 'n' or core == 'l': #printing commands
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
            if not extra and buf.modified(): # print '?' if changes yet to save
                print('? (unsaved buffer modified. Use qq to leave anyway)')
                r = dot
            elif extra and buf.modified():
                if(c[1] == 'q'): break;
            else: break

        else: print('?')

        if r < 0: print('?') # print '?' on any error condition
        else: dot = r        # otherwise use returned dot from method call
    #end while
main();

