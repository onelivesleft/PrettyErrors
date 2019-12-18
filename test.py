import pretty_errors
pretty_errors.configure(
    seperator_character = '*',
    filename_display = pretty_errors.FILENAME_EXTENDED,
    lines_before=10,
    stack_depth=2
)
raise KeyError
