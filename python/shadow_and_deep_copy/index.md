# Shadow_and_deep_copy


In Python, the copy() method of a list creates a ***shallow copy*** of the list, which means that it creates a new list with a new memory address, but the new list contains references to the same objects as the original list. This means that changes made to the objects in the new list will also  affect the objects in the original list, and vice versa.

```python
>>> original_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
>>> new_list = original_list.copy()
>>> new_list[0][0] = 10
>>> print(original_list)
[[10, 2, 3], [4, 5, 6], [7, 8, 9]]
>>> print(new_list)
[[10, 2, 3], [4, 5, 6], [7, 8, 9]]
```
As you can see, the modification to the first element of new_list also affects the corresponding element in the original_list. This is because both lists contain references to the same nested list object.

If you need to create a new list that is independent of the original list, you can use the ***copy.deepcopy()*** method of the copy module, as shown below:
```python
>>> import copy
>>> original_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
>>> new_list = copy.deepcopy(original_list)
>>> new_list[0][0] = 10
>>> print(original_list)
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
>>> print(new_list)
[[10, 2, 3], [4, 5, 6], [7, 8, 9]]
```
The reason for having both shallow and deep copies is that they are useful in different situations. Shallow copies are faster to create and use less memory, which makes them a good choice when you want to create a copy of an object that you don't intend to modify. Deep copies, on the other hand, are slower to create and use more memory, but they create an independent copy of the object, which is important when you want to modify the copy without affecting the original object.

In general, ***you should use a shallow copy when you only need to create a new object that is a copy of the original, and you don't intend to modify it.*** If you need to modify the copy without affecting the original, or if the original object contains nested objects that you want to copy as well, you should use a deep copy.

In Python,***a copy is automatically deep when it involves immutable objects such as numbers, strings, and tuples.*** Immutable objects cannot be changed once they are created, so there is no need to create a new copy of them when they are used in a new object.

