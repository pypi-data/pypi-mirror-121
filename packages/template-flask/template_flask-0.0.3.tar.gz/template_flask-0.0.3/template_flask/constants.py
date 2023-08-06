REQUIREMENTS = [
    'flask',
    'flask_sqlalchemy',
    'flask_login',
    'flask_mail',
    'flask_wtf',
    'flask_debugtoolbar',
    'pytest',
    'pytest_cov'
]

INDEX_HTML = {
    1: ['<!DOCTYPE html>', False],
    2: ['<html lang="en">', False],
    3: ['<head>', False],
    4: ['\t<meta charset="UTF-8">', False],
    5: ['\t<title>NEW PROJECT: {fill}</title>', True],
    6: ['</head>', False],
    7: ['<body>', False],
    8: ['\t<h1>Welcome to your new project: {fill}</h1>', True],
    9: ['</body>', False],
    10: ['</html>', False]
}

CONFIG = {
    1: ['SECRET_KEY = """{fill}"""', True],
    2: ["SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'", False]
}

ROUTE = {
    1: ["from flask import render_template, redirect, url_for, session, flash", False],
    2: ["from {fill}_app import app", True],
    3: ["", False],
    4: ["@app.route('/')", False],
    5: ["@app.route('/home')", False],
    6: ["def index():", False],
    7: ["\treturn render_template('index.html')", False]
}

MODEL = {
    1: ["from datetime import datetime", False],
    2: ["from {fill}_app import db", True],
    3: ["", False],
    4: ["class Model(db.Model):", False],
    5: ["\tid = db.Column(db.Integer, primary_key=True)", False]
}

RUN = {
    1: ["from {fill}_app import app", True],
    2: ["", False],
    3: ["if __name__ == '__main__':", False],
    4: ["\tapp.run(debug=True)", False]
}

INIT = {
    1: ["from flask import Flask", False],
    2: ["from flask_sqlalchemy import SQLAlchemy", False],
    3: ["# from flask_login import ()", False],
    4: ["# from flask_mail import ()", False],
    5: ["# from flask_wft import ()", False],
    6: ["# from flask_debugtoolbar import ()", False],
    7: ["from {fill}_app.config import *", True],
    8: ["", False],
    9: ["app = Flask(__name__)", False],
    10: ["app.config['SECRET_KEY'] = SECRET_KEY", False],
    11: ["app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI", False],
    12: ["# app.config[''] = ''", False],
    13: ["# app.config[''] = ''", False],
    14: ["# app.config[''] = ''", False],
    15: ["# app.config[''] = ''", False],
    16: ["", False],
    17: ["db = SQLAlchemy(app)", False],
    18: ["", False],
    19: ["from {fill}_app import routes", True]
}

