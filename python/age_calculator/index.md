# Simple math caculation


# Install Python and Hello world
Make sure you have it installed
```bash
$ python3 --version
Python 3.8.10
$ python3
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
$ cat hello_world.py 
print("Hello world!")
$ python3 hello_world.py 
Hello world!
```
#  extension for vscode
After installed ms-python.python vscode extention and select Python interpreter（I never know that I have python2 pre-installed too), I can now click on run button to run the .py file like the one created above.

# Using Interpreter
You know need print to see the output here

```python
>>> length=2
>>> width=5
>>> area = length*width
>>> area
10
>>> 
```

# Basic data types and functions

Built-in types are installed together with Python:

|   |Order   |Change   |Duplicate   |define   |
|---|---|---|---|---|
|List |ordered   |changeable   |Allows   | []  |
|Tuple   | ordered  |unchangeable   | Allows  |  () |
|Set   |unordered and unindexed  |unchangeable*   |No duplicate   | {}  |
|Dictionary   |ordered**  |changeable  |No duplicate   | {}  |

*Set items are unchangeable, but you can remove and/or add items whenever you like.

**As of Python version 3.7, dictionaries are ordered. In Python 3.6 and earlier, dictionaries are unordered.

```python
amount = 20 
tax = .13 #Remember the primitive Data Types
total = amount + amount*tax
print(total) # print function will print the argument

print(int(22.6)) # int function convert float to int
print(float(10)) # float function convert int to float

blog_name = "Victor's blog" #Using single quotes or double quotes to identify str
print(blog_name) # print out doesn't have quotes becasue it's only to tell python 
greeting = "Welcome to" 
print(greeting + " " + blog_name) # Concatenate two string, and a space

your_blog = input("what is your blog name\n") #Input function
print(greeting + " " + your_blog)
```

# app convert nubmer to string

```python
your_age = input("What is your age?\n") #43
# decades = your_age/10 TypeError: unsupported operand type(s) for //: 'str' and 'int'
# decades = int(your_age)/10 # this operator get a fload or whole number
decades = int(your_age)//10 # input result is a str
print(decades)
years = int(your_age)%10 # Modulus operator
print(years)
# print("You are "+decades+"Decades and"+years+"years old.") TypeError: can only concatenate str (not "int") to str
print("You are",decades,"Decades and",years,"years old.",sep=" ") # another way of print
```
