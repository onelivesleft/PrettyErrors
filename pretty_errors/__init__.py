name = "pretty_errors"

import sys, re, colorama, os, time

colorama.init()


FILENAME_COMPACT  = 0
FILENAME_EXTENDED = 1
FILENAME_FULL     = 2

location_expression = re.compile(r'.*File "([^"]*)", line ([0-9]+), in (.*)')
reset_color = '\033[m'

class PrettyErrors():
    def __init__(self):
        self.line_length         = 79
        self.full_line_newline   = True
        self.filename_display    = FILENAME_COMPACT
        self.display_timestamp   = False
        self.seperator_character = '-'
        self.header_color        = '\033[1;30m'
        self.timestamp_color     = '\033[1;30m'
        self.default_color       = '\033[2;37m'
        self.filename_color      = '\033[1;36m'
        self.line_number_color   = '\033[1;32m'
        self.function_color      = '\033[1;34m'
        self.reset_stdout        = False


    def configure(self, **kwargs):
        """Used to configure settings governing how exceptions are displayed."""
        for setting in kwargs:
            if kwargs[setting] is not None: setattr(self, setting, kwargs[setting])


    def write(self, *args):
        """Replaces sys.stderr.write, outputing pretty errors."""
        for arg in args:
            for line in arg.split('\n'):
                if self.is_header(line):
                    self.write_header()
                else:
                    location = self.get_location(line)
                    if location:
                        path, line_number, function = location
                        self.write_location(path, line_number, function)
                    else:
                        self.write_body(line)
        sys.pretty_errors_stderr.write(reset_color)
        if self.reset_stdout:
            sys.stdout.write(reset_color)


    def write_header(self):
        """Writes a header at the start of a traceback"""
        if self.display_timestamp:
            timestamp = self.timestamp()
            seperator = (self.line_length - len(timestamp)) * self.seperator_character + timestamp
        else:
            seperator = self.line_length * self.seperator_character
        self.output_text('\n')
        self.output_text([self.header_color, seperator], newline = True)


    def write_location(self, path, line_number, function):
        """Writes location of exception: file, line number and function"""
        line_number += " "
        self.output_text('\n')
        if self.filename_display == FILENAME_FULL:
            filename = ""
            self.output_text([self.filename_color, path], newline = True)
            self.output_text([self.line_number_color, line_number, self.function_color, function], newline = True)
        else:
            if self.filename_display == FILENAME_EXTENDED:
                filename = path[-(self.line_length - len(line_number) - len(function) - 4):]
                if filename != path:
                    filename = '...' + filename
                filename += " "
            else:
                filename = os.path.basename(path) + " "
            self.output_text([self.filename_color,    filename,
                              self.line_number_color, line_number,
                              self.function_color,    function
                             ], newline = True)


    def write_body(self, body):
        """Writes any text other than location identifier or traceback header."""
        self.output_text(self.default_color)
        body = body.strip()
        while len(body) > self.line_length:
            c = self.line_length - 1
            while c > 0 and body[c] not in (" ", "\t"):
                c -= 1
            if c == 0: c = self.line_length
            self.output_text(body[:c], newline = True)
            body = body[c:].strip()
        if body:
            self.output_text(body, newline = True)


    def output_text(self, texts, newline = False):
        """Helper function to output text while trying to only insert 1 newline when outputing a line of maximum length."""
        if not isinstance(texts, (list, tuple)):
            texts = [texts]
        count = 0
        for text in texts:
            sys.pretty_errors_stderr.write(text)
            if not text.startswith('\033'):
                count += len(text)
        if newline and (count == 0 or count % self.line_length or self.full_line_newline):
            sys.pretty_errors_stderr.write('\n')


    def get_location(self, text):
        """Helper function to extract location of exception.  If it returns None then text was not a location identifier."""
        location = location_expression.match(text)
        if location:
            return (location.group(1), location.group(2), location.group(3))
        else:
            return None


    def is_header(self, text):
        """Returns True if text is a traceback header."""
        return text.startswith('Traceback')


    def timestamp(self):
        return str(time.perf_counter())


if not getattr(sys, 'pretty_errors_stderr', False):
    sys.pretty_errors_stderr = sys.stderr
    sys.stderr = PrettyErrors()


def configure(line_length = None, filename_display = None, full_line_newline = None, display_timestamp = None,
              seperator_character = None, header_color = None, default_color = None, timestamp_color = None,
              filename_color = None, line_number_color = None, function_color = None, reset_stdout = None):
    """Used to configure settings governing how exceptions are displayed."""
    sys.stderr.configure(
        line_length         = line_length,
        filename_display    = filename_display,
        full_line_newline   = full_line_newline,
        display_timestamp   = display_timestamp,
        seperator_character = seperator_character,
        header_color        = header_color,
        default_color       = default_color,
        timestamp_color     = timestamp_color,
        filename_color      = filename_color,
        line_number_color   = line_number_color,
        function_color      = function_color,
        reset_stdout        = reset_stdout
    )
