# Version 1.1

import sys, re, colorama, os
colorama.init()


# Mode select values for FILENAME_DISPLAY
COMPACT  = 0
EXTENDED = 1
FULL     = 2


# Control variables; change to suit your preference
LINE_LENGTH = 50
FILENAME_DISPLAY = COMPACT
DEFAULT     = "\033[02;37m"
SEPERATOR   = '\033[01;30m'
FILENAME    = "\033[01;36m"
LINE_NUMBER = "\033[01;32m"
FUNCTION    = "\033[01;34m"


PARTS = re.compile(r'.*File "(.*\.py)", line ([0-9]+), in (.*)')


class PrettyErrors():
    def out(self, s):
        sys.core_stderr.write(s)

    def write(self, *args):
        for arg in args:
            for line in arg.split("\n"):
                if line.startswith("Traceback"):
                    self.out("\n" + SEPERATOR + LINE_LENGTH * "-" + "\n")
                else:
                    line = line.replace('\\', '/')
                    parts = PARTS.match(line)
                    if parts:
                        line_number = parts.group(2) + " "
                        function = parts.group(3)
                        if FILENAME_DISPLAY == FULL:
                            filename = parts.group(1) + "\n"
                        elif FILENAME_DISPLAY == EXTENDED:
                            filename = parts.group(1)[-(LINE_LENGTH - len(line_number) - len(function) - 4):]
                            if filename != parts.group(1): filename = "..." + filename
                            filename += " "
                        else:
                            filename = os.path.basename(parts.group(1)) + " "
                        self.out("\n")
                        self.out(FILENAME + filename)
                        self.out(LINE_NUMBER + line_number)
                        self.out(FUNCTION + function)
                    else:
                        self.out(DEFAULT)
                        line.strip()
                        while len(line) > LINE_LENGTH:
                            c = LINE_LENGTH
                            while c > 0 and line[c] not in (" ", "\t"):
                                c -= 1
                            if c == 0: c = LINE_LENGTH
                            self.out(line[:c] + "\n")
                            line = line[c:].strip()
                        if line:
                            self.out(line + "\n")


try:
    t = sys.core_stderr
except AttributeError:
    sys.core_stderr = sys.stderr
    sys.stderr = PrettyErrors()
