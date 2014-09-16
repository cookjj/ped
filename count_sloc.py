import sys, re, string, os

def issourceline(line):
    """identifies if a line has only comment content or is whitespace"""
    """currently does not support sensing triple-quote comments like this"""

    # 1) Check for whitespace only lines
    p = re.compile('\s')
    line = p.sub("", line)
    if(len(line) == 0): # line is only whitespace
        return False # i.e., is not a source line

    # 2) Check for strpos of '#' after whitespace-stripping.
    idx = line.find("#")
    if(idx == 0): # It is pos 0 if no source code before hash char
        return False
    else:
        return True # otherwise is source line


def main():
    total = 0
    for file in os.listdir("."): 
        if not ".py" in file: continue;
        f = open(file, "r")
        if file == sys.argv[0]:
            continue
        for line in f:
            if issourceline(line):
                total = total + 1
        f.close()
    print("Total source lines:", total)

main();

