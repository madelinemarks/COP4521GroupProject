import mysql.connector
from mysql.connector import connect, Error

sitedb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pythongroup"
)

cur = sitedb.cursor()

cur.execute("CREATE TABLE Users(Username VARCHAR(30) NOT NULL UNIQUE, FirstName VARCHAR(30), LastName VARCHAR(30), "
            "DOB DATE, Pass VARCHAR(255))")
cur.execute("CREATE TABLE Textbooks(Title VARCHAR(500), ISBN VARCHAR(50) PRIMARY KEY, Retail FLOAT, Subj VARCHAR(50))")
cur.execute("CREATE TABLE Listings(Title VARCHAR(500), ISBN VARCHAR(50), Asking FLOAT, HighestBid FLOAT)")
cur.execute("CREATE ROLE 'administrator', 'standard'")
