# Example_of_package_module_structure


# Create a folder structure as this: py_pkg/reader/

reader module in reader package, has a class called Reader ```py_pkg/reader/reader.py ```

```python
# class has three methods: "init", "close" and "read".
class Reader: 
    #It takes a parameter "filename" which is used to open a file in read mode ('rt')
    def __init__(self, filename):
        # assigns the file object to an instance variable called "f".
        self.f = open(filename, 'rt')
    
    # close method calls the "close" method on the file object stored in the instance variable "f".
    def close(self):
        self.f.close()

    # The "read" method is used to read the contents of the file opened in the constructor. 
    def read(self):
        # returns the result of calling the "read" method on the file object stored in the instance variable "f".
        return self.f.read()
```
Test it

```python
>>> import reader.reader
>>> f = reader.reader.Reader('LICENSE.md')
>>> f.read()
'Copyright (c) 2023 Victor Ma\n\n## Blog Infrastructure...'
>>> f.close()
```
After import Reader class into the reader package by ```py_pkg/reader/__init__.py ```
```python
# from package reader's module reader.py, import Reader class.
from reader.reader import Reader
# Now Reader class is putting directly under reader package
```
Test it again
```python
>>> import reader # imported reader package
>>> f= reader.Reader('LICENSE.md')
>>> f.read()
'Copyright (c) 2023 Victor Ma\n\n## Blog Infrastructure...'
>>> f.close()
```
# subpackage structure as this: py_pkg/reader/compressed

Create a subpackage called compressed and a module gzipped.py

```python3
import gzip
import sys

opener  = gzip.open

# common way to check if the current script is being executed as the main program or if it is being imported as a module in another program.
if __name__ == '__main__':
    # opens a gzip file for writing using the first command-line argument passed to the script (sys.argv[1]) as the file path. 
    f = gzip.open(sys.argv[1], mode='wt')
    # writes a single string to the file, which is obtained by joining all the command-line arguments starting from the third (sys.argv[2:]) with a space character.
    f.write(' '.join(sys.argv[2:]))
    f.close()

```
Test each package, subpackage and module can be importted

```python
>>> import reader
>>> import reader.reader
>>> import reader.compressed
>>> import reader.compressed.gzipped
```

Test calling the module directly to create a gzipped file

```bash
$ python3 -m reader.compressed.gzipped test.gzip Content compressed by gzip
$ file test.gzip 
test.gzip: gzip compressed data, was "test.gzip", last modified: Sat Feb 18 20:03:35 2023, max compression, original size modulo 2^32 26
```
Just for the fun of it, create a bzipped module to handle bz2 file, and test

```python3
import bz2
import sys

opener  = bz2.open

if __name__ == '__main__':
    f = bz2.open(sys.argv[1], mode='wt')
    f.write(' '.join(sys.argv[2:]))
    f.close()
```
# Call the compressed helpper module from Reader class

Change the reader module like this:
```python
import os # used to get file extension, to decide which compressed moudle to call
# import both compressed module together
from reader.compressed import gzipped,bzipped

# creat a dict to map extension to their opener functions
extension_map = {
    '.gzip': gzipped.opener,
    '.bz2': bzipped.opener,
}

# class has three methods: "init", "close" and "read".
class Reader: 
    #It takes a parameter "filename" which is used to open a file in read mode ('rt')
    def __init__(self, filename):
        # get the filename's extension
        extension = os.path.splitext(filename)[1]
        # define opener function to choose from the dictrionary 
        # or fall back to the default python built-in fuction "open"
        opener = extension_map.get(extension, open)
        # assigns the file object to an instance variable called "f".
        self.f = opener(filename, 'rt')
```

Test it out

```python
>>> import reader.reader
>>> f = reader.Reader('test.gzip')
>>> f.read()
'Content compressed by gzip'
>>> f.close()
>>> f = reader.Reader('test.bz2')
>>> f.read()
'Content compressed by bz2'
>>> f.close()
```
