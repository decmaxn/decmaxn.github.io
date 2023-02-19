---
title: "Concise_form"
date: 2023-02-13T17:32:15-05:00
draft: false
tags: ["coding","python","tips"]
---

# one liner for loop
Instead of:

```python
>>> m = []
>>> for i in range(10):
...     m.append(i)
... 
>>> m
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```
do
```python
>>> [i for i in range(10)]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> {"index"+str(i): i*2 for i in range(3)}
{'index0': 0, 'index1': 2, 'index2': 4}
```

# one liner condition
Instead of:

```python
>>> done = False
>>> if done:
...     a =1
... else:
...     a =2
... 
>>> a
2
```
do
```python
>>> a = 1 if done else 2
>>> a
2
```

# one liner condition plus for loop
Instead of:

```python
>>> l = []
>>> for i in range(10):
...     if i%2 == 0:
...             l.append(i*2)
... 
>>> l
[0, 4, 8, 12, 16]
```
do
```python
>>> [i*2 for i in range(10) if i%2 ==0]
[0, 4, 8, 12, 16]
>> {"index"+str(i): i*2 for i in range(10) if i%2 ==0}
{'index0': 0, 'index2': 4, 'index4': 8, 'index6': 12, 'index8': 16}
```

# enumerate automatically for indexing
Instead of:

```python
>>> count = 0
>>> l = [1,2,3,4]
>>> for data in l:
...     if count == 2:
...             data += 1
...     l[count]=data
...     count += 1
... 
>>> l
[1, 2, 4, 4]
```
do
```python
>>> l = [1,2,3,4]
>>> for index, data in enumerate(l):
...     if index == 2:
...             data += 1
...     l[index] = data
... 
>>> l
[1, 2, 4, 4]
```


# Zip to loop together
Instead of:

```python
>>> name = ["a", "b", "c"]
>>> number = [1,2,3]
>>> d = []
>>> d= {}
>>> for i in range(3):
...     d[name[i]] = number[i]
... 
>>> d
{'a': 1, 'b': 2, 'c': 3}
```
do
```python
>>> for n, b in zip(name, number):
...     d[n] = b
... 
>>> d
{'a': 1, 'b': 2, 'c': 3}
```

# reverse & reversed
Instead of 
```python
>>> number
[1, 2, 3]
>>> _number = []
>>> for i in range(len(number)):
...     _number.append(number[-1-i])
... 
>>> _number
[3, 2, 1]
```
do
```python
>>> _number
[3, 2, 1]
>>> [_number[-1-i] for i in range(len(_number))]
[1, 2, 3]
```
or
```python
>>> _number
[1, 2, 3]
>>> _number.reverse()
>>> _number
[3, 2, 1]
```
or 
```python
>>> _number
[1, 2, 3]
>>> [i for i in reversed(_number)]
[3, 2, 1]
```

# slice operator
The slice operator in Python is a powerful feature that allows you to extract a range of elements from a sequence (such as a list, tuple or string). The syntax for the slice operator is [start:stop:step], where start is the index of the first element to be included, stop is the index of the first element to be excluded, and step is the distance between each element to be included.
```python
>>> number
[1, 2, 3]
>>> number[::-1]
[3, 2, 1]
```
If start is not specified, it defaults to 0, and if stop is not specified, it defaults to the length of the sequence. If step is not specified, it defaults to 1. By using a negative value for step, you can extract elements from the sequence in reverse order.

Using the slice operator, you can easily manipulate and extract data from sequences without the need for more complex loops and conditional statements.
