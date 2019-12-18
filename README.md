# pretty-errors

Prettifies Python exception output to make it legible. Install it with
```
python -m pip install pretty-errors
```
---
![Example](https://i.imgur.com/0jpEqob.png)

---
Use it simply by importing it:
```python
import pretty_errors
```
Note you need to be running in a terminal capable of colour output in order to get colour output: in Windows
this means powershell, cmder, etc.

If you want to configure the output then use `pretty_errors.configure()`.  For example:
```python
import pretty_errors
pretty_errors.configure(
    seperator_character = '*',
    filename_display = pretty_errors.FILENAME_FULL,
    lines_before = 2,
    lines_after = 1
)
pretty_errors.blacklist('c:/python')
```

It is possible to have the interactive interpreter always use `pretty_errors`, instead of including it in your projects, by using the `PYTHONSTARTUP` environment variable.  Set it to a python file and that file will be run every time python is.  If you don't already have one then create a file with the above code block and set `PYTHONSTARTUP` to its path.  Whenever you run python interactively, `pretty_errors` will be automatically imported and configured (though this will not be true when your python code is run outwith the interactive interpreter.)

---

##### Whitelist / Blacklist:

You may use the functions `whitelist(path)` and `blacklist(path)` to add paths which will be necessary (`whitelist`) or excluded (`blacklist`).  The top frame of the stack is never excluded.

---

##### Configuration settings:

* `line_length`<br>
Output will be wrapped at this point.  If set to `0` (which is the default) it will automatically match your console width.

* `full_line_newline`<br>
Insert a hard newline even if the line is full.  If `line_length` is the same as your console width and this is enabled then you will see double newlines where unwanted, so usually you would only set this if they are different.

* `filename_display`<br>
How the filename is displayed: may be `pretty_errors.FILENAME_COMPACT`, `pretty_errors.FILENAME_EXTENDED`, or `pretty_errors.FILENAME_FULL`

* `display_timestamp`<br>
When enabled a timestamp is written in the traceback header.

* `display_link`<br>
When enabled a link is written below the error location, which VSCode will allow you to click on.

* `display_locals`<br>
When enabled, local variables appearing in the top stack frame code will be displayed with their values.

* `display_trace_locals`<br>
When enabled, local variables appearing in other stack frame code will be displayed with their values.

* `exception_above`<br>
When enabled the exception is displayed above the stack trace.

* `exception_below`<br>
When enabled the exception is displayed below the stack trace.

* `line_number_first`<br>
When enabled the line number will be displayed first, rather than the filename.

* `top_first`<br>
When enabled the stack trace will be reversed, displaying the top of the stack first.

* `stack_depth`<br>
The maximum number of entries from the stack trace to display.  When `0` will display the entire stack, which is the default.

* `lines_before`, `lines_after`<br>
How many lines of code to display for the top frame, before and after the line the exception occurred on.

* `trace_lines_before`, `trace_lines_after`<br>
How many lines of code to display for each other frame in the stack trace, before and after the line the exception occurred on.

* `seperator_character`<br>
Character used to create the header line.  Hyphen is used by default.

* `prefix`<br>
Text string which is displayed at the top of the report, just below the header.

* `infix`<br>
Text string which is displayed between each frame of the stack.

* `postfix`<br>
Text string which is displayed at the bottom of the exception report.

* `header_color`<br>
Escape sequence to set header color.

* `timestamp_color`<br>
Escape sequence to set timestamp color.

* `line_color`<br>
Escape sequence to set the color of the line of code which caused the exception.

* `code_color`<br>
Escape sequence to set the color of other displayed lines of code.

* `local_name_color`<br>
Escape sequence to set the color of local variable names.

* `local_value_color`<br>
Escape sequence to set the color of local variable values.

* `filename_color`<br>
Escape sequence to set filename color.

* `line_number_color`<br>
Escape sequence to set line number color.

* `function_color`<br>
Escape sequence to set function color.

* `exception_color`<br>
Escape sequence to set exception color.

* `exception_arg_color`<br>
Escape sequence to set exception arguments color.

* `link_color`<br>
Escape sequence to set link color.

* `reset_stdout`<br>
When enabled the reset escape sequence will be written to stdout as well as stderr; turn this on if your console is being left with the wrong color.
