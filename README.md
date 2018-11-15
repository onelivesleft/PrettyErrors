# PrettyErrors

Prettifies Python exception output to make it legible. To use simply put PrettyErrors.py in your project and
```python
import PrettyErrors
```
Note you need to be running in a terminal capable of colour output in order to get colour output: in Windows
this means powershell, cmder, etc.

If you want to configure the output then use `PrettyErrors.configure()`.  For example: ```python
import PrettyErrors
PrettyErrors.configure(seperator_character = '—', line_length = 54, filename_display = PrettyErrors.FilenameDisplayMode.FULL)
```

![Example](https://github.com/onelivesleft/PrettyErrors/blob/master/example.png)
