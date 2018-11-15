import sys, re, colorama
colorama.init()

LINE_LENGTH = 50
DEFAULT     = "\033[02;37m"
SEPERATOR   = '\033[01;30m'
FILENAME    = "\033[01;36m"
LINE_NUMBER = "\033[01;32m"
FUNCTION    = "\033[01;34m"


PARTS = re.compile(r'.*File.*/([^/]+\.py)", line ([0-9]+), in (.*)')


class PrettyErrors():
    def out(self, s):
        sys.core_stderr.write(s)

    def write(self, *args):
        for arg in args:
            for line in arg.split("\n"):
                if line .startswith("Traceback"):
                    self.out("\n" + SEPERATOR + LINE_LENGTH * "-" + "\n")
                else:
                    line = line.replace('\\', '/')
                    parts = PARTS.match(line)
                    if parts:
                        self.out("\n")
                        self.out(FILENAME + parts.group(1) + " ")
                        self.out(LINE_NUMBER + parts.group(2) + " ")
                        self.out(FUNCTION + parts.group(3))
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
