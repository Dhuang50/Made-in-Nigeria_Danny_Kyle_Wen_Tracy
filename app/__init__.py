'''
Wen Zhang, Kyle Lee, Danny Huang, Tracy Ye
Made-in-Nigeria
SoftDev
P00 - Move Slowly and Fix Things
Time Spent:
Target Ship Date: 2024-11-04
'''

# import necessary

import sqlite3
import csv
import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect

import database

# flask hosting base

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    return render_template("main.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route("/user", methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")

@app.route("/edit", methods=['GET', 'POST'])
def edit_page():
    return render_template("edit_page.html")

@app.route("/create", methods=['GET', 'POST'])
def create_page():
    return render_template("create_page.html")

@app.route("/view", methods=['GET', 'POST'])
def view():
    render_template("view.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    return redirect(url_for('root'))

if __name__ == "__main__": 
    app.debug = True 
    app.run()
