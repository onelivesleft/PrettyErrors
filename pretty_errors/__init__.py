import sys, re, colorama, os, time, linecache
colorama.init()
output_stderr = sys.stderr
terminal_is_interactive = sys.stderr.isatty()

name = "pretty_errors"
__version__ = "1.2.19"  # remember to update version in setup.py!

active = 'PYTHON_PRETTY_ERRORS' not in os.environ or os.environ['PYTHON_PRETTY_ERRORS'] != '0'
interactive_tty_only = 'PYTHON_PRETTY_ERRORS_ISATTY_ONLY' in os.environ and os.environ['PYTHON_PRETTY_ERRORS_ISATTY_ONLY'] != '0'


FILENAME_COMPACT  = 0
FILENAME_EXTENDED = 1
FILENAME_FULL     = 2

RESET_COLOR = '\033[m'

BLACK   = '\033[0;30m'
RED     = '\033[0;31m'
GREEN   = '\033[0;32m'
YELLOW  = '\033[0;33m'
BLUE    = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN    = '\033[0;36m'
WHITE   = '\033[0;37m'

BRIGHT_BLACK   = GREY = '\033[1;30m'
BRIGHT_RED     = '\033[1;31m'
BRIGHT_GREEN   = '\033[1;32m'
BRIGHT_YELLOW  = '\033[1;33m'
BRIGHT_BLUE    = '\033[1;34m'
BRIGHT_MAGENTA = '\033[1;35m'
BRIGHT_CYAN    = '\033[1;36m'
BRIGHT_WHITE   = '\033[1;37m'

BLACK_BACKGROUND   = '\033[40m'
RED_BACKGROUND     = '\033[41m'
GREEN_BACKGROUND   = '\033[42m'
YELLOW_BACKGROUND  = '\033[43m'
BLUE_BACKGROUND    = '\033[44m'
MAGENTA_BACKGROUND = '\033[45m'
CYAN_BACKGROUND    = '\033[46m'
WHITE_BACKGROUND   = '\033[47m'


ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
whitelist_paths = []
blacklist_paths = []
config_paths = {}


class PrettyErrorsConfig():
    def __init__(self, instance = None):
        if instance is None:
            self.name                      = "default"
            self.line_length               = 0
            self.full_line_newline         = False
            self.filename_display          = FILENAME_COMPACT
            self.display_timestamp         = False
            try:
                self.timestamp_function    = time.perf_counter
            except AttributeError:
                self.timestamp_function    = time.time
            self.display_link              = False
            self.separator_character       = '-'
            self.line_number_first         = False
            self.top_first                 = False
            self.always_display_bottom     = True
            self.stack_depth               = 0
            self.exception_above           = False
            self.exception_below           = True
            self.trace_lines_before        = 0
            self.trace_lines_after         = 0
            self.lines_before              = 0
            self.lines_after               = 0
            self.display_locals            = False
            self.display_trace_locals      = False
            self.truncate_locals           = True
            self.truncate_code             = False
            self.display_arrow             = True
            self.arrow_tail_character      = '-'
            self.arrow_head_character      = '^'
            self.header_color              = GREY
            self.timestamp_color           = GREY
            self.line_color                = BRIGHT_WHITE
            self.code_color                = GREY
            self.filename_color            = BRIGHT_CYAN
            self.line_number_color         = BRIGHT_GREEN
            self.function_color            = BRIGHT_BLUE
            self.link_color                = GREY
            self.local_name_color          = BRIGHT_MAGENTA
            self.local_value_color         = RESET_COLOR
            self.local_len_color           = GREY
            self.exception_color           = BRIGHT_RED
            self.exception_arg_color       = BRIGHT_YELLOW
            self.exception_file_color      = BRIGHT_MAGENTA
            self.syntax_error_color        = BRIGHT_GREEN
            self.arrow_tail_color          = BRIGHT_GREEN
            self.arrow_head_color          = BRIGHT_GREEN
            self.inner_exception_message   = None
            self.inner_exception_separator = False
            self.prefix                    = None
            self.infix                     = None
            self.postfix                   = None
            self.reset_stdout              = False
            self.show_suppressed           = False
        else:
            self.name                      = instance.name
            self.line_length               = instance.line_length
            self.full_line_newline         = instance.full_line_newline
            self.filename_display          = instance.filename_display
            self.display_timestamp         = instance.display_timestamp
            self.timestamp_function        = instance.timestamp_function
            self.display_link              = instance.display_link
            self.separator_character       = instance.separator_character
            self.line_number_first         = instance.line_number_first
            self.top_first                 = instance.top_first
            self.always_display_bottom     = instance.always_display_bottom
            self.stack_depth               = instance.stack_depth
            self.exception_above           = instance.exception_above
            self.exception_below           = instance.exception_below
            self.trace_lines_before        = instance.trace_lines_before
            self.trace_lines_after         = instance.trace_lines_after
            self.lines_before              = instance.lines_before
            self.lines_after               = instance.lines_after
            self.display_locals            = instance.display_locals
            self.display_trace_locals      = instance.display_trace_locals
            self.truncate_locals           = instance.truncate_locals
            self.truncate_code             = instance.truncate_code
            self.display_arrow             = instance.display_arrow
            self.arrow_tail_character      = instance.arrow_tail_character
            self.arrow_head_character      = instance.arrow_head_character
            self.header_color              = instance.header_color
            self.timestamp_color           = instance.timestamp_color
            self.line_color                = instance.line_color
            self.code_color                = instance.code_color
            self.filename_color            = instance.filename_color
            self.line_number_color         = instance.line_number_color
            self.function_color            = instance.function_color
            self.link_color                = instance.link_color
            self.local_name_color          = instance.local_name_color
            self.local_value_color         = instance.local_value_color
            self.local_len_color           = instance.local_len_color
            self.exception_color           = instance.exception_color
            self.exception_arg_color       = instance.exception_arg_color
            self.exception_file_color      = instance.exception_file_color
            self.syntax_error_color        = instance.syntax_error_color
            self.arrow_tail_color          = instance.arrow_tail_color
            self.arrow_head_color          = instance.arrow_head_color
            self.inner_exception_message   = instance.inner_exception_message
            self.inner_exception_separator = instance.inner_exception_separator
            self.prefix                    = instance.prefix
            self.infix                     = instance.infix
            self.postfix                   = instance.postfix
            self.reset_stdout              = instance.reset_stdout
            self.show_suppressed           = instance.show_suppressed


    def configure(self, **kwargs):
        """Configure settings governing how exceptions are displayed."""
        for setting in kwargs:
            if kwargs[setting] is not None: setattr(self, setting, kwargs[setting])


    def copy(self):
        c = PrettyErrorsConfig()
        c.name                      = self.name
        c.line_length               = self.line_length
        c.full_line_newline         = self.full_line_newline
        c.filename_display          = self.filename_display
        c.display_timestamp         = self.display_timestamp
        c.timestamp_function        = self.timestamp_function
        c.display_link              = self.display_link
        c.separator_character       = self.separator_character
        c.line_number_first         = self.line_number_first
        c.top_first                 = self.top_first
        c.always_display_bottom     = self.always_display_bottom
        c.stack_depth               = self.stack_depth
        c.exception_above           = self.exception_above
        c.exception_below           = self.exception_below
        c.trace_lines_before        = self.trace_lines_before
        c.trace_lines_after         = self.trace_lines_after
        c.lines_before              = self.lines_before
        c.lines_after               = self.lines_after
        c.display_locals            = self.display_locals
        c.display_trace_locals      = self.display_trace_locals
        c.truncate_locals           = self.truncate_locals
        c.truncate_code             = self.truncate_code
        c.display_arrow             = self.display_arrow
        c.arrow_tail_character      = self.arrow_tail_character
        c.arrow_head_character      = self.arrow_head_character
        c.header_color              = self.header_color
        c.timestamp_color           = self.timestamp_color
        c.line_color                = self.line_color
        c.code_color                = self.code_color
        c.filename_color            = self.filename_color
        c.line_number_color         = self.line_number_color
        c.function_color            = self.function_color
        c.link_color                = self.link_color
        c.local_name_color          = self.local_name_color
        c.local_value_color         = self.local_value_color
        c.local_len_color           = self.local_len_color
        c.exception_color           = self.exception_color
        c.exception_arg_color       = self.exception_arg_color
        c.exception_file_color       = self.exception_file_color
        c.syntax_error_color        = self.syntax_error_color
        c.arrow_tail_color          = self.arrow_tail_color
        c.arrow_head_color          = self.arrow_head_color
        c.inner_exception_message   = self.inner_exception_message
        c.inner_exception_separator = self.inner_exception_separator
        c.prefix                    = self.prefix
        c.infix                     = self.infix
        c.postfix                   = self.postfix
        c.reset_stdout              = self.reset_stdout
        c.show_suppressed           = self.show_suppressed
        return c

    __copy__ = copy


config = PrettyErrorsConfig()
default_config = PrettyErrorsConfig()


def configure(
        always_display_bottom     = None,
        arrow_head_character      = None,
        arrow_tail_character      = None,
        arrow_head_color          = None,
        arrow_tail_color          = None,
        code_color                = None,
        display_arrow             = None,
        display_link              = None,
        display_locals            = None,
        display_timestamp         = None,
        display_trace_locals      = None,
        exception_above           = None,
        exception_arg_color       = None,
        exception_below           = None,
        exception_color           = None,
        exception_file_color      = None,
        filename_color            = None,
        filename_display          = None,
        full_line_newline         = None,
        function_color            = None,
        header_color              = None,
        infix                     = None,
        inner_exception_message   = None,
        inner_exception_separator = None,
        line_color                = None,
        line_length               = None,
        line_number_color         = None,
        line_number_first         = None,
        lines_after               = None,
        lines_before              = None,
        link_color                = None,
        local_len_color           = None,
        local_name_color          = None,
        local_value_color         = None,
        name                      = None,
        postfix                   = None,
        prefix                    = None,
        reset_stdout              = None,
        separator_character       = None,
        show_suppressed           = None,
        stack_depth               = None,
        syntax_error_color        = None,
        timestamp_color           = None,
        timestamp_function        = None,
        top_first                 = None,
        trace_lines_after         = None,
        trace_lines_before        = None,
        truncate_code             = None,
        truncate_locals           = None
        ):
    """Configure settings governing how exceptions are displayed."""
    config.configure(
        always_display_bottom     = always_display_bottom,
        arrow_head_character      = arrow_head_character,
        arrow_tail_character      = arrow_tail_character,
        arrow_head_color          = arrow_head_color,
        arrow_tail_color          = arrow_tail_color,
        code_color                = code_color,
        display_arrow             = display_arrow,
        display_link              = display_link,
        display_locals            = display_locals,
        display_timestamp         = display_timestamp,
        display_trace_locals      = display_trace_locals,
        exception_above           = exception_above,
        exception_arg_color       = exception_arg_color,
        exception_below           = exception_below,
        exception_color           = exception_color,
        exception_file_color      = exception_file_color,
        filename_color            = filename_color,
        filename_display          = filename_display,
        full_line_newline         = full_line_newline,
        function_color            = function_color,
        header_color              = header_color,
        infix                     = infix,
        inner_exception_message   = inner_exception_message,
        inner_exception_separator = inner_exception_separator,
        line_color                = line_color,
        line_length               = line_length,
        line_number_color         = line_number_color,
        line_number_first         = line_number_first,
        lines_after               = lines_after,
        lines_before              = lines_before,
        link_color                = link_color,
        local_len_color           = local_len_color,
        local_name_color          = local_name_color,
        local_value_color         = local_value_color,
        name                      = name,
        postfix                   = postfix,
        prefix                    = prefix,
        reset_stdout              = reset_stdout,
        separator_character       = separator_character,
        show_suppressed           = show_suppressed,
        stack_depth               = stack_depth,
        syntax_error_color        = syntax_error_color,
        timestamp_color           = timestamp_color,
        timestamp_function        = timestamp_function,
        top_first                 = top_first,
        trace_lines_after         = trace_lines_after,
        trace_lines_before        = trace_lines_before,
        truncate_code             = truncate_code,
        truncate_locals           = truncate_locals
    )


def mono():
    global RESET_COLOR
    RESET_COLOR = ''
    configure(
        name                 = "mono",
        infix                = '\n---\n',
        line_number_first    = True,
        code_color           = '| ',
        exception_arg_color  = '',
        exception_color      = '',
        exception_file_color = '',
        filename_color       = '',
        function_color       = '',
        header_color         = '',
        line_color           = '> ',
        line_number_color    = '',
        link_color           = '',
        local_len_color      = '',
        local_name_color     = '= ',
        local_value_color    = '',
        timestamp_color      = '',
        arrow_head_color     = '',
        arrow_tail_color     = '',
        syntax_error_color   = ''
    )


def whitelist(*paths):
    """If the whitelist has any entries, then only files which begin with
    one of its entries will be included in the stack trace.
    """
    for path in paths:
        whitelist_paths.append(os.path.normpath(path).lower())


def blacklist(*paths):
    """Files which begin with a path on the blacklist will not be
    included in the stack trace.
    """
    for path in paths:
        blacklist_paths.append(os.path.normpath(path).lower())


def pathed_config(configuration, *paths):
    """Use alternate configuration for files in the stack trace whose path
    begins with one of these paths."""
    for path in paths:
        config_paths[os.path.normpath(path).lower()] = configuration



class ExceptionWriter():
    """ExceptionWriter class for outputing exceptions to the screen.
    Methods beginning 'write_' are the primary candidates for overriding.

    Inherit from this class, then set:
        pretty_errors.exception_writer = MyExceptionWriter()
    """
    def __init__(self):
        self.config = None


    def get_terminal_width(self):
        """Width of terminal in characters."""
        try:
            return os.get_terminal_size()[0]
        except Exception:
            return 79


    def get_line_length(self):
        """Calculated line length."""
        if self.config.line_length == 0:
            return self.get_terminal_width()
        else:
            return self.config.line_length


    def visible_length(self, s):
        """Visible length of string (i.e. without ansi escape sequences)"""
        return len(ansi_escape.sub('', s))


    def output_text(self, texts):
        """Write list of texts to stderr.
        Use this function for all output.

            texts: a string or a list of strings
        """
        if not isinstance(texts, (list, tuple)):
            texts = [texts]
        count = 0
        for text in texts:
            text = str(text)
            output_stderr.write(text)
            count += self.visible_length(text)
        line_length = self.get_line_length()
        if count == 0 or count % line_length != 0 or self.config.full_line_newline:
            output_stderr.write('\n')
        output_stderr.write(RESET_COLOR)
        if self.config.reset_stdout:
            sys.stdout.write(RESET_COLOR)


    def write_header(self):
        """Write stack trace header to screen.

            Should make use of:
                self.config.separator_character
                self.config.display_timestamp
                self.config.timestamp_function()
                self.config.header_color"""
        if not self.config.separator_character: return
        line_length = self.get_line_length()
        if self.config.display_timestamp:
            timestamp = str(self.config.timestamp_function())
            separator = (line_length - len(timestamp)) * self.config.separator_character + timestamp
        else:
            separator = line_length * self.config.separator_character
        self.output_text('')
        self.output_text([self.config.header_color, separator])


    def write_location(self, path, line, function):
        """Write location of frame to screen.

        Should make use of:
            self.config.filename_display
            self.config.filename_color
            self.config.line_number_color
            self.config.function_color
            self.config.line_number_first
            self.config.function_color
            self.config.display_link
            self.config.link_color
        """
        line_number = str(line) + ' '
        self.output_text('')
        if self.config.filename_display == FILENAME_FULL:
            filename = ""
            self.output_text([self.config.filename_color, path])
            self.output_text([self.config.line_number_color, line_number, self.config.function_color, function])
        else:
            if self.config.filename_display == FILENAME_EXTENDED:
                line_length = self.get_line_length()
                filename = path[-(line_length - len(line_number) - len(function) - 4):]
                if filename != path:
                    filename = '...' + filename
            else:
                filename = os.path.basename(path)
            if self.config.line_number_first:
                self.output_text([
                    self.config.line_number_color, line_number,
                    self.config.function_color,    function + ' ',
                    self.config.filename_color,    filename
                ])
            else:
                self.output_text([
                    self.config.filename_color,    filename + ' ',
                    self.config.line_number_color, line_number,
                    self.config.function_color,    function
                ])
        if self.config.display_link:
            self.output_text([self.config.link_color, '"%s", line %s' % (path, line)])


    def write_code(self, filepath, line, module_globals, is_final, point_at = None):
        """Write frame code to screen.
        Parameters:
            filepath:        path to code file
            line:            line number in file
            module_globals:  pass to linecache.getline()
            is_final:        True if this is the last frame
            point_at:        character position to point at

        Should make use of:
            self.config.lines_before
            self.config.lines_after
            self.config.trace_lines_before
            self.config.trace_lines_after
            self.config.truncate_code
            self.config.display_arrow
            self.config.arrow_head_character
            self.config.arrow_tail_character
            self.config.line_color
            self.config.code_color
            self.config.arrow_head_color
            self.config.arrow_tail_color
            self.config.syntax_error_color
        """

        lines = []
        if filepath == '<stdin>':
            lines.append(str(line).rstrip())
            line = target_line = start = end = 0
        else:
            if is_final:
                target_line = self.config.lines_before
                start = line - self.config.lines_before
                end   = line + self.config.lines_after
            else:
                target_line = self.config.trace_lines_before
                start = line - self.config.trace_lines_before
                end   = line + self.config.trace_lines_after

            if start < 1:
                target_line -= (1 - start)
                start = 1

            for i in range(start, end + 1):
                lines.append(linecache.getline(filepath, i, module_globals).rstrip())

        min_lead = None
        for line in lines:
            if line.strip() == '': continue
            c = 0
            while c < len(line) and line[c] in (' ', '\t'):
                c += 1
            if min_lead is None or c < min_lead:
                min_lead = c
        if min_lead is None:
            min_lead = 0
        if min_lead > 0:
            lines = [line[min_lead:] for line in lines]

        line_length = self.get_line_length()

        for i, line in enumerate(lines):
            if i == target_line:
                color = self.config.line_color
                if point_at is not None:
                    point_at -= (min_lead + 1)
            else:
                color = self.config.code_color
            color_length = self.visible_length(color)
            if self.config.truncate_code and len(line) + color_length > line_length:
                line = line[:line_length - color_length + 3] + '...'
            if i == target_line and point_at is not None:
                if point_at >= line_length:
                    point_at = line_length - 1
                start_char = point_at
                while start_char > 0 and line[start_char - 1] not in (' ', '\t'):
                    start_char -= 1
                end_char = point_at + 1
                while end_char < len(line) - 1 and line[end_char] not in (' ', '\t'):
                    end_char += 1
                self.output_text([
                    color, line[:start_char], RESET_COLOR,
                    self.config.syntax_error_color, line[start_char:end_char], RESET_COLOR,
                    color, line[end_char:]
                ])
                if self.config.display_arrow:
                    self.output_text([
                        self.config.arrow_tail_color, self.config.arrow_tail_character * point_at,
                        self.config.arrow_head_color, self.config.arrow_head_character
                    ])
            else:
                self.output_text([color, line])

        return '\n'.join(lines)


    def exception_name(self, exception):
        """Name of exception."""
        label = str(exception)
        if label.startswith("<class '"):
            label = label[8:-2]
        return label


    def write_exception(self, exception_type, exception_value):
        """Write exception to screen.

        Should make use of:
            self.exception_name()
            self.config.exception_color
            self.config.exception_arg_color
        """
        if exception_value and len(exception_value.args) > 0:
            output = [
                self.config.exception_color, self.exception_name(exception_type), ':\n',
                self.config.exception_arg_color, '\n'.join((str(x) for x in exception_value.args))
            ]
        else:
            output = [self.config.exception_color, self.exception_name(exception_type)]

        for attr in ("filename", "filename2"):
            if hasattr(exception_value, attr):
                path = getattr(exception_value, attr)
                if path is not None:
                    output.append('\n')
                    output.append(self.config.exception_file_color)
                    output.append(path)

        self.output_text(output)



exception_writer = ExceptionWriter()



def excepthook(exception_type, exception_value, traceback):
    "Replaces sys.excepthook to output pretty errors."

    writer = exception_writer
    writer.config = writer.default_config = config


    if (not writer.config.top_first and exception_value.__context__
            and (not exception_value.__suppress_context__ or config.show_suppressed)):
        excepthook(type(exception_value.__context__), exception_value.__context__, exception_value.__context__.__traceback__)
        writer.config = writer.default_config
        if writer.config.inner_exception_message != None:
            if writer.config.inner_exception_separator:
                writer.write_header()
            output_stderr.write(writer.config.inner_exception_message)

    def check_for_pathed_config(path):
        writer.config = writer.default_config
        for config_path in config_paths:
            if path.startswith(config_path):
                writer.config = config_paths[config_path]
                break

    if traceback:
        tb = traceback
        while tb.tb_next != None:
            tb = tb.tb_next
        check_for_pathed_config(os.path.normpath(tb.tb_frame.f_code.co_filename).lower())
        writer.default_config = writer.config

    writer.write_header()

    if writer.config.prefix != None:
        output_stderr.write(writer.config.prefix)

    syntax_error_info = None
    if exception_type == SyntaxError:
        syntax_error_info = exception_value.args[1]
        exception_value.args = [exception_value.args[0]]

    if writer.config.exception_above:
        writer.output_text('')
        writer.write_exception(exception_type, exception_value)

    if syntax_error_info:
        check_for_pathed_config(os.path.normpath(syntax_error_info[0]).lower())
        writer.write_location(syntax_error_info[0], syntax_error_info[1], '')
        if(syntax_error_info[0] == '<stdin>'):
            writer.write_code(syntax_error_info[0], syntax_error_info[3], [], True, syntax_error_info[2])
        else:
            writer.write_code(syntax_error_info[0], syntax_error_info[1], [], True, syntax_error_info[2])
    else:
        tracebacks = []
        while traceback != None:
            path = os.path.normpath(traceback.tb_frame.f_code.co_filename).lower()
            if traceback.tb_next == None or (writer.config.always_display_bottom and tracebacks == []):
                tracebacks.append(traceback)
            else:
                if whitelist_paths:
                    for white in whitelist_paths:
                        if path.startswith(white): break
                    else:
                        traceback = traceback.tb_next
                        continue
                for black in blacklist_paths:
                    if path.startswith(black): break
                else:
                    tracebacks.append(traceback)
            traceback = traceback.tb_next

        if writer.config.top_first:
            tracebacks.reverse()
            if writer.config.stack_depth > 0:
                if writer.config.always_display_bottom and len(tracebacks) > 1:
                    tracebacks = tracebacks[:writer.config.stack_depth] + tracebacks[-1:]
                else:
                    tracebacks = tracebacks[:writer.config.stack_depth]
            final = 0
        else:
            if writer.config.stack_depth > 0:
                if writer.config.always_display_bottom and len(tracebacks) > 1:
                    tracebacks = tracebacks[:1] + tracebacks[-writer.config.stack_depth:]
                else:
                    tracebacks = tracebacks[-writer.config.stack_depth:]
            final = len(tracebacks) - 1

        for count, traceback in enumerate(tracebacks):
            path = os.path.normpath(traceback.tb_frame.f_code.co_filename).lower()
            check_for_pathed_config(path)

            if writer.config.infix != None and count != 0:
                output_stderr.write(writer.config.infix)

            frame = traceback.tb_frame
            code = frame.f_code
            writer.write_location(code.co_filename, traceback.tb_lineno, code.co_name)
            code_string = writer.write_code(code.co_filename, traceback.tb_lineno, frame.f_globals, count == final)

            if (writer.config.display_locals and count == final) or (writer.config.display_trace_locals and count != final):
                local_variables = [(code_string.find(x), x) for x in frame.f_locals]
                local_variables.sort()
                local_variables = [x[1] for x in local_variables if x[0] >= 0]
                if local_variables:
                    writer.output_text('')
                    spacer = ': '
                    len_spacer = '... '
                    line_length = writer.get_line_length()
                    for local in local_variables:
                        value = str(frame.f_locals[local])
                        output = [writer.config.local_name_color, local, spacer, writer.config.local_value_color]
                        if writer.config.truncate_locals and len(local) + len(spacer) + len(value) > line_length:
                            length = '[' + str(len(value)) + ']'
                            value = value[:line_length - (len(local) + len(spacer) + len(len_spacer) + len(length))]
                            output += [value, len_spacer, writer.config.local_len_color, length]
                        else:
                            output += [value]
                        writer.output_text(output)

    writer.config = writer.default_config

    if writer.config.exception_below:
        writer.output_text('')
        writer.write_exception(exception_type, exception_value)

    if writer.config.postfix != None:
        output_stderr.write(writer.config.postfix)

    if (writer.config.top_first and exception_value.__context__ and
        (not exception_value.__suppress_context__ or config.show_suppressed)):
        if writer.config.inner_exception_message != None:
            if writer.config.inner_exception_separator:
                writer.write_header()
            output_stderr.write(writer.config.inner_exception_message)
        excepthook(type(exception_value.__context__), exception_value.__context__, exception_value.__context__.__traceback__)



location_expression = re.compile(r'.*File "([^"]*)", line ([0-9]+), in (.*)')

class StdErr():
    """Replaces sys.stderr in order to scrape it, when capturing stack trace is unavailable."""
    def __init__(self):
        self.__in_exception = False
        self.__awaiting_code = False
        self.__awaiting_end = 0
        self.__frames = []
        self.__point_at = None


    def __getattr__(self, name):
        return getattr(output_stderr, name)


    def __enter__(self, *args, **kwargs):
        return output_stderr.__enter__(*args, **kwargs)


    def __is_header(self, text):
        """Is text a traceback header?"""
        return text.startswith('Traceback (most recent call last):')


    def __is_outer_exception(self, text):
        """Is text a notification for an outer exception?"""
        return text.startswith('During handling of the above exception, another exception occurred:')


    def __get_location(self, text):
        """Extract location of exception.  If it returns None then text was not a location identifier."""
        location = location_expression.match(text)
        if location:
            return (location.group(1), int(location.group(2)), location.group(3))
        else:
            return None


    def __write_exception(self):
        """Write exception, prettily."""
        if not self.__frames: return

        writer = exception_writer
        writer.config = writer.default_config = config

        def check_for_pathed_config(path):
            writer.config = writer.default_config
            for config_path in config_paths:
                if path.startswith(config_path):
                    writer.config = config_paths[config_path]
                    break

        path, line_number, function = self.__frames[-1]
        check_for_pathed_config(os.path.normpath(path.lower()))
        writer.default_config = writer.config

        writer.write_header()

        if writer.config.prefix != None:
            output_stderr.write(writer.config.prefix)

        exception_type = self.__exception
        if self.__exception_args:
            class ExceptionValue():
                def __init__(self):
                    self.args = []
            exception_value = ExceptionValue()
            if self.__exception_args.startswith('('):
                for arg in self.__exception_args[1:-1].split(', '):
                    exception_value.args.append(arg)
            else:
                exception_value.args.append(self.__exception_args)
        else:
            exception_value = None

        syntax_error_info = None
        if self.__exception == 'SyntaxError':
            syntax_error_info = self.__frames[-1]
            syntax_error_info[2] = self.__point_at

        if writer.config.exception_above:
            writer.output_text('')
            writer.write_exception(exception_type, exception_value)

        if syntax_error_info:
            check_for_pathed_config(os.path.normpath(syntax_error_info[0]).lower())
            writer.write_location(syntax_error_info[0], syntax_error_info[1], '')
            writer.write_code(syntax_error_info[0], syntax_error_info[1], [], True, syntax_error_info[2])
        else:
            tracebacks = []
            for i, frame in enumerate(self.__frames):
                path, line_number, function = frame
                path = os.path.normpath(path).lower()
                if (i == len(self.__frames) - 1) or (writer.config.always_display_bottom and tracebacks == []):
                    tracebacks.append(frame)
                else:
                    if whitelist_paths:
                        for white in whitelist_paths:
                            if path.startswith(white): break
                        else:
                            continue
                    for black in blacklist_paths:
                        if path.startswith(black): break
                    else:
                        tracebacks.append(frame)

            if writer.config.top_first:
                tracebacks.reverse()
                if writer.config.stack_depth > 0:
                    if writer.config.always_display_bottom and len(tracebacks) > 1:
                        tracebacks = tracebacks[:writer.config.stack_depth] + tracebacks[-1:]
                    else:
                        tracebacks = tracebacks[:writer.config.stack_depth]
                final = 0
            else:
                if writer.config.stack_depth > 0:
                    if writer.config.always_display_bottom and len(tracebacks) > 1:
                        tracebacks = tracebacks[:1] + tracebacks[-writer.config.stack_depth:]
                    else:
                        tracebacks = tracebacks[-writer.config.stack_depth:]
                final = len(tracebacks) - 1

            for count, traceback in enumerate(tracebacks):
                path, line_number, function = traceback
                normpath = os.path.normpath(path).lower()
                check_for_pathed_config(normpath)

                if writer.config.infix != None and count != 0:
                    output_stderr.write(writer.config.infix)

                writer.write_location(path, line_number, function)
                writer.write_code(path, line_number, [], count == final)

        writer.config = writer.default_config

        if writer.config.exception_below:
            writer.output_text('')
            writer.write_exception(exception_type, exception_value)

        if writer.config.postfix != None:
            output_stderr.write(writer.config.postfix)


    def write(self, text):
        """Replaces sys.stderr.write, outputing pretty errors."""
        if not self.__in_exception and not text.split():
            output_stderr.write(text)
        else:
            for line in text.split('\n'):
                if self.__awaiting_end > 0:
                    self.__awaiting_end -= 1
                    if self.__awaiting_end == 0:
                        self.__exception_args = line.strip()
                        self.__in_exception = False
                        self.__write_exception()
                elif self.__in_exception:
                    if not line.strip():
                        pass
                    elif self.__awaiting_code:
                        self.__awaiting_code = False
                    else:
                        location = self.__get_location(line)
                        if location:
                            self.__frames.append(location)
                            self.__awaiting_code = True
                        elif line.strip() == '^':
                            self.__point_at = len(line) - 2
                        else: # end of traceback
                            if ': ' in line:
                                self.__exception, self.__exception_args = line.strip().split(': ', 1)
                                self.__in_exception = False
                                self.__write_exception()
                            else:
                                self.__awaiting_end = 2
                                self.__exception = line.strip()
                elif self.__is_header(line):
                    self.__in_exception = True
                    self.__awaiting_code = False
                    self.__frames = []
                elif self.__is_outer_exception(line):
                    if config.inner_exception_message != None:
                        if config.inner_exception_separator:
                            exception_writer.write_header()
                        output_stderr.write(config.inner_exception_message)
                else:
                    output_stderr.write(line)



def replace_stderr(force = False):
    """Replace sys.stderr, for cases where standard use with activate() does not work."""
    if (force or not interactive_tty_only or terminal_is_interactive):
        sys.stderr = StdErr()


def activate():
    """Set sys.excepthook to use pretty errors."""
    sys.excepthook = excepthook


if active and (not interactive_tty_only or terminal_is_interactive):
    activate()



if __name__ == "__main__":
    configure(
        filename_display    = FILENAME_EXTENDED,
        line_number_first   = True,
        display_link        = True,
        lines_before        = 5,
        lines_after         = 2,
        line_color          = RED + '> ' + default_config.line_color,
        code_color          =       '  ' + default_config.line_color,
        truncate_code       = True,
        inner_exception_separator=True,
        inner_exception_message = MAGENTA + "\n  During handling of the above exception, another exception occurred:\n",
        display_locals      = True
    )
    blacklist('c:/python')
    try:
        myval = [1,2]
        print(myval[3])
    except:
        a = "C" * "B"
