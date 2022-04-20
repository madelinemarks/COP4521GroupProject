from flask import Flask, render_template, request, url_for, redirect, flash
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
import sqlite3 as sql
import sys
import time
import stripe
app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = environ.get("STRIPE_PUBLIC_KEY")
app.config['STRIPE_PRIVATE_KEY'] = environ.get("STRIPE_PRIVATE_KEY")
stripe.api_key = app.config['STRIPE_PRIVATE_KEY']

@app.route('/')
def home():
    return render_template('index.html', template_folder='Templates')

@app.route('/signup')
def signup():
    return render_template('signup.html', template_folder='Templates')

@app.route('/addUser', methods = ['POST', 'GET'])
def addUser():
        if request.method == 'POST':
            try:
                usrnm   = request.form['usrnm']
                frst    = request.form['frst']
                last    = request.form['last']
                dob     = request.form['dob']
                pswd    = request.form['pswd']
                usrtype = request.form['usrtype']
                confirm = request.form['confirm']

                if pswd != confirm:
                    msg = "Passwords do not match" # refine where this displays
                else:
                    with sql.connect("siteData.db") as con:
                        cur = con.cursor()
                        pswd_hash = generate_password_hash(pswd)  # hashing password
                        cur.execute("INSERT INTO Users (Username, FirstName, LastName, DOB, Pass, UserType) VALUES (?,?,?,?,?,?)", (usrnm,frst,last,dob,pswd_hash,usrtype,))
                        con.commit()
                        msg = "Successfully created user"
            except:
                con.rollback()
            finally:
                con.close()
                return result(msg)

@app.route('/userTable')
def userInfo():
    con = sql.connect('siteData.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM Users")

    rows = cur.fetchall()
    return render_template('userTable.html', rows=rows)

@app.route('/loginPage')
def loginPage():
    return render_template('loginPage.html', template_folder='Templates')

@app.route('/loginAttempt', methods = ['POST', 'GET'])
def loginAttempt():
    if request.method == 'POST':
        try:
            usrnm = request.form['usrnm']
            pswd = request.form['pswd']

            with sql.connect("siteData.db") as con:
                cur = con.cursor()
                con.row_factory = sql.Row

                cur.execute("SELECT * FROM Users WHERE Username = ? AND Username = ?", (usrnm, usrnm)) # only works with the AND condition for some reason
                rows = cur.fetchone()
                if rows is None:
                    msg = "Could not find existing username"
                else:
                    pswd_hash = rows[4]
                    if check_password_hash(pswd_hash, pswd):
                        msg = "logged in!" #TODO: create an actual log-in session
                        return msg
                    else:
                        msg = "Incorrect password"
        except:
            con.rollback()
        finally:
            con.close()
            return msg

@app.route('/search')
def search():
    return render_template('search.html', template_folder='Templates')

@app.route('/searchResults', methods=['POST', 'GET'])
def searchResults():
    if request.method == 'POST':
        # start with empty dbRows tuple
        dbRows = ()
        try:
            query = request.form['query']
            type = request.form['search']

            with sql.connect("siteData.db") as con:
                cur = con.cursor()
                con.row_factory = sql.Row

                # add rows found by isbn from database
                if type == "isbn":
                    msg = "Searching for ISBN#" + query
                    cur.execute("SELECT * FROM Listings WHERE ISBN = ?", (query))
                    dbRows = cur.fetchall()

                # add rows found by title from database
                elif type == "title":
                    msg = "Searching for \"" + query + "\" by title"
                    cur.execute("SELECT * FROM Listings WHERE Title = ?", (query))
                    dbRows = cur.fetchall()

                # no variable defined
                else:
                    msg = "Search failed, invalid query."

        except:
            con.rollback()
        finally:
            # load chromedriver from local chromedriver installation
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            wait = WebDriverWait(driver, 15)
            # use driver to get info from book aggregator
            driver.get('https://www.bookfinder.com/')
            if (type == "isbn"):
                #submit ISBN input
                isbnInput = driver.find_element(By.NAME, 'isbn').send_keys(query)
                isbnSubmit = driver.find_element(By.ID, 'submitBtn').click()

                #find lowest price (new)
                e = wait.until(EC.visibility_of_element_located((By.ID, 'describe-isbn-title')))
                title = e.get_attribute('innerHTML')

                e = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="bd-isbn"]/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td[4]/div/span/a')))
                lowestNew = e.get_attribute('text')

                newLink = driver.find_element(By.XPATH, '//*[@id="bd-isbn"]/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td[4]/div/span/a').get_attribute('href')
                sellerInfo = str(newLink)

                #TODO remove once final testing screenshot to ensure correct found
                #driver.save_screenshot('isbnScreen.png')

                print( "Book Info: " + str(title) + str(query) + str(lowestNew) + str(sellerInfo), flush=True)
                #insert into Textbooks if not found, update if found
                cur.execute("INSERT OR IGNORE INTO Textbooks (Title, ISBN, Retail, Subj) VALUES (?, ?, ?, ?)", (title, query, lowestNew, sellerInfo,))
                cur.execute("UPDATE Textbooks SET Retail = ? WHERE ISBN = ?", (lowestNew, query,))
                cur.execute("SELECT * FROM Textbooks WHERE ISBN = ?" , (query,))
                webRows = cur.fetchall()
                con.commit()
                print (webRows, flush=True)

            elif (type == "title"):
                titleInput = driver.find_element(By.ID, 'title').send_keys(query)
                titleSubmit = driver.find_element(By.ID, 'submitBtn').click()
                time.sleep(5)  # TODO REMOVE, only for testing screenshot capability
                driver.save_screenshot('titleScreen.png')
            # create list to include results from competitor websites (amazon to start test)
            cur.close()
            con.close()
            return render_template('searchResults.html', template_folder='Templates', msg=msg, query=query, type=type,rows=dbRows, webRows=webRows)

@app.route('/createListing')
def createListing():
    return render_template('createListing.html', template_folder='Templates')

@app.route('/addListing', methods=['POST', 'GET'])
def addListing():
    if request.method == 'POST':
        con = sql.connect("siteData.db")
        msg = "Not at try"
        try:
            title = request.form['title']
            isbn = request.form['isbn']
            askprc = request.form['askprc']
            msg = "Finished try"

            cur = con.cursor()
            cur.execute("INSERT INTO Listings (Title, ISBN, Asking, HighestBid) VALUES (?,?,?,?)",(title, isbn, askprc, 0,))
            con.commit()
            msg = "Successfully created listing"
        except:
            con.rollback()
        finally:
            con.close()
            return result(msg)

@app.route('/result')
def result(msg):
    return render_template('result.html', template_folder='Templates', msg=msg)

@app.route('/createTextbook')
def createTextbook():
    return render_template('createTextbook.html', template_folder='Templates')

@app.route('/listings')
def listings():
    con = sql.connect("siteData.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM Listings")

    rows = cur.fetchall()
    return render_template("listings.html", rows=rows)

@app.route('/checkout', methods=['POST'])
def checkout():
    title = request.form['title']
    isbn = request.form['isbn']
    asking = int(float(request.form['asking'].replace('$', ''))) * 100

    session = stripe.checkout.Session.create(
        line_items=[{
            'name': title,
            'amount': asking,
            'quantity': 1,
            'currency': 'usd',
            'description': 'ISBN: ' + isbn
        }],
        payment_method_types=['card'],
        mode='payment',
        success_url=url_for('success', _external=True),  # + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('listings', _external=True)
    )
    return redirect(session.url, code=303)

@app.route('/success')
def success():
    return render_template("success.html")

if __name__ == '__main__':  # main
    app.run(debug=True)
