# v1.2.6

* Fixed `pathed_config` bug.
* Added `activate` call.
* Added arrow pointing to syntax error.
* Added config options `display_arrow`, `arrow_head_character`, `arrow_head_color`, `arrow_tail_character`, `arrow_tail_color`, `syntax_error_color`


# v1.2.5

* Fix comment skeleton in *customize.py output.


# v1.2.4

* README updated.


# v1.2.3

* Added `ExceptionWriter` class to allow for overriding.
* Added `pathed_config` call to allow for multiple configs, activated by path of code file in frame.
* Added environment variable `PYTHON_PRETTY_ERRORS`.  If set to `0` then pretty_errors will be disabled.


# v1.2.2

* `separator_character` can now be set to `None` or `''` to disable header.
* Improved install wizard.
* Spelling corrections.


# v1.2.1

* Fix for Python 2


# v1.2.0

* Added `mono` function to set useful config options for a monochrome terminal.
* Added config option `timestamp_function`
* Added `default_config` for reference.
* May now use any characters in color prefixes (not just escape sequences)
* Removed config options `line_prefix`, `code_prefix`, `line_prefix_color`, `code_prefix_color` - no longer needed because of above.


# v 1.1.11

* Fix for python 2


# v1.1.10

* Added `__main__` for running with `-m`
* Removed post-install code (it doesn't work with `pip` - `pip` has no post-install hook)


# v1.1.9

* Automated adding to `sitecustomize.py`


# v1.1.8

* Added config options `always_display_bottom`, `truncate_locals`, `truncate_code`, `line_prefix`, `code_prefix`, `line_prefix_color`, `code_prefix_color`, `local_len_color`


# v1.1.7

* Site customize instructions.


# v1.1.6

* Added config options `display_locals`, `display_trace_locals`, `local_name_color`, `local_value_color`


# v1.1.5

* Nada


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
