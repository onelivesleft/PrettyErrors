import pretty_errors, sys
pretty_errors.install(skip_query=('-y' in sys.argv))
