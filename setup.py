import sqlite3

conn = sqlite3.connect('siteData.db')   # do we need more than one database?
print("Opened database successfully")

# we will definitely need to add more tables and change data types, placeholders for now
conn.execute('CREATE TABLE Users(Username TEXT, FirstName TEXT, LastName TEXT, DOB, Pass TEXT)') #  we should probably store passwords differently, how to store Date?
conn.execute('CREATE TABLE Textbooks(Title TEXT, ISBN TEXT, Retail REAL, Subj TEXT)')
conn.execute('CREATE TABLE Listings(Title TEXT, ISBN TEXT, Asking REAL, HighestBid REAL)')