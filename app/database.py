'''
Wen Zhang, Kyle Lee, Danny Huang, Tracy Ye
Made-in-Nigeria
SoftDev
P00 - Move Slowly and Fix Things
Time Spent:
Target Ship Date: 2024-11-011
'''

import sqlite3

db = sqlite3.connect("data.db")
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS accounts(username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS blogs(owner TEXT, blogtitle TEXT)")
# c.execute("CREATE TABLE IF NOT EXISTS username_blogtitle(entryID INTEGER, entry TEXT)")
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
    c.execute(f"Insert INTO blogs VALUES ('{owner}', '{blogtitle}')")
    db.commit()
    db.close()

def addentry(owner, blogtitle, entryID, entry):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"Insert INTO {owner}_{blogtitle} VALUES ('{entryID}', '{entry}')")
    db.commit()
    db.close()

def viewAccount(username):
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute(f"SELECT password from accounts WHERE username = '{username}'")
    return c.fetchall()

def viewAll():
    db = sqlite3.connect("data.db")
    c = db.cursor()
    c.execute("SELECT * FROM accounts")
    return c.fetchall()