from flask import Flask, render_template, request, url_for, redirect, flash
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
import mysql.connector
import sys
import time
import stripe
app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = environ.get("STRIPE_PUBLIC_KEY")
app.config['STRIPE_PRIVATE_KEY'] = environ.get("STRIPE_PRIVATE_KEY")
stripe.api_key = app.config['STRIPE_PRIVATE_KEY']

@app.route('/')
def loginRequired():
    return render_template('loginRequired.html', template_folder='Templates')

@app.route('/home')
def home():
    return render_template('index.html', template_folder='Templates')

@app.route('/signup')
def signup():
    return render_template('signup.html', template_folder='Templates')

def userExists(usrnm):
    sitedb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pythongroup"
    )
    cur = sitedb.cursor(dictionary=True)
    cur.execute("SELECT * FROM Users WHERE Username = %s AND Username = %s",(usrnm, usrnm))
    rows = cur.fetchone()

    if rows is None:
        return False
    else:
        return True

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
                    msg = "Passwords do not match"
                elif userExists(usrnm):
                    msg = "Username already exists"
                else:
                    with mysql.connector.connect(host="localhost",user="root",password="root",database="pythongroup") as sitedb:
                        cur = sitedb.cursor()
                        pswd_hash = generate_password_hash(pswd)  # hashing password
                        
                        cur.execute("INSERT INTO Users (Username, FirstName, LastName, DOB, Pass) VALUES (%s,%s,%s,%s,%s)", (usrnm,frst,last,dob,pswd_hash,))
                        sitedb.commit()
                        msg = "Successfully created user"
            except:
                sitedb.rollback()
            finally:
                return result(msg)
                con.close()

@app.route('/userTable')
def userInfo():
    sitedb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pythongroup"
    )
    cur = sitedb.cursor(dictionary=True)
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

            with mysql.connector.connect(host="localhost",user="root",password="root",database="pythongroup") as sitedb:
                cur = sitedb.cursor(dictionary=True)

                cur.execute("SELECT * FROM Users WHERE Username = %s AND Username = %s", (usrnm, usrnm))
                rows = cur.fetchone()
        except:
            sitedb.rollback()
        finally:
            if rows is None:
                msg = "Could not find existing username"
                return msg
            else:
                pswd_hash = rows['Pass']
                if check_password_hash(pswd_hash, pswd):
                    msg = "logged in!"  # TODO: create an actual log-in session
                    return render_template('index.html', template_folder='Templates')
                else:
                    msg = "Incorrect password"
                    return msg
            con.close()
            return render_template('index.html')

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

            with mysql.connector.connect(host="localhost",user="root",password="root",database="pythongroup") as sitedb:
                cur = sitedb.cursor(dictionary=True)
                # add rows found by isbn from database
                if type == "isbn":
                    msg = "Searching for ISBN# " + query
                    print(("LOOKING FOR QUERY" + str(query)), flush=True)
                    cur.execute("SELECT * FROM Listings WHERE ISBN = %s" , (query,))
                    dbRows = cur.fetchall()
                    print((dbRows), flush=True)

                # add rows found by title from database
                elif type == "title":
                    msg = "Searching for \"" + query + "\" by title"
                    print("LOOKING FOR ROWS", flush=True)
                    cur.execute("SELECT * FROM Listings WHERE Title = %s" , (query,))
                    dbRows = cur.fetchall()
                    print(dbRows, flush=True)

                # no variable defined
                else:
                    msg = "Search failed, invalid query."

        except:
            sitedb.rollback()
        finally:
            sitedb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="pythongroup"
            )
            cur = sitedb.cursor(dictionary=True)

            # load chromedriver from local chromedriver installation
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            wait = WebDriverWait(driver, 20)
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

                #insert into Textbooks if not found, update if found
                cur.execute("INSERT IGNORE INTO Textbooks (Title, ISBN, Retail, Subj) VALUES (%s, %s, %s, %s)", (title, query, lowestNew, sellerInfo,))
                cur.execute("UPDATE Textbooks SET Retail = %s WHERE ISBN = %s", (lowestNew, query,))
                cur.execute("SELECT * FROM Textbooks WHERE ISBN = %s" , (query,))
                webRows = cur.fetchall()
                sitedb.commit()
                print (webRows, flush=True)

            elif (type == "title"):
                titleInput = driver.find_element(By.ID, 'title').send_keys(query)
                titleSubmit = driver.find_element(By.ID, 'submitBtn').click()
                
                e = wait.until(EC.visibility_of_any_elements_located((By.XPATH, "//*[contains(text(), 'Click to pick a title')]")))
                clickTitle = driver.find_element(By.XPATH, '//*[@id="bd"]/ul/li/span/a').click()

                #find ISBN
                e = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="bd"]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/a')))
                isbn = e.get_attribute('innerHTML')

                e = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="bd"]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[4]/div/span/a')))
                lowestNew = e.get_attribute('text')

                newLink = driver.find_element(By.XPATH, '//*[@id="bd"]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[4]/div/span/a').get_attribute('href')
                sellerInfo = str(newLink)

                #insert into Textbooks if not found, update if found
                cur.execute("INSERT IGNORE INTO Textbooks (Title, ISBN, Retail, Subj) VALUES (%s, %s, %s, %s)", (query, isbn, lowestNew.strip('$'), sellerInfo,))
                cur.execute("UPDATE Textbooks SET Retail = %s WHERE ISBN = %s", (lowestNew.strip('$'), isbn,))
                cur.execute("SELECT * FROM Textbooks WHERE ISBN = %s" , (isbn,))
                webRows = cur.fetchall()
                sitedb.commit()
                print(webRows, flush=True)

                # TODO remove once final driver.save_screenshot('titleScreen.png')
            # create list to include results from competitor websites (amazon to start test)
            cur.close()
            sitedb.close()
            return render_template('searchResults.html', template_folder='Templates', msg=msg, query=query, type=type,rows=dbRows, webRows=webRows)

@app.route('/createListing')
def createListing():
    return render_template('createListing.html', template_folder='Templates')

@app.route('/addListing', methods=['POST', 'GET'])
def addListing():
    if request.method == 'POST':
        sitedb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="pythongroup"
        )
        msg = "Not at try"
        try:
            title = request.form['title']
            isbn = request.form['isbn']
            askprc = request.form['askprc']
            msg = "Finished try"

            cur = sitedb.cursor()
            cur.execute("INSERT INTO Listings (Title, ISBN, Asking, HighestBid) VALUES (%s,%s,%s,%s)",(title, isbn, askprc, 0,))
            sitedb.commit()
            msg = "Successfully created listing"
        except:
            sitedb.rollback()
        finally:
            sitedb.close()
            return result(msg)

@app.route('/result')
def result(msg):
    return render_template('result.html', template_folder='Templates', msg=msg)

@app.route('/createTextbook')
def createTextbook():
    return render_template('createTextbook.html', template_folder='Templates')

@app.route('/listings')
def listings():
    sitedb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pythongroup"
    )
    cur = sitedb.cursor(dictionary=True)
    cur.execute("SELECT * FROM Listings")

    rows = cur.fetchall()
    return render_template("listings.html", rows=rows)

@app.route('/checkout', methods=['POST'])
def checkout():
    title = request.form['title']
    isbn = request.form['isbn']
    asking = float(request.form['asking'].replace('$', ''))

    session = stripe.checkout.Session.create(
        line_items=[{
            'name': title,
            'amount': int(asking) * 100,
            'quantity': 1,
            'currency': 'usd',
            'description': 'ISBN: ' + isbn
        }],
        shipping_address_collection={
            'allowed_countries': ['US', 'CA'],
        },
        shipping_options=[
        {
            'shipping_rate_data': {
                'type': 'fixed_amount',
                'fixed_amount': {
                    'amount': 0,
                    'currency': 'usd',
                },
                'display_name': 'Free shipping',
                'delivery_estimate': {
                    'minimum': {
                        'unit': 'business_day',
                        'value': 5,
                    },
                    'maximum': {
                        'unit': 'business_day',
                        'value': 7,
                    },
                }
            }
        }],
        payment_method_types=['card'],
        mode='payment',
        success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('listings', _external=True)
    )
    return redirect(session.url, code=303)

@app.route('/success')
def success():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    customer = stripe.Customer.retrieve(session.customer)
    #line_items = stripe.checkout.Session.list_line_items(request.args.get('session_id'), limit=5)

    name = customer.name
    shipping = customer.shipping
    email = customer.email
    return render_template("success.html", name=name, shipping=shipping, email=email)

if __name__ == '__main__':  # main
    app.run(debug=True)
