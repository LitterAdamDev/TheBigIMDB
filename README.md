# TheBigIMDB
**Objective**  
>The assignment is to create an application that scrapes data from [IMDB](https://www.imdb.com/chart/top/) and adjusts IMDB ratings based on some rules.


## How to start

### Clone the project
Project is ready to run (with some requirements)

```sh
$ mkdir Project
$ cd Project
$ git clone git@github.com:LitterAdamDev/TheBigIMDB.git .
```

### Virtual Environment
Create a virtual environment that uses Python and install the dependencies from the requirements file:
```sh
$ py -m pip install --user virtualenv
$ py -m venv env
$ .\env\Scripts\activate
$ py -m pip install -r requirements.txt
```

### Run a Development Server

Here's how you run the flask app from the terminal:
```sh
$ flask run
```

### Open in a Browser

Your running server will be visible at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## How to run unit tests
Here's how you run the tests from the terminal:
```sh
$ py test_app.py
```