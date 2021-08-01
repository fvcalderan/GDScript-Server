# GDScript-Server
Simple GDScript server using Python and Flask.

```
  __                _     _
 / _|_   _____ __ _| | __| | ___ _ __ __ _ _ __
| |_\ \ / / __/ _` | |/ _` |/ _ \ '__/ _` | '_ \
|  _|\ V / (_| (_| | | (_| |  __/ | | (_| | | | |
|_|   \_/ \___\__,_|_|\__,_|\___|_|  \__,_|_| |_|

BSD 3-Clause License
Copyright (c) 2021, Felipe V. Calderan
All rights reserved.
See the full license inside LICENSE file
```

## How it works
It receives a GDScript as input, runs it on a headless linux version of Godot
with `godot -s`, then displays `stdout` and `stderr` contents to the user.

## Features

- Manages time limit for each script running
- Prohibit the use of dangerous function calls
- Display error messages to the user

## Prerequisites
For local execution, it requires `Flask`. Additionally, if it's ran on Heroku,
`gunicorn` is also required.

## How to setup the server locally
Uncomment the following lines at the end of `gdscript_server.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```
then, run the program with: `python3 gdscript_server.py`. By default it should
be opened in `127.0.0.1:5000`.

## How to deploy the server on Heroku
Create a new Heroku app, sync it with your GDScript-Server GitHub repository,
enable the automatic build upon commit and build the project. There are other
ways to achieve the same thing, I recommend reading Heroku's documentation.

## How to access the server as an user
You can either access the home page through a web-browser (including text-based
ones like LINKS) or user cURL:
```bash
curl -X POST -F "script=$(cat example_script.gd)" "IP:PORT"
```
