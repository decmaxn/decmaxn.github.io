# Dictionary


# Compare with javascript object

In Python, dictionaries are data structures that store key-value pairs. Each key maps to a unique value within the dictionary, and you can use the keys to look up the corresponding values. For example:

```python
person = {'name': 'John', 'age': 32, 'city': 'New York'}
print(person['name'])  # Output: John
```
In JavaScript, objects serve a similar purpose as dictionaries in Python. They also store key-value pairs, and you can use the keys to look up the corresponding values. For example:
```javascript
const person = {name: 'John', age: 32, city: 'New York'};
console.log(person.name);  // Output: John
```
However, their ways to refer to items different as shown above.

Similarly, lists in Python and arrays in JavaScript are similar.

# Dictionary

```python
acronyms = {
    'LOL': 'laugh out loud',
    'IDK': "I dont' know", # note the different quotes to avoid problem
    'TBH': 'to be honest'
}

print(acronyms)

print(acronyms['IDK']) # Refer to one item
acronyms['TBH'] = "honestly"  #Update an item
print(acronyms['TBH'])

# print(acronyms['BTW']) KeyError: 'BTW' when there is no such a key
print(acronyms.get('BTW')) # Get None if the key doesn't exist

acronyms['BTW'] = "by the way" # Add an item if it's not exist
print(acronyms['BTW'])

del acronyms['LOL'] # Delete
```
# None Type
None is a type that represents the absence of a value, it also evaluates to False

```python
if acronyms.get('BTW'):   # Use what None type evaluates to for condition
    print(acronyms.get('BTW'))
else:
    print("key BTW is not there")

if acronyms.get('LOL') != None:   # Use None type itself to compare
    print(acronyms.get('LOL'))
else:
    print("key LOL is not there")
```


