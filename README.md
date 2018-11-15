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
pretty_errors.configure(seperator_character = '—', line_length = 54, filename_display = pretty_errors.FilenameDisplayMode.FULL)
```

![Example](https://github.com/onelivesleft/PrettyErrors/blob/master/example.png)
