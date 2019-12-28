import pretty_errors, sys
if '-h' in sys.argv or '--help' in sys.argv or '/?' in sys.argv:
    print("""\
Run without options to use interactive mode, otherwise:

  python -m pretty_errors <-u|-s> [-p] OR <-f>

-u = install in default user location
-s = install in default system location
-p = with above, install in pretty_errors.pth instead of *customize.py
-f = find where pretty_errors is installed""")
else:
    pretty_errors.install(
        find        = ('-f' in sys.argv),
        add_to_user = ('-u' in sys.argv),
        add_to_site = ('-s' in sys.argv),
        pth         = ('-p' in sys.argv))
