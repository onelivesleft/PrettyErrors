import sys, re, colorama, os, time, linecache
colorama.init()


name = "pretty_errors"

FILENAME_COMPACT  = 0
FILENAME_EXTENDED = 1
FILENAME_FULL     = 2

reset_color = '\033[m'



class PrettyErrorsConfig():
    def __init__(self):
        self.line_length            = 0
        self.full_line_newline      = False
        self.filename_display       = FILENAME_COMPACT
        self.display_timestamp      = False
        self.display_link           = False
        self.seperator_character    = '-'
        self.line_number_first      = False
        self.top_first              = False
        self.always_display_bottom  = True
        self.stack_depth            = 0
        self.exception_above        = False
        self.exception_below        = True
        self.trace_lines_before     = 0
        self.trace_lines_after      = 0
        self.lines_before           = 0
        self.lines_after            = 0
        self.display_locals         = False
        self.display_trace_locals   = False
        self.truncate_locals        = True
        self.truncate_code          = False
        self.line_prefix            = ''
        self.code_prefix            = ''
        self.header_color           = '\033[1;30m'
        self.timestamp_color        = '\033[1;30m'
        self.line_color             = '\033[1;38m'
        self.code_color             = '\033[1;30m'
        self.line_prefix_color      = '\033[1;38m'
        self.code_prefix_color      = '\033[1;30m'
        self.filename_color         = '\033[1;36m'
        self.line_number_color      = '\033[1;32m'
        self.function_color         = '\033[1;34m'
        self.link_color             = '\033[1;30m'
        self.local_name_color       = '\033[1;35m'
        self.local_value_color      = '\033[m'
        self.local_len_color        = '\033[1;30m'
        self.exception_color        = '\033[1;31m'
        self.exception_arg_color    = '\033[1;33m'
        self.prefix                 = None
        self.infix                  = None
        self.postfix                = None
        self.whitelist_paths        = []
        self.blacklist_paths        = []
        self.reset_stdout           = False


    def configure(self, **kwargs):
        """Used to configure settings governing how exceptions are displayed."""
        for setting in kwargs:
            if kwargs[setting] is not None: setattr(self, setting, kwargs[setting])


config = PrettyErrorsConfig()


def configure(
        always_display_bottom = None,
        code_color = None,
        code_prefix = None,
        code_prefix_color = None,
        display_link = None,
        display_locals = None,
        display_timestamp = None,
        display_trace_locals = None,
        exception_above = None,
        exception_arg_color = None,
        exception_below = None,
        exception_color = None,
        filename_color = None,
        filename_display = None,
        full_line_newline = None,
        function_color = None,
        header_color = None,
        infix = None,
        line_color = None,
        line_length = None,
        line_number_color = None,
        line_number_first = None,
        line_prefix = None,
        line_prefix_color = None,
        lines_after = None,
        lines_before = None,
        link_color = None,
        local_len_color = None,
        local_name_color = None,
        local_value_color = None,
        postfix = None,
        prefix = None,
        reset_stdout = None,
        seperator_character = None,
        stack_depth = None,
        timestamp_color = None,
        top_first = None,
        trace_lines_after = None,
        trace_lines_before = None,
        truncate_code = None,
        truncate_locals = None
        ):
    """Used to configure settings governing how exceptions are displayed."""
    config.configure(
        always_display_bottom  = always_display_bottom,
        code_color             = code_color,
        code_prefix            = code_prefix,
        code_prefix_color      = code_prefix_color,
        display_link           = display_link,
        display_locals         = display_locals,
        display_timestamp      = display_timestamp,
        display_trace_locals   = display_trace_locals,
        exception_above        = exception_above,
        exception_arg_color    = exception_arg_color,
        exception_below        = exception_below,
        exception_color        = exception_color,
        filename_color         = filename_color,
        filename_display       = filename_display,
        full_line_newline      = full_line_newline,
        function_color         = function_color,
        header_color           = header_color,
        infix                  = infix,
        line_color             = line_color,
        line_length            = line_length,
        line_number_color      = line_number_color,
        line_number_first      = line_number_first,
        line_prefix            = line_prefix,
        line_prefix_color      = line_prefix_color,
        lines_after            = lines_after,
        lines_before           = lines_before,
        link_color             = link_color,
        local_len_color        = local_len_color,
        local_name_color       = local_name_color,
        local_value_color      = local_value_color,
        postfix                = postfix,
        prefix                 = prefix,
        reset_stdout           = reset_stdout,
        seperator_character    = seperator_character,
        stack_depth            = stack_depth,
        timestamp_color        = timestamp_color,
        top_first              = top_first,
        trace_lines_after      = trace_lines_after,
        trace_lines_before     = trace_lines_before,
        truncate_code          = truncate_code,
        truncate_locals        = truncate_locals
    )


def whitelist(*paths):
    """If the whitelist has any entries, then only files which begin with
    one of its entries will be included in the stack trace"""
    for path in paths:
        config.whitelist_paths.append(os.path.normpath(path).lower())


def blacklist(*paths):
    """Files which begin with a path on the blacklist will not be
    included in the stack trace."""
    for path in paths:
        config.blacklist_paths.append(os.path.normpath(path).lower())



def excepthook(exception_type, exception_value, traceback):
    "Replaces sys.excepthook to output pretty errors."


    def get_terminal_width():
        try:
            return os.get_terminal_size()[0]
        except Exception:
            return 79


    def get_line_length():
        if config.line_length == 0:
            return get_terminal_width()
        else:
            return config.line_length


    def output_text(texts, newline = False):
        if not isinstance(texts, (list, tuple)):
            texts = [texts]
        count = 0
        for text in texts:
            text = str(text)
            sys.stderr.write(text)
            if not text.startswith('\033'):
                count += len(text)
        line_length = get_line_length()
        if newline and (count == 0 or count % line_length != 0 or config.full_line_newline):
            sys.stderr.write('\n')
        sys.stderr.write(reset_color)
        if config.reset_stdout:
            sys.stdout.write(reset_color)


    def write_header():
        line_length = get_line_length()
        if config.display_timestamp:
            timestamp = str(time.perf_counter())
            seperator = (line_length - len(timestamp)) * config.seperator_character + timestamp
        else:
            seperator = line_length * config.seperator_character
        output_text('\n')
        output_text([config.header_color, seperator], newline = True)


    def write_location(path, line, function):
        line_number = str(line) + ' '
        output_text('\n')
        if config.filename_display == FILENAME_FULL:
            filename = ""
            output_text([config.filename_color, path], newline = True)
            output_text([config.line_number_color, line_number, config.function_color, function], newline = True)
        else:
            if config.filename_display == FILENAME_EXTENDED:
                line_length = get_line_length()
                filename = path[-(line_length - len(line_number) - len(function) - 4):]
                if filename != path:
                    filename = '...' + filename
            else:
                filename = os.path.basename(path)
            if config.line_number_first:
                output_text([
                    config.line_number_color, line_number,
                    config.function_color,    function + ' ',
                    config.filename_color,    filename
                ], newline = True)
            else:
                output_text([
                    config.filename_color,    filename + ' ',
                    config.line_number_color, line_number,
                    config.function_color,    function
                ], newline = True)
        if config.display_link:
            output_text([config.link_color, '"%s", line %s' % (path, line)], newline = True)


    def write_code(filepath, line, module_globals, is_final):
        if is_final:
            target_line = config.lines_before
            start = line - config.lines_before
            end   = line + config.lines_after
        else:
            target_line = config.trace_lines_before
            start = line - config.trace_lines_before
            end   = line + config.trace_lines_after

        if start < 1:
            target_line -= (1 - start)
            start = 1

        lines = []
        for i in range(start, end + 1):
            lines.append(linecache.getline(filepath, i, module_globals).rstrip())

        min_lead = 9999
        for line in lines:
            if line.strip() == '': continue
            c = 0
            while c < len(line) and line[c] in (' ', '\t'):
                c += 1
            if c < min_lead: min_lead = c
        if min_lead > 0:
            lines = [line[min_lead:] for line in lines]

        if config.truncate_code:
            line_length = get_line_length()

        for i, line in enumerate(lines):
            if i == target_line:
                prefix_color = config.line_prefix_color
                prefix       = config.line_prefix
                color        = config.line_color
            else:
                prefix_color = config.code_prefix_color
                prefix       = config.code_prefix
                color        = config.code_color
            if config.truncate_code and len(line) + len(prefix) > line_length:
                line = line[:line_length - (len(prefix) + 3)] + '...'
            if prefix != '':
                output_text([prefix_color, prefix, reset_color, color, line], newline = True)
            else:
                output_text([color, line], newline = True)

        return '\n'.join(lines)


    def exception_name(exception):
        label = str(exception)
        if label.startswith("<class '"):
            label = label[8:-2]
        return label


    def write_exception(exception_type, exception_value):
        if len(exception_value.args) > 0:
            output_text([
                config.exception_color, exception_name(exception_type), ':\n',
                config.exception_arg_color, '\n'.join((str(x) for x in exception_value.args))
            ], newline = True)
        else:
            output_text([config.exception_color, exception_name(exception_type)], newline = True)


    write_header()

    if config.prefix != None:
        sys.stderr.write(config.prefix)

    if config.exception_above:
        output_text('', newline = True)
        write_exception(exception_type, exception_value)

    tracebacks = []
    while traceback != None:
        path = os.path.normpath(traceback.tb_frame.f_code.co_filename).lower()
        if traceback.tb_next == None or (config.always_display_bottom and tracebacks == []):
            tracebacks.append(traceback)
        else:
            if config.whitelist_paths:
                for white in config.whitelist_paths:
                    if path.startswith(white): break
                else:
                    traceback = traceback.tb_next
                    continue
            for black in config.blacklist_paths:
                if path.startswith(black): break
            else:
                tracebacks.append(traceback)
        traceback = traceback.tb_next

    if config.top_first:
        tracebacks.reverse()
        if config.stack_depth > 0:
            if config.always_display_bottom and len(tracebacks) > 1:
                tracebacks = tracebacks[:config.stack_depth] + tracebacks[-1:]
            else:
                tracebacks = tracebacks[:config.stack_depth]
        final = 0
    else:
        if config.stack_depth > 0:
            if config.always_display_bottom and len(tracebacks) > 1:
                tracebacks = tracebacks[:1] + tracebacks[-config.stack_depth:]
            else:
                tracebacks = tracebacks[-config.stack_depth:]
        final = len(tracebacks) - 1

    for count, traceback in enumerate(tracebacks):
        if config.infix != None and count != 0:
            sys.stderr.write(config.infix)

        frame = traceback.tb_frame
        code = frame.f_code
        write_location(code.co_filename, traceback.tb_lineno, code.co_name)
        code_string = write_code(code.co_filename, traceback.tb_lineno, frame.f_globals, count == final)

        if (config.display_locals and count == final) or (config.display_trace_locals and count != final):
            local_variables = [(code_string.find(x), x) for x in frame.f_locals]
            local_variables.sort()
            local_variables = [x[1] for x in local_variables if x[0] >= 0]
            if local_variables:
                output_text('', newline = True)
                spacer = ': '
                len_spacer = '... '
                line_length = get_line_length()
                for local in local_variables:
                    value = str(frame.f_locals[local])
                    output = [config.local_name_color, local, spacer, config.local_value_color]
                    if config.truncate_locals and len(local) + len(spacer) + len(value) > line_length:
                        length = '[' + str(len(value)) + ']'
                        value = value[:line_length - (len(local) + len(spacer) + len(len_spacer) + len(length))]
                        output += [value, len_spacer, config.local_len_color, length]
                    else:
                        output += [value]
                    output_text(output, newline = True)

    if config.exception_below:
        output_text('', newline = True)
        write_exception(exception_type, exception_value)

    if config.postfix != None:
        sys.stderr.write(config.postfix)


sys.excepthook = excepthook



if __name__ == "__main__":
    configure(
        seperator_character = '*',
        filename_display = FILENAME_EXTENDED,
        line_number_first = True,
        display_link = True,
        lines_before = 2,
        lines_after = 1,
        code_color = '\033[1;38m',
        line_prefix_color = '\033[1;33m',
        line_prefix = '> ',
        code_prefix = '  ',
        truncate_code = True,
        display_locals = True
    )
    #blacklist("c:/")
    alpha = "It's actually trick trick question: I'll be back up on 27th. I think the evening of the 29th possibly the 30th as well"
    hello = "Hi"
    raise KeyError("foo", 1)
        #test
