# Condition_and_module


# Comparators

```python
>>> temp = 95  # Assignment
>>> temp == 85 # Comparator
False
>>> temp == 95
True
```

# Condition and logical operator

```python
temp = int(input("What is the temporature?\n"))

if temp <= 95 and temp >=45:  # AND Logical operators 
    print("Nice, go outside")  #indented code inside a "Code block"
    print("There is 4 spaces before this line insead of a tab") # Tab or 4 spaces
# print("There is 2 spaces before this line insead of a tab or  4 spaces") IndentationError
elif temp > 95:
    print("Too hot, stay inside")
else:
    print("Too cold, stay inside")

if temp > 95 or temp < 45:  # OR logical opeartor
    print("stay inside")
else:
    print("Go outside")

forcast = "rain"
if not forcast == "rain": # Not logical operator
    print("Go outside")
else:
    print("stay inside")

raining = True # Condition with Boolean Data type VAR
if raining:  # It's more like plain english
    print("Stay inside, it's raining")
```

# Modules

Not only built-in types are installed together with Python, [Python standard Library](https://docs.python.org/3/library/), etc. math, datetime, random, os, also get installed.

```python
import random

roll = random.randint(1,6) #Return a random integer N such that a <= N <= b. 

guess = int(input("What the computer rolls?\n"))

if roll == guess:
    print("You have guessed right, computer rolled a " + str(roll))
else:
    print("You lost, computer rolled a " + str(roll))
```

# Rock, Paper, Scissors game
```python
import random

computer = random.choice(["Rock","Paper","Scissors"]) # Return a random element from the non-empty sequence seq.

you = input("What do you play: Rock or Paper or Scissors\n")

if you == computer:
    print("TIE")
elif you == "Paper" and computer == "Rock":
    print("WIN")
elif you == "Rock" and computer == "Scissors":
    print("WIN")
elif you == "Scissors" and computer == "Paper":
    print("WIN")
else:
    print("LOSE")
```
