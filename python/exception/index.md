# Exception


# Exception

Mechanism for interrupting normal program flow and continuing in surrounding context.

1. event is raising an exception
1. handling an exception with exception handler
1. unhandled exceptions cause termination
1. Exception objects transferred from event to handler

Exception are ubiquitous in Python compare with other programing languages.

# exceptional.py with unhandled exception
```python
DIGIT_MAP = {
    'zero':  '0',
    'one':   '1',
    'two':   '2',
    'three': '3',
    'four':  '4',
    'five':  '5',
    'six':   '6',
    'seven': '7',
    'eight': '8',
    'nine':  '9',
}

def convert(s):
    number = ''
    for token in s:
        number += DIGIT_MAP[token]
    x = int(number)
    return x
```
Now let's make a good call and an exception
```python
>>> from exceptional import convert
>>> convert("one three two".split())
132
>>> convert("seventeen".split())
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/vma/decmaxn.github.io/exceptional.py", line 17, in convert
    number += DIGIT_MAP[token]
KeyError: 'seventeen'
```
# Handle KeyError and TypeError with error code
```python
def convert(s):
    try:
        number = ''
        for token in s:
            number += DIGIT_MAP[token] # Exception is raised
        x = int(number) # Skipped when exception is raised
        print(f"Conversion succeeded! x = {x}") # Skipped when exception is raised
    except KeyError: # Program jumped to here when this exception is raised
        print("Conversion failed!")
        x = -1
    except TypeError: # Program jumped to here when this exception is raised
        print("Conversion failed!")
        x = -1
    return x
```
test
```python
>>> from exceptional import convert
>>> convert("one two three".split())
Conversion succeeded! x = 123
123
>>> convert("seventeen".split())
Conversion failed!
-1
>>> convert(123)
Conversion failed!
-1
```


# Programmer Errors
Programmer Errors should not be caught at runtime, etc. IndentationError, SyntaxError and NameError
```python
def convert(s):
    """Convert a string to an integer."""
    x = -1
    try:
        number = ''
        for token in s:
            number += DIGIT_MAP[token]
        x = int(number)
    except (KeyError, TypeError): # empty block is not permitted and can be solved by adding pass statement as no-op
    return x
```

# Accessing Exception Objects
```python
import sys

DIGIT_MAP =  . . .

def convert(s):
    try:
        number = ''
        for token in s:
            number += DIGIT_MAP[token]
        return int(number)
    except (KeyError, TypeError) as e: # Use as keyword
        print(f"Conversion error: {e!r}", #Print error message
              file=sys.stderr)
        return -1
```
Test
```python
>>> from exceptional import convert
>>> convert("seventeen".split())
Conversion error: KeyError('seventeen')
-1
>>> convert(123)
Conversion error: TypeError("'int' object is not iterable")
-1
```
# Re-raising Exceptions and clean up action
> Much better and altogether more Pythonic is to forget about error return codes completely and go back to raising an exception from convert. Instead of returning an un‑Pythonic error code, we can simply omit our error message and re‑raise the exception object we're currently handling. This can be done by replacing the return a ‑1 with raise at the end of our exception handling block. Without a parameter, raise simply re‑raises the exception that is being currently handled.
```python
import os
import sys

def make_at(path, dir_name):
    original_path = os.getcwd()
    os.chdir(path)
    try:
        os.mkdir(dir_name)
    except OSError as e:
        print(e, file=sys.stderr)
        raise # Re-raise exception so errors are not passed silently
    finally:  # Clean up action no matter mkdir works or not
        os.chdir(original_path) # try-block terminates
```
