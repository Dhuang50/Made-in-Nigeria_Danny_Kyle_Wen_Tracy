'''
Wen Zhang, Kyle Lee, Danny Huang, Tracy Ye
Made-in-Nigeria
SoftDev
P00 - Move Slowly and Fix Things
Time Spent:
Target Ship Date: 2024-11-04
'''

import sqlite3



db = sqlite3.connect("data.db")
c = db.cursor()

c.execute("CREATE TABLE accounts(username TEXT, password TEXT)")
c.execute("CREATE TABLE blogs(owner TEXT, blogtitle TEXT)")
c.execute("CREATE TABLE username_blogtitle(entryID INTEGER, entry TEXT)")


def addAccount(username, password):
    c.execute(f"INSERT INTO accounts VALUES ({username}, {password})")

def addBlog(owner, blogtitle):
    c.execute(f"Insert INTO blogs VALUES ({owner}, {blogtitle})")

def addentry(owner, blogtitle, entryID, entry):
    c.execute(f"Insert INTO {owner}_{blogtitle} VALUES ({entryID}, {entry})")
    
db.commit()
db.close()

