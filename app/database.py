'''
Wen Zhang, Kyle Lee, Danny Huang, Tracy Ye
Made-in-Nigeria
SoftDev
P00 - Move Slowly and Fix Things
Time Spent:
Target Ship Date: 2024-11-07
'''

import sqlite3

db = sqlite3.connect("data.db")
c = db.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS accounts(
              username TEXT PRIMARY KEY, 
              password TEXT NOT NULL
              )
          '''
        )
c.execute('''
          CREATE TABLE IF NOT EXISTS blogs(
              owner TEXT NOT NULL, 
              blogtitle TEXT NOT NULL, 
              entryCount INTEGER NOT NULL)
          '''
        )
db.commit()
db.close()


def addAccount(username, password):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"INSERT INTO accounts VALUES ('{username}', '{password}')")
    db.commit()
    db.close()

def addBlog(owner, blogtitle):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"Insert INTO blogs VALUES ('{owner}', '{blogtitle}', 0)")
    c.execute(f"CREATE TABLE IF NOT EXISTS '{owner}''{blogtitle}'(entryID INTEGER, entryTitle, entry TEXT)")
    db.commit()
    db.close()

def addentry(owner, blogtitle, entryTitle, entry):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT entryCount FROM blogs WHERE (owner = '{owner}' AND blogtitle = '{blogtitle}'")
    print(c.fetchall())
    entryID = c.fetchall()[0]+1
    c.execute(f"Insert INTO {owner}{blogtitle} VALUES ('{entryID}', '{entryTitle}', {entry}')")
    db.commit()
    db.close()

def accountExit(username):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT * from accounts WHERE username = '{username}'")
    return c.fetchall() != []

def viewAccount(username):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT password from accounts WHERE username = '{username}'")
    return c.fetchall()

def viewAll():
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT * from accounts")
    return c.fetchall()

def get_blog():
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute("SELECT owner, blogtitle FROM blogs")
    blogs = c.fetchall()
    blogEntries = {}
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


    

