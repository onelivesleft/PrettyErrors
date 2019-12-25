# pretty-errors

Prettifies Python exception output to make it legible. Install it with
```bash
python -m pip install pretty-errors
```

The installer will ask you if you want to add `pretty_errors` to your `sitecustomize.py`.  If you do then it will be used whenever you run *any* python file; you won't have to import it manually.

If you say no, but want to add it later, you can do so by manually editting the file, or by running `pretty_errors`:
```bash
python -m pretty_errors
```

---

![Example](https://i.imgur.com/0jpEqob.png)

---

If you have not installed it in your `sitecustomize.py` you can use it simply by importing it:
```python
import pretty_errors
```
Note you need to be running in a terminal capable of colour output in order to get colour output: in Windows
this means powershell, cmder, etc.

If you want to configure the output then use `pretty_errors.configure()`, `pretty_errors.whitelist()`, `pretty_errors.blacklist()`.  For example:
```python
import pretty_errors
pretty_errors.configure(
    seperator_character = '*',
    filename_display    = pretty_errors.FILENAME_EXTENDED,
    line_number_first   = True,
    display_link        = True,
    lines_before        = 2,
    lines_after         = 1,
    line_prefix_color   = '\033[1;33m',
    line_prefix         = '> ',
    code_prefix         = '  ',
    truncate_code       = True,
    display_locals      = True
)
pretty_errors.blacklist('c:/python')
```

---

##### Whitelist / Blacklist:

You may use the functions `whitelist(path)` and `blacklist(path)` to add paths which will be necessary (`whitelist`) or excluded (`blacklist`).  The top frame of the stack is never excluded.

---

##### Configuration settings:

* `line_length`<br>
Output will be wrapped at this point.  If set to `0` (which is the default) it will automatically match your console width.

* `full_line_newline`<br>
Insert a hard newline even if the line is full.  If `line_length` is the same as your console width and this is enabled then you will see double newlines where unwanted, so usually you would only set this if they are different.

* `seperator_character`<br>
Character used to create the header line.  Hyphen is used by default.

* `display_timestamp`<br>
When enabled a timestamp is written in the traceback header.

* `exception_above`<br>
When enabled the exception is displayed above the stack trace.

* `exception_below`<br>
When enabled the exception is displayed below the stack trace.

* `stack_depth`<br>
The maximum number of entries from the stack trace to display.  When `0` will display the entire stack, which is the default.

* `top_first`<br>
When enabled the stack trace will be reversed, displaying the top of the stack first.

* `always_display_bottom`<br>
When enabled (which is the default) the bottom frame of the stack trace will always be displayed.

* `filename_display`<br>
How the filename is displayed: may be `pretty_errors.FILENAME_COMPACT`, `pretty_errors.FILENAME_EXTENDED`, or `pretty_errors.FILENAME_FULL`

* `line_number_first`<br>
When enabled the line number will be displayed first, rather than the filename.

* `display_link`<br>
When enabled a link is written below the error location, which VSCode will allow you to click on.

* `lines_after`, `lines_before`<br>
How many lines of code to display for the top frame, before and after the line the exception occurred on.

* `trace_lines_after`, `trace_lines_before`<br>
How many lines of code to display for each other frame in the stack trace, before and after the line the exception occurred on.

* `line_prefix`<br>
String displayed before the line which caused the exception.

* `code_prefix`<br>
String displayed before each line of context code.

* `truncate_code`<br>
When enabled each line of code will be truncated to fit the line length.

* `display_locals`<br>
When enabled, local variables appearing in the top stack frame code will be displayed with their values.

* `display_trace_locals`<br>
When enabled, local variables appearing in other stack frame code will be displayed with their values.

* `truncate_locals`<br>
When enabled the values of displayed local variables will be truncated to fit the line length.

* `prefix`<br>
Text string which is displayed at the top of the report, just below the header.

* `infix`<br>
Text string which is displayed between each frame of the stack.

* `postfix`<br>
Text string which is displayed at the bottom of the exception report.

* `reset_stdout`<br>
When enabled the reset escape sequence will be written to stdout as well as stderr; turn this on if your console is being left with the wrong color.

---

* `header_color`<br>
Escape sequence to set header color.

* `timestamp_color`<br>
Escape sequence to set timestamp color.

* `exception_color`<br>
Escape sequence to set exception color.

* `exception_arg_color`<br>
Escape sequence to set exception arguments color.

* `filename_color`<br>
Escape sequence to set filename color.

* `line_number_color`<br>
Escape sequence to set line number color.

* `function_color`<br>
Escape sequence to set function color.

* `link_color`<br>
Escape sequence to set link color.

* `line_prefix_color`<br>
Escape sequence to set color of prefix for line of code which caused the exception.

* `line_color`<br>
Escape sequence to set the color of the line of code which caused the exception.

* `code_prefix_color`<br>
Escape sequence to set color of prefix for context code lines.

* `code_color`<br>
Escape sequence to set the color of other displayed lines of code.

* `local_name_color`<br>
Escape sequence to set the color of local variable names.

* `local_value_color`<br>
Escape sequence to set the color of local variable values.

* `local_len_color`<br>
Escape sequence to set the color of local value length when local is truncated.
