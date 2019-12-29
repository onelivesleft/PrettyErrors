import pretty_errors
pretty_errors.configure(
    separator_character = '*',
    filename_display = pretty_errors.FILENAME_FULL,
    lines_before=10,
    code_color = pretty_errors.default_config.line_color,
    stack_depth=2
)
irrelevant = pretty_errors.config.copy()
irrelevant.line_color = irrelevant.code_color = irrelevant.filename_color = irrelevant.function_color = irrelevant.line_number_color = (
    pretty_errors.default_config.header_color
)
pretty_errors.pathed_config(irrelevant, 'c:/python', 'c:/users')
raise KeyError
