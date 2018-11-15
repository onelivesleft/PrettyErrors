name = "pretty_errors"

import sys, re, colorama, os, time
from enum import Enum

colorama.init()


class FilenameDisplayMode(Enum):
    COMPACT  = 0
    EXTENDED = 1
    FULL     = 2


part_expression = re.compile(r'.*File "([^"]*)", line ([0-9]+), in (.*)')


class PrettyErrors():
    def __init__(self):
        self._line_length         = 79
        self._filename_display    = FilenameDisplayMode.COMPACT
        self._full_line_newline   = False
        self._display_timestamp   = False
        self._seperator_character = '-'
        self._seperator_color     = '\033[01;30m'
        self._timestamp_color     = '\033[01;30m'
        self._default_color       = '\033[02;37m'
        self._filename_color      = '\033[01;36m'
        self._line_number_color   = '\033[01;32m'
        self._function_color      = '\033[01;34m'


    def configure(self, line_length = None, filename_display = None, full_line_newline = None, display_timestamp = None,
                  seperator_character = None, seperator_color = None, default_color = None, timestamp_color = None,
                  filename_color = None, line_number_color = None, function_color = None):
        if line_length         is not None: self._line_length         = line_length
        if filename_display    is not None: self._filename_display    = filename_display
        if display_timestamp   is not None: self._display_timestamp   = display_timestamp
        if seperator_character is not None: self._seperator_character = seperator_character
        if seperator_color     is not None: self._seperator_color     = seperator_color
        if default_color       is not None: self._default_color       = default_color
        if timestamp_color     is not None: self._timestamp_color     = timestamp_color
        if filename_color      is not None: self._filename_color      = filename_color
        if line_number_color   is not None: self._line_number_color   = line_number_color
        if function_color      is not None: self._function_color      = function_color


    def out(self, s, wants_newline = False):
        sys.pretty_errors_stderr.write(s)
        if wants_newline and (len(s) < self._line_length or self._full_line_newline):
            sys.pretty_errors_stderr.write('\n')


    def write(self, *args):
        for arg in args:
            for line in arg.split("\n"):
                if line.startswith("Traceback"):
                    if self._display_timestamp:
                        timestamp = str(time.perf_counter())
                        seperator = (self._line_length - len(timestamp)) * self._seperator_character + timestamp
                    else:
                        seperator = self._line_length * self._seperator_character
                    self.out('\n')
                    self.out(self._seperator_color + seperator, wants_newline = True)
                else:
                    line = line.replace('\\', '/')
                    parts = part_expression.match(line)
                    if parts:
                        line_number = parts.group(2) + " "
                        function = parts.group(3)
                        wants_newline = False
                        if self._filename_display == FilenameDisplayMode.FULL:
                            filename = parts.group(1)
                            wants_newline = True
                        elif self._filename_display == FilenameDisplayMode.EXTENDED:
                            filename = parts.group(1)[-(self._line_length - len(line_number) - len(function) - 4):]
                            if filename != parts.group(1): filename = "..." + filename
                            filename += " "
                        else:
                            filename = os.path.basename(parts.group(1)) + " "
                        self.out('\n')
                        self.out(self._filename_color    + filename, wants_newline = wants_newline)
                        self.out(self._line_number_color + line_number)
                        self.out(self._function_color    + function, wants_newline = True)
                    else:
                        self.out(self._default_color)
                        line = line.strip()
                        while len(line) > self._line_length:
                            c = self._line_length - 1
                            while c > 0 and line[c] not in (" ", "\t"):
                                c -= 1
                            if c == 0: c = self._line_length
                            self.out(line[:c], wants_newline = True)
                            line = line[c:].strip()
                        if line:
                            self.out(line, wants_newline = True)


if not getattr(sys, 'pretty_errors_stderr', False):
    sys.pretty_errors_stderr = sys.stderr
    sys.stderr = PrettyErrors()


def configure(line_length = None, filename_display = None, full_line_newline = None, display_timestamp = None,
              seperator_character = None, seperator_color = None, default_color = None, timestamp_color = None,
              filename_color = None, line_number_color = None, function_color = None):
    sys.stderr.configure(line_length, filename_display, full_line_newline, display_timestamp, seperator_character,
                         seperator_color, default_color, timestamp_color, filename_color, line_number_color, function_color)
