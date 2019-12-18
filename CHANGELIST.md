# v1.1.0

* Reworked to replace sys.excepthook instead of sys.stderr
* Now automatically works out line length if line length is 0 (which is the default)
* Added config options: `top_first`, `stack_depth`, `exception_above`, `exception_below`, `lines_before`, `lines_after`, `trace_lines_before`, `trace_lines_after`, `line_color`, `code_color` , `exception_color`, `exception_arg_color`, `prefix`, `infix`, `postfix`
* Removed config option: `default_color`
