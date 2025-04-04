import os
import time
import argparse
import dotenv

from collections.abc import Callable

# Options (can be overwritten in main code)
CHECK_INTERVAL = 5.0               # minimum intervals of file checking to reduce overhead (in seconds)

BEAUTIFY_OUTPUT = True             # if you want to have output indents depending on function call depth
                                       # (probably doesn't work very well with async functions)
BEAUTIFY_INDENT = " ⎪  "           # indent for displaying function call depth
BEAUTIFY_PREFIX_START = " ┌> "     # prefix for beautifying ("function started" message)
BEAUTIFY_PREFIX_FINISH = " └  "    # prefix for beautifying ("function finished" message)
# ----------------------------------------

# Name of file, which contains data whether tracing is enabled or not (if file exists, the tracing is enabled,
#   otherwise, it is disabled)
# NOTE: The default name has no file type and is hidden, so it's unlikely, that it will have conflict name with
#   something else, besides, you can set the name to match the existing debug files
dotenv.load_dotenv()
_MODE_FILENAME = os.getenv("MODE_FILENAME", ".TRACE_FUNCTIONS")


__all__ = ['trace'] # Hide private functions for star import

# Variables for saving the state of tracing
_last_check_time = 0.0
_cached_running = False

# Variable for tracing how many functions are running at the moment to beautify output
# (I don't know how this will work with async functions)
_function_depth = 0

"""
Checks the value in the file
    - If the file exists, tracing is enabled.
    - If the file doesn't exist, tracing is disabled.
"""
def _is_running() -> bool:
    global _last_check_time, _cached_running
    current_time = time.time()

    # Only re-read the file if enough time has passed
    if current_time - _last_check_time >= CHECK_INTERVAL:
        _last_check_time = current_time

        # If file exists, tracing is turned on
        if os.path.isfile(_MODE_FILENAME):
            _cached_running = True
        else:
            _cached_running = False

    return _cached_running

"""
Decorator function for time tracing
    - If time tracing is enabled, prints debug information about the given function with given parameters.
    - If time tracing is disabled, calls the funtion without any decorating.
"""
def trace(tested_function: Callable) -> Callable:
    # Returns function name including its input parameters as string
    def func_name_str(f: Callable, args, kwargs) -> str:
        arg_list = list(map(str, args))                                  # add positional args
        arg_list += [f"{key}={str(val)}" for key, val in kwargs.items()] # add formatted keyword args

        return f"{f.__qualname__}({', '.join(arg_list)})"

    def wrapper(*args, **kwargs):
        if _is_running():
            global _function_depth

            print(f"{BEAUTIFY_INDENT * _function_depth + BEAUTIFY_PREFIX_START if BEAUTIFY_OUTPUT else ''}"
                  f"Function '{func_name_str(tested_function, args, kwargs)}'", end="")
            start_time = time.time()
            print(f" started (time: {start_time}).")
            _function_depth += 1

            tested_function(*args, **kwargs)

            _function_depth -= 1
            end_time = time.time()
            result_time = end_time - start_time
            print(f"{BEAUTIFY_INDENT * _function_depth + BEAUTIFY_PREFIX_FINISH if BEAUTIFY_OUTPUT else ''}"
                  f"Function '{func_name_str(tested_function, args, kwargs)}' "
                  f"finished (time: {end_time}) and took {result_time} seconds.")

        else:
            return tested_function(*args, **kwargs)

    return wrapper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Time tracing module')
    state_arg_group = parser.add_mutually_exclusive_group(required=True)
    state_arg_group.add_argument('-e', '--enable', dest='enable', action='store_true', help='enable profiling')
    state_arg_group.add_argument('-d', '--disable', dest='disable', action='store_true', help='disable profiling')
    args = parser.parse_args()

    if args.enable:
        try:
            with open(_MODE_FILENAME, 'x'):
                pass
        except FileExistsError:
            print("Error: Already enabled.")
    else:
        try:
            os.remove(_MODE_FILENAME)
        except FileNotFoundError:
            print("Error: Already disabled.")
