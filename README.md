# time_trace
***
## File `time_trace.py`:
Main module with decorator `track(<function>)`, that measures time it took function to finish and prints it to console (if tracing is enabled) or runs function without any modification (if tracing is disabled).

### Options
***
- `CHECK_INTERVAL: float` - Minimum time (in seconds) to wait before next check if file exists. Used to change state update frequency. The bigger the number, the lower the overhead but also after you change the file, it will take some time for module to notice.
  By default set to `5.0`.
- `BEAUTIFY_OUTPUT: bool` - Determines whether the output will be formatted for readability. 
  By default set to `True`.
- `BEAUTIFY_INDENT: str` - Set string for foramtting, that is appended before output as many times as the depth the function is nested in other traced functions.
  By default set to `" ⎪  "`.
- `BEAUTIFY_PREFIX_START: str` - Prefix for "function started" message.
  By default set to `" ┌> "`.
- `BEAUTIFY_PREFIX_FINISH: str` - Prefix for "function finished" message.
  By default set to `" └  "`.
- `MODE_FILENAME: str` - You can overwrite it to change the name of file, that is used to check if tracing is enabled.
  By default is set to `".TRACE_FUNCTIONS"`.
> [!WARNING]
> To rewrite `MODE_FILENAME` option, you have to create `.env` file and add there `MODE_FILENAME="<your_name>"`

### Usage
***
- Firstly, import time_tracing `import time_tracing`, `from time_tracing import *` or such
- After import you can change options listed above like `time_tracing.OPTION = NEW_VALUE` (check the warning above to modify `MODE_FILENAME`)
- Append `@time_tracing.trace` right before every function you want to track (decorate those functions with function `track()` from this module)
- Now, to turn tracing on/off you just need to create/delete the file specified by `MODE_FILENAME` (or you can run `python3 time_tracing.py --enable`/`python3 time_tracing.py --disable` resp.)

### Example
***
#### your_file.py
```python
# other imports
import os
import time
import random

# import the module
import time_tracing

# change options
time_tracing.CHECK_INTERVAL = 3.0
time_tracing.BEAUTIFY_PREFIX_START = " ┌-----> "

@time_tracing.trace # add the function to be traced
def dummy_function(cycles):
    something = 0
    for i in range(cycles):
        something += i
        something -= i

@time_tracing.trace # add the function to be traced
def function_that_calls_function(count):
    if count != 0:
        function_that_calls_function(count - 1)
        function_that_calls_function(count - 1)
    else:
        a = 1231
        a = a**3//123
        dummy_function(a)

dummy_function(random.randint(1,100000000))
function_that_calls_function(3)

while 1:
    dummy_function(random.randint(1,1000000))
    time.sleep(1)
```
***
#### .env
```.env
MODE_FILENAME=".example_filename"
```
***
#### run (shell)
```shell
$ python3 your_file.py
```
***
#### enable/disable profiling (works while the code is running) (shell)
```shell
$ python3 time_tracing.py --enable
```
```shell
$ python3 time_tracing.py --disable
```
## Requirements:
***
- Python (>= 3.10 recommended)
- dotenv (can install by running `$ pip install -r requirements.txt`)