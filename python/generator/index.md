# Generator

# What is generator
Generators are a powerful tool in Python that allow you to create iterable objects on-the-fly. They are functions that use the yield statement instead of return to produce a sequence of values.

# Why we need generator

One of the main reasons why we need generators is that they are memory-efficient. When you create a list, for example, all the elements of the list are created and stored in memory at once. If the list is very large, this can consume a lot of memory. Generators, on the other hand, only generate one value at a time as you iterate over them, so they don't require as much memory.

# How generator works
Generators can also be more efficient in terms of computation time. Since they generate values on-the-fly, they can often avoid unnecessary calculations and terminate early if the result is already determined.

```python
>>> def need_return(init_value):
...     tmp = init_value
...     for item in range(300):
...         if item == tmp: # since item eq tmp,
...             tmp *= 2 # double tmp makes tmp always bigger than item
...             print("yeild a qualified item=%d from inside the generator" % item)
...             yield item  # Control goes out to caller
...             print("control back to the generator")
... 
>>> for i in need_return(10):
...     print("Outside caller received item=%d\n" % i)
... 
yeild a qualified item=10 from inside the generator
Outside caller received item=10

control back to the generator
yeild a qualified item=20 from inside the generator
Outside caller received item=20

control back to the generator
yeild a qualified item=40 from inside the generator
Outside caller received item=40

control back to the generator
yeild a qualified item=80 from inside the generator
Outside caller received item=80

control back to the generator
yeild a qualified item=160 from inside the generator
Outside caller received item=160

control back to the generator
```

# \_\_iter__ and \_\_next__ methods

When the Python interpreter encounters the yield keyword in a generator function, it automatically converts the generator function to a generator object and adds the __iter__() and __next__() methods to the object. The implementation of these methods is generated automatically by the Python interpreter and includes the necessary logic to control the generator's iteration and state.
