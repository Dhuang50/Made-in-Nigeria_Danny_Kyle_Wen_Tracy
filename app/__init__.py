'''
Wen Zhang, Kyle Lee, Danny Huang, Tracy Ye
Made-in-Nigeria
SoftDev
P00 - Move Slowly and Fix Things
Time Spent:
Target Ship Date: 2024-11-01
'''

# Import necessary libraries
import sqlite3
import csv
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
import database

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(32)  # Set a secret key for session management

# Root route, redirects to dashboard if logged in, else shows main page
@app.route("/", methods=['GET', 'POST'])
def root():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template("main.html")

# Login route, handles both GET and POST requests
@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        # Check for successful signup notification
        if session.pop('signup_success', None):
            flash("Account created successfully! Please log in.")
        elif request.method == "POST":
            # Retrieve username and password from form
            username = request.form['username']
            password = request.form['pw']
            user = database.viewAccount(username)
            
            # Check if account exists
            if len(user) > 0:
                stored_password = user[0][0]
                # Verify password
                if password == stored_password:
                    session['username'] = username
                    return redirect(url_for('dashboard'))
                else:
                    flash("Incorrect password. Please try again.")
            else:
                flash("No account found with that username. Please sign up.")
        
        return render_template("login.html")

# Signup route, handles account creation
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        # Retrieve username and password from form
        username = request.form['username']
        password = request.form['pw']
        # Check if username already exists
        if database.accountExists(username):
            flash("Username already exists. Please choose a different username.")
        else:
            # Add new account to the database and redirect to login
            database.addAccount(username, password)
            session['signup_success'] = True
            return redirect(url_for('login'))
    
    return render_template("signup.html")

# Dashboard route, shows user info if logged in
@app.route("/user", methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        user = database.viewAccount(session['username'])
        return render_template("dashboard.html", uname=session['username'])
    else:
        return redirect(url_for('login'))

# Edit page route, allows users to edit blog entries
@app.route("/edit", methods=['GET', 'POST'])
def edit_page():
    if 'username' in session:
        # Retrieve entry information for editing
        entry = database.get_entry(session['username'], session['blogTitle'], session['entryID'])
        if request.method =="POST":
            # Save edited entry
            database.edit_entry(session['username'], session['blogTitle'], session['entryID'], request.form['entryTitle'], request.form['entryContent'])
            return redirect(url_for('view'))
        print("_________________________")
        print(entry)
        return render_template("edit_page.html", entry=entry)
    else:
        return redirect(url_for('login'))

# Route for creating a new blog
@app.route("/create", methods=['GET', 'POST'])
def create_page():
    if 'username' in session:
        if request.method =="POST":
            # Add a new blog to the database
            database.addBlog(session['username'], request.form['blog_title'])
            flash(f"Blog {request.form['blog_title']} Created Successfully.")
            return redirect(url_for('view'))
        return render_template("create_page.html", uname=session['username'])
    else:
        return redirect(url_for('login'))

# View route, shows all blogs
@app.route("/view", methods=['GET', 'POST'])
def view():
    if 'username' in session:
        blogs = database.get_blog()
        owners = []
        blogtitles = []
        # Collect owner and title for each blog
        for (owner, blogtitle) in blogs:
            owners.append(owner)
            blogtitles.append(blogtitle)
        return render_template("view.html", owners=owners, blogtitles=blogtitles, blogs=blogs, user=session['username'])
    else:
        return redirect(url_for('login'))

# View specific blog route, allows users to view entries within a blog
@app.route("/view/<owner>/<blogtitle>", methods=['GET', 'POST'])
def viewBlog(owner, blogtitle):
    if 'username' in session:
        session['author'] = owner
        session['blogTitle'] = blogtitle
        entries = database.get_entries(owner, blogtitle)
        edit = False
        # Enable edit option if the user is the author
        if session['author'] == session['username']:
            edit = True
        if request.method == "POST":
            # Set entry ID for editing
            session['entryID'] = request.form.get('entryID')
            return redirect(url_for('edit_page'))
        return render_template("viewBlog.html", owner=owner, blogtitle=blogtitle, entries=entries, edit=edit)
    else:
        return redirect(url_for('login'))

# Route for adding a new entry to a blog
@app.route("/addEntry", methods=['GET', 'POST'])
def add():
    if 'username' in session:
        if request.method =="POST":
            # Add a new entry to the current blog
            database.addentry(session['username'], session['blogTitle'], request.form['entryTitle'], request.form['entryContent'])
            flash("New Entry Added Successfully.")
            return redirect(url_for('view'))
        return render_template("add.html", uname=session['username'], blogtitle=session['blogTitle'])
    else:
        return redirect(url_for('login'))

# Logout route, clears the session and logs the user out
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('root'))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8080)
