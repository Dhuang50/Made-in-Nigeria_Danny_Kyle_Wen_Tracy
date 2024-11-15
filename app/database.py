'''
Wen Zhang, Kyle Lee, Danny Huang, Tracy Ye
Made-in-Nigeria
SoftDev
P00 - Move Slowly and Fix Things
Time Spent:
Target Ship Date: 2024-11-07
'''

import sqlite3

# Create or connect to the main database file
db = sqlite3.connect("data.db")
c = db.cursor()

# Create accounts table if it doesn't already exist
c.execute('''
          CREATE TABLE IF NOT EXISTS accounts(
              username TEXT PRIMARY KEY, 
              password TEXT NOT NULL
              )
          '''
        )

# Create blogs table to store blog metadata if it doesn't already exist
c.execute('''
          CREATE TABLE IF NOT EXISTS blogs(
              owner TEXT NOT NULL, 
              blogtitle TEXT NOT NULL, 
              entryCount INTEGER NOT NULL)
          '''
        )
db.commit()
db.close()

# Function to add a new account to the accounts table
def addAccount(username, password):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"INSERT INTO accounts VALUES ('{username}', '{password}')")
    db.commit()
    db.close()

# Function to add a new blog entry with title, initializing entry count to 0
def addBlog(owner, blogtitle):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"INSERT INTO blogs VALUES ('{owner}', '{blogtitle}', 0)")
    # Create a unique table for each blog with columns for entry ID, title, and content
    c.execute(f"CREATE TABLE IF NOT EXISTS '{owner}{blogtitle}'(entryID INTEGER, entryTitle TEXT, entry TEXT)")
    db.commit()
    db.close()

# Function to add a new entry to a specific blog
def addentry(owner, blogtitle, entryTitle, entry):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    # Get current entry count for the blog to determine the new entry ID
    c.execute(f"SELECT entryCount FROM blogs WHERE owner = '{owner}' AND blogtitle = '{blogtitle}'")
    num = c.fetchall()[0][0]
    entryID = int(num) + 1
    # Update entry count in blogs table and add new entry in the respective blog table
    c.execute(f"UPDATE blogs SET entryCount = {entryID} WHERE owner = '{owner}' AND blogtitle = '{blogtitle}'")
    c.execute(f"INSERT INTO '{owner}{blogtitle}' VALUES ('{entryID}', '{entryTitle}', '{entry}')")
    db.commit()
    db.close()

# Function to check if an account with a given username exists
def accountExists(username):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT * FROM accounts WHERE username = '{username}'")
    return c.fetchall() != []

# Function to retrieve account information (password) for a specific username
def viewAccount(username):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT password FROM accounts WHERE username = '{username}'")
    return c.fetchall()

# Function to retrieve all accounts in the accounts table
def viewAll():
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute("SELECT * FROM accounts")
    return c.fetchall()

# Function to get a list of all blogs and their entries
def get_blog():
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute("SELECT owner, blogtitle FROM blogs")
    blogs = c.fetchall()
    blogEntries = {}
    # Retrieve entries for each blog, handling cases where blog tables might not exist
    for owner, blogtitle in blogs:
        table_name = f"{owner}{blogtitle}"
        try:
            c.execute(f"SELECT entryID, entry FROM {table_name}")
            entries = c.fetchall()  
            blogEntries[(owner, blogtitle)] = entries
        except sqlite3.OperationalError: 
            blogEntries[(owner, blogtitle)] = []
    db.close()
    return blogEntries

# Function to retrieve all entries for a specific blog
def get_entries(username, blogtitle):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT * FROM '{username}{blogtitle}'")
    return c.fetchall()

# Function to retrieve a single entry by ID for a specific blog
def get_entry(username, blogtitle, entryID):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT * FROM '{username}{blogtitle}' WHERE entryID = {entryID}")
    entry = c.fetchall()
    return entry

# Function to edit a specific blog entry's title and content
def edit_entry(username, blogtitle, entryID, entryTitle, entry):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"UPDATE '{username}{blogtitle}' SET entryTitle = '{entryTitle}' WHERE entryID = {entryID}")
    c.execute(f"UPDATE '{username}{blogtitle}' SET entry = '{entry}' WHERE entryID = {entryID}")
    db.commit()
    db.close()
