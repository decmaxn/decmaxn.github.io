---
title: "Venv and API call"
date: 2023-02-12T17:12:35-05:00
draft: false
---

# [Venv](https://docs.python.org/3/library/venv.html)

Creating virtual env, make sure to slect vscode python interpreter after.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install requests
$ deactivate 
```
# Api call example
First sign up at [Open weather](https://home.openweathermap.org/api_keys) and get an API key.

```python
import requests

api_key = "<tobereplaced>"
city = "Beverly Hills"
lat = "34.0901"
lon = "-118.4065"
# Copy/paste from Open weatcher:"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}"

url = "https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&appid="+api_key+"&units=metric"

response = requests.get(url)
json = response.json()

# multiple levels of get method
description = json.get("weather")[0].get("description")
temp_min = json.get("main").get("temp_min")
temp_max = json.get("main").get("temp_max")
print("Today's weather is ",description)
print("temperature high at:",temp_max,"low at:",temp_min)
```