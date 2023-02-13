---
title: "Function"
date: 2023-02-12T19:09:37-05:00
draft: false
tags: ["coding","python","course"]
---

# Simple function

```python
def greeting(name):   # order matters, define first
    print("Hello", name)

#main program
input_name = input("Enter your name:\n")
greeting(input_name)
```
# Scope
The input_name is a global var and has global scope,  
```
# name is not defined - cause it's defined and only avaible in the func
# print("Thanks", name)
print("Thanks", input_name) # input_name is defined outside of func
```
This greeting_global function uses a global var
```python
def greeting_global(): # define func without var
    print("Hello again", input_name) # refer to a global var

greeting_global()
```
# Return and main func to orginzing

```python
def greeting_return(): 
    return "Retruned? Hello, " + input_name # Return a value instead

def main(): # main func to orgnize the code
    retruned = greeting_return()
    print(retruned)

main()
```

# Examle
```python
import random

def roll_dice():
    dice_total =  random.randint(1,6) + random.randint(1,6) # maybe 1,12 is ok too
    return dice_total

#main program
def main():
    player1 = input("Enter player 1 name:\n")
    player2 = input("Enter player 2 name:\n")

    roll1= roll_dice()
    roll2= roll_dice()

    print(player1, " rolled", roll1) 
    print(player2, " rolled", roll2) 

    if roll1 > roll2:
        print(player1, 'wins')
    elif roll1 < roll2:
        print(player2, 'wins')
    else:
        print('tie')

main()
```
# organize Weather program
[Reference](/python/venv_and_api#Api_call_example)