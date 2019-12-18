# v1.1.4

* `colorama` dependency


# v1.1.3

* Added `whitelist` and `blacklist`


# v1.1.2

* Fix README


# v1.1.1

* Python 2.7 compatibility


# v1.1.0

* Reworked to replace `sys.excepthook` instead of `sys.stderr`
* Now automatically works out line length if line length is `0` (which is the default)
* Added config options: `top_first`, `stack_depth`, `exception_above`, `exception_below`, `lines_before`, `lines_after`, `trace_lines_before`, `trace_lines_after`, `line_color`, `code_color` , `exception_color`, `exception_arg_color`, `prefix`, `infix`, `postfix`, `line_number_first`
* Removed config option: `default_color`
