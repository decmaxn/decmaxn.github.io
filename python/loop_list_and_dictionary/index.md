# Loop_list_and_dictionary


# Two loop variables in one loop with items method of dictionary

This way, you can get both the key and value of each key value pair at the same time

```python
Chars = {
    'letters': 'abcde...',
    'numbers': 1234567890,
    'special': '!@#$%...'
}

for key, value in Chars.items():  # items method of dictionary
    print(key,'includes',value)
```

# Dictionary represent object

```python
contacts = {  # use dictionary for object
    "number": 4,
    "students": [  #List of dictionaries
        {"name":"Sarah", "email":"sarah@email.com"},
        {"name":"Harry", "email":"harry@email.com"},
        {"name":"Hermione", "email":"hermione@email.com"},
        {"name":"Ron", "email":"ron@email.com"}
    ]
}

for student in contacts.get('students'):  # student represents each item in students list
    print(student.get('email'))
```

# JSON - Javascript Object Notation
some api website return raw data in json format instead of html file.
```python
import requests

response = requests.get('http://api.open-notify.org/astros.json')

# print(response) Response [200]

json = response.json() # requests module's json method

# print(json) the whole json response

for person in json['people']:
    print(person['name'])
```
