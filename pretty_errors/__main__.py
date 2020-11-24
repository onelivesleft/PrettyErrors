import pretty_errors, sys, os, re, site
if '-h' in sys.argv or '--help' in sys.argv or '/?' in sys.argv:
    print("""\
Run without options to use interactive mode, otherwise:

  python -m pretty_errors [-m] <-u|-s> [-p] OR <-f> OR <-c>

-m = monochrome (do not use color escape codes in output of this menu)
-u = install in default user location
-s = install in default system location
-p = with above, install in pretty_errors.pth instead of *customize.py
-f = find where pretty_errors is installed
-c = clean pretty_errors from python startup (do so before uninstalling)""")

else:
    find        = ('-f' in sys.argv)
    add_to_user = ('-u' in sys.argv)
    add_to_site = ('-s' in sys.argv)
    pth         = ('-p' in sys.argv)
    clean       = ('-c' in sys.argv)
    mono        = ('-m' in sys.argv)

    if not mono:
        reset_color   = pretty_errors.RESET_COLOR
        file_color    = pretty_errors.BRIGHT_CYAN
        message_color = pretty_errors.BRIGHT_RED
        key_color     = pretty_errors.YELLOW
        error_color   = pretty_errors.RED
    else:
        reset_color   = ''
        file_color    = ''
        message_color = ''
        key_color     = ''
        error_color   = ''

    check = re.compile(r'^\s*import\s+\bpretty_errors\b', re.MULTILINE)

    in_virtualenv = 'VIRTUAL_ENV' in os.environ
    # in virtualenv, `site` has no attribute `getsitepackages` or `getusersitepackages`
    if in_virtualenv:
        def getsitepackages():
            pattern = re.compile(r'^%s$' % os.path.join(os.environ['VIRTUAL_ENV'], 'lib', 'python[0-9.]+', 'site-packages'))
            return [path for path in set(sys.path) if pattern.search(path)]

        def getusersitepackages():
            return []
    else:
        getsitepackages = site.getsitepackages

        def getusersitepackages():
            return [site.getusersitepackages()]

    def getallsitepackages():
        return getsitepackages() + getusersitepackages()


    def readfile(path):
        try:
            return ''.join((x for x in open(path)))
        except IOError:
            return ''


    def find_install(quiet = False):
        found = False
        for path in getallsitepackages():
            for filename in 'usercustomize.py', 'sitecustomize.py', 'pretty_errors.pth':
                filepath = os.path.join(path, filename)
                if check.search(readfile(filepath)):
                    if not found:
                        print(message_color + '\n\npretty_errors found in:' + file_color)
                        found = True
                    print(filepath)
                    print(reset_color)
        if not found and not quiet:
            print(message_color + '\npretty_errors not currently installed in any expected locations.\n' + reset_color)
        return found

    def clean_install():
        files_to_edit = []
        files_to_remove = []
        for path in getallsitepackages():
            for filename in 'usercustomize.py', 'sitecustomize.py', 'pretty_errors.pth':
                filepath = os.path.join(path, filename)
                data = readfile(filepath).strip()
                if check.search(data):
                    if filename.endswith('.pth') or (
                            data.startswith('### BEGIN PRETTY ERRORS') and
                            data.endswith('### END PRETTY ERRORS')):
                        files_to_remove.append(filepath)
                    else:
                        files_to_edit.append(filepath)
        if not files_to_edit and not files_to_remove:
            print(message_color + '\npretty_errors not currently installed in any expected locations.' + reset_color)
            return
        if files_to_remove:
            print('\nAttempting to remove the following files:\n')
            for filepath in files_to_remove:
                print(file_color + filepath + reset_color, end='... ')
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(error_color + 'ERR\n' + str(e) + reset_color)
                else:
                    print('OK')
        if files_to_edit:
            print('\n\nFound entry for pretty_errors in the following files.\n' +
                message_color +
                'Please edit and remove the relevant section:\n')
            for filepath in files_to_edit:
                print(file_color + filepath + reset_color)

    if find:
        find_install()
        sys.exit(0)
    elif clean:
        clean_install()
        sys.exit(0)

    if add_to_user:
        if in_virtualenv:
            print('You are now in virtualenv, which has sitepackage but no user sitepackages, ' +
                  message_color + '`-u`' + reset_color + ' is incompatible with virtualenv.')
            print('Please use ' + message_color + '`-s`' + reset_color + ' instead.')
            sys.exit(1)
        path = getusersitepackages()[0]
        filename = 'pretty_errors.pth' if pth else 'usercustomize.py'
    elif add_to_site:
        path = getsitepackages()[0]
        filename = 'pretty_errors.pth' if pth else 'sitecustomize.py'
    else:

        found = find_install(True)

        def prompt(key, caption, is_path = False):
            if is_path:
                print(key_color + key + reset_color + ': ' + file_color + caption + reset_color)
            else:
                print(key_color + key + reset_color + ': ' + caption + reset_color)

        def get_choice(query, choices, default = None):
            options = {}
            for i in range(len(choices)):
                options[str(i + 1)] = i
            while True:
                print()
                print(' ' + query)
                print()
                if found:
                    prompt('C', 'Clean startup files (do so before uninstalling pretty_errors)')
                for option, choice in enumerate(choices):
                    prompt('%d' % (option + 1), choice, True)
                prompt('0', 'Exit')
                if default is None:
                    print('\nOption: ', end='')
                else:
                    print('\nOption: [default: ' + message_color + str(default + 1) + reset_color + '] ', end='')
                choice = input()
                if choice == '' and default is not None:
                    choice = str(default + 1)
                if choice == '0':
                    sys.exit(0)
                elif choice.lower() == 'c':
                    clean_install()
                    sys.exit(0)
                elif choice in options:
                    return options[choice]

        formatting = {'file': file_color, 'msg': message_color, 'reset': reset_color, 'key': key_color}
        print("""
To have pretty_errors be used when you run any python file you may add it to your\
%(file)s usercustomize.py %(reset)s(user level) or\
%(file)s sitecustomize.py %(reset)s(system level), or to\
%(file)s pretty_errors.pth%(reset)s.

(just hit %(key)s<enter>%(reset)s to accept the defaults if you are unsure)
""" % formatting)

        paths = getallsitepackages()
        path = paths[get_choice('Choose folder to install into:', paths, -1 if found else len(paths) - 1)]

        if path in getsitepackages():
            filenames = ['sitecustomize.py', 'pretty_errors.pth']
        else:
            filenames = ['usercustomize.py', 'pretty_errors.pth']
        filename = filenames[get_choice('Choose file to install into:', filenames, 0)]

    if filename.endswith('.pth'):
        output = (os.path.dirname(os.path.dirname(os.path.normpath(__file__))) +
            '\nimport pretty_errors; ' +
            '#pretty_errors.configure()  ' +
            '# keep on one line, for options see ' +
            'https://github.com/onelivesleft/PrettyErrors/blob/master/README.md'
        )
    else:
        output = []
        output.append('''

### BEGIN PRETTY ERRORS

# pretty-errors package to make exception reports legible.
# v%s generated this config: newer version may have added methods/options not present!

try:
    import pretty_errors
except ImportError:
    print(
        'You have uninstalled pretty_errors but it is still present in your python startup.' +
        '  Please remove its section from file:\\n ' + __file__ + '\\n'
    )
else:
    pass

    # Use if you do not have a color terminal:
    #pretty_errors.mono()

    # Use if you are using a framework which is handling all the exceptions before pretty_errors can:
    #if pretty_errors.active:
    #    pretty_errors.replace_stderr()

    # Use to hide frames whose file begins with these paths:
    #pretty_errors.blacklist('/path/to/blacklist', '/other/path/to/blacklist', ...)

    # Use to only show frames whose file begins with these paths:
    #pretty_errors.whitelist('/path/to/whitelist', '/other/path/to/whitelist', ...)

    # Use to selectively set a config based on the path to the code of the current frame.
    #alternate_config = pretty_errors.config.copy()
    #pretty_errors.pathed_config(alternate_config, '/use/alternate/for/this/path')

    # Use to configure output:  Uncomment each line to change that setting.
    """pretty_errors.configure(
    ''' % pretty_errors.__version__)

        options = []
        colors = []
        parameters = []
        max_length = 0
        for option in dir(pretty_errors.config):
            if len(option) > max_length:
                max_length = len(option)
            if (option not in ('configure', 'mono', 'copy') and
                    not option.startswith('_')):
                if option.endswith('_color'):
                    colors.append(option)
                elif option != 'name':
                    options.append(option)
        indent = '        '
        def prefix(s):
            return indent + '#' + s.ljust(max_length) + ' = '
        for option in sorted(options):
            if option == 'filename_display':
                parameters.append(prefix(option) + 'pretty_errors.FILENAME_COMPACT,  # FILENAME_EXTENDED | FILENAME_FULL')
            elif option == 'timestamp_function':
                parameters.append(prefix(option) + 'time.perf_counter')
            else:
                parameters.append(prefix(option) + repr(getattr(pretty_errors.config, option)))
        for option in sorted(colors):
            parameters.append(prefix(option) + repr(getattr(pretty_errors.config, option)))
        parameters.append('\n' + indent + 'name = "custom"  # name it whatever you want')
        output.append(',\n'.join(parameters))
        output.append('\n    )"""\n')
        output.append('### END PRETTY ERRORS\n')
        output = '\n'.join(output)

    print('\n--------------')

    filepath = os.path.join(path, filename)
    if check.search(readfile(filepath)):
        print('\npretty_errors already present in:\n' + file_color + '\n' + filepath +
            '\n' + reset_color + '\nEdit it to set config options.\n')
        sys.exit(0)

    try:
        os.makedirs(path)
    except Exception:
        pass
    try:
        out = open(filepath, 'a')
        out.write(output)
        out.close()
    except Exception:
        print('\nFailed to write to:\n' + filepath)
    else:
        print('\npretty_errors added to:\n' + file_color + '\n' + filepath + '\n' + reset_color + '\nEdit it to set config options.\n')
        if filepath.endswith('.pth'):
            print(error_color + '\n*** Delete this file when you uninstall pretty_errors! ***\n' + reset_color)
