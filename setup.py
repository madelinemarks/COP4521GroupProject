import sqlite3
from datetime import date 

conn = sqlite3.connect('siteData.db')   # do we need more than one database?
print("Opened database successfully")

# we will definitely need to add more tables and change data types, placeholders for now
conn.execute('CREATE TABLE Users(Username TEXT, FirstName TEXT, LastName TEXT, DOB DATE, Pass TEXT, UserType TEXT)') #  we should probably store passwords differently, how to store Date?
conn.execute('CREATE TABLE Textbooks(Title TEXT, ISBN TEXT PRIMARY KEY, Retail REAL, Subj TEXT)')
conn.execute('CREATE TABLE Listings(Title TEXT, ISBN TEXT PRIMARY KEY, Asking REAL, HighestBid REAL)')
