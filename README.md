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
    seperator_character = '—',
    line_length = 54,
    filename_display = pretty_errors.FILENAME_FULL
)
```
It is possible to have the interactive interpreter always use `pretty_errors`, instead of including it in your projects, by using the `PYTHONSTARTUP` environment variable.  Set it to a python file and that file will be run every time python is.  If you don't already have one then create a file with the above code block and set `PYTHONSTARTUP` to its path.  Whenever you run python interactively, `pretty_errors` will be automatically imported and configured (though this will not be true when your python code is run outwith the interactive interpreter.)
---
Configuration settings:
* `line_length` : Output will be wrapped at this point.  If this matches your console width you may want to disable `full_line_newline` in order to prevent apparent double newlines.
* `full_line_newline` : Insert a hard newline even if the line is full.  Disable if the console automatically inserts its own newline at this point.
* `filename_display` : How the filename is displayed: may be `FILENAME_COMPACT`, `FILENAME_EXTENDED`, or `FILENAME_FULL`
* `display_timestamp` : When enabled a timestamp is written in the traceback header.
* `seperator_character` : Character used to create the header line.  Hyphen is used by default.
* `header_color` : Escape sequence to set header color.
* `timestamp_color` : Escape sequence to set timestamp color.
* `default_color` : Escape sequence to set default color.
* `filename_color` : Escape sequence to set filename color.
* `line_number_color` : Escape sequence to set line number color.
* `function_color` : Escape sequence to set function color.
* `reset_stdout` : When enabled the reset escape sequence will be written to stdout as well as stderr; turn this on if your console is being left with the wrong color.
---
If you want to customize the output more than `configure` provides then you can replace the output functions
on `sys.stderr` after importing `pretty_errors`.  These are:

### `write_header(self)`
Is called at the start of a traceback.

### `timestamp(self)`
Returns a string timestamp used in the header if `display_timestamp` is enabled.

### `write_location(self, path, line_number, function)`
Is called with details on the exception's location.

### `write_body(self, body)`
Is called with any other text sent to stderr (i.e. the code in question).  `body` will never contain `\n`, though
it may be longer than the defined maximum line length.

You may replace as many of these functions as you wish, or for maximum control of output you may replace the main
method called with all stderr output:

###`write(self, *args)`
Replacement for `sys.stderr.write`


You may use these helper functions to make this easier (see `pretty_errors/__init__.py` for examples, especially `write`):

`output_text(self, text, wants_newline = False)`
Outputs text while trying to only insert 1 newline when outputing a line of maximum length.  `text` should be a
list of strings: colour escape codes and text data.

`get_location(self, text)`
Extract's location of exception.  If it returns `None` then text was not a location identifier.

`is_header(self, text)`
Checks if text is the start of a traceback.


For example, to change the header:
```python
def write_header(self):
    self.output_text([self.header_color, "\nERROR!!!!!!!!!!"], wants_newline = True)

sys.stderr.write_header = write_header
```
