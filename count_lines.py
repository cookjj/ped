import sys, re, string

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
    argc = len(sys.argv)
    if(argc < 2):
        print("usage: python3 count_lines.py file1 file2 ...")
        return -1

    total = 0
    for i in range(1, argc):
        filename = sys.argv[i]
        with open(filename, "r") as f:
            for line in f:
                if issourceline(line):
                    total = total + 1
    print("Total source lines:", total)

main();

