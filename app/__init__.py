'''
Wen Zhang, Kyle Lee, Danny Huang, Tracy Ye
Made-in-Nigeria
SoftDev
P00 - Move Slowly and Fix Things
Time Spent:
Target Ship Date: 2024-11-011
'''

# import necessary

import sqlite3
import csv
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash


import database

# flask hosting base

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    return render_template("main.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        if request.method == "POST":
            username = request.form['username']
            password = request.form['pw']
            user = database.viewAccount(username)
            
            if user and len(user) > 0:
                flash("Username already exists. Please choose a different username.")
                return redirect(url_for('signup'))
            else:
                database.addAccount(username, password)
                flash("Account created successfully. Please log in.")
                return redirect(url_for('login'))
        return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    
    return render_template("signup.html")

@app.route("/user", methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html", uname=session['username'], passw=database.viewAccount(session['username'])[0][0])
    else:
        if request.method == "POST":
            username = request.form['username']
            password = request.form['pw']
            user = database.viewAccount(username)
            if user and len(user) > 0 and password == user[0][0]:
                session['username'] = username
                return render_template("dashboard.html", uname=username, passw=password)
            else:
                flash("Invalid credentials. Please try again.")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@app.route("/edit", methods=['GET', 'POST'])
def edit_page():
    return render_template("edit_page.html")

@app.route("/create", methods=['GET', 'POST'])
def create_page():
    if 'username' in session:
        if request.method =="POST":
            database.addBlog(session['username'], request.form['blog_title'])
            return redirect(url_for('dashboard'))
        return render_template("create_page.html", uname = session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/view", methods=['GET', 'POST'])
def view():
    if 'username' in session:
        blogs = database.get_blog()
        owners = []
        blogtitles = []
        blogIDs = []
        blogEntries = []
        for (owner, blogtitle), entries in blogs.items():
            owners.append(owner)
            blogtitles.append(blogtitle)
            if entries:
                for entryID, entry in entries:
                    blogIDs.append(entryID)
                    blogEntries.append(entry)
        return render_template("view.html", owners=owners, blogtitles=blogtitles, blogIDs=blogIDs, blogEntries=blogEntries)
    else:
        return redirect(url_for('login'))
    
@app.route("/addEntry", methods=['GET', 'POST'])
def add():
    if 'username' in session:
        if request.method =="POST":
            database.addentry(session['username'], request.form['blog_title'], request.form['entryTitle', request.form['entryContent']])
            return redirect(url_for('view'))
        return render_template("add.html", uname = session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username')
    return redirect(url_for('root'))

if __name__ == "__main__": 
    app.debug = True 
    app.run()