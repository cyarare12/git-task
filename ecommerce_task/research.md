# Research Answers

## 1. Python requests module

The requests module is a tool for Python. It helps send messages to websites.

People use it to ask websites for information. It can send different types of requests like GET, POST, PUT, DELETE.

Example code:
```python
import requests

response = requests.get('https://api.example.com/data')
print(response.json())
```

This asks a website for data and shows it.

## 2. JSON and XML data formats

### JSON

JSON is a way to write data. It is simple and easy to read. Computers can understand it quickly.

People use JSON to send data between apps and websites.

**Good things:**
1. Takes little space.
2. Easy to read and write.
3. Works well with websites.
4. Fast for computers.

**Bad things:**
1. No notes or comments allowed.
2. Cannot store dates easily.
3. Can be unsafe if not checked.
4. Hard for very big data.

### XML

XML is another way to write data. It uses tags like <name> and </name>. It is good for big, complex data.

People use XML to store and send data.

**Good things:**
1. Very flexible.
2. Good for complex data.
3. Easy to read.
4. Works everywhere.

**Bad things:**
1. Takes more space.
2. Slower for computers.
3. Harder to use in code.
4. Needs more power.

## 3. RESTful API

RESTful API is a way to connect apps. It uses web addresses to get data. It uses normal web commands.

Apps send requests to addresses. Server sends back data. Usually in JSON.

Example: GET /users gets user list. POST /users adds user.

Used to connect different apps online.

**Good things:**
1. Can handle many users.
2. Easy to learn.
3. Works with any system.
4. Can save data for speed.

**Bad things:**
1. May need many requests.
2. No built-in safety.
3. Limited by web rules.
4. May get wrong amount of data.