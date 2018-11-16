# pretty-errors

Prettifies Python exception output to make it legible. Install it with
```
python -m pip install pretty-errors
```

Then use it simply by importing it:
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
---
![Example](https://i.imgur.com/0jpEqob.png)
---
If you want to customize the output more than `configure` provides then you can replace the output functions
on `sys.stderr` after importing pretty_errors.  These are:

`write_header(self)`
Is called at the start of a traceback.

`write_location(self, path, line_number, function)`
Is called with details on the exception's location.

`write_body(self, body)`
Is called with any other text sent to stderr (i.e. the code in question).  `body` will never contain `\n`, though
it may be longer than the defined maximum line length.

You may replace as many of these functions as you wish, or for maximum control of output you may replace the main
method called with all stderr output:
`write(self, *args)`


You may use these helper functions to make this easier:

`output_text(self, text, wants_newline = False)`
Outputs text while trying to only insert 1 newline when outputing a line of maximum length.

`get_location(self, text)`
Extract's location of exception.  If it returns `None` then text was not a location identifier.

`is_header(self, text)`
Checks if text is the start of a traceback.
