from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', template_folder = 'Templates')

@app.route('/signup')
def signup():
    return render_template('signup.html', template_folder = 'Templates')

@app.route('/addUser', methods = ['POST', 'GET'])
def addUser():

        if request.method == 'POST':
            try:
                usrnm   = request.form['usrnm']
                frst    = request.form['frst']
                last    = request.form['last']
                dob     = request.form['dob']
                pswd    = request.form['pswd']
                confirm = request.form['confirm']

                if pswd != confirm:
                    msg = "Password and Confirm Password must match" # refine where this displays
                else:
                    with sql.connect("siteData.db") as con:
                        cur = con.cursor()
                        cur.execute("INSERT INTO Users (Username, FirstName, LastName, DOB, Pass) VALUES (?,?,?,?,?)", (usrnm,frst,last,dob,pswd,))
                        con.commit()
                        msg = "Successfully created user"
            except:
                con.rollback()
            finally:
                con.close()
                return result(msg)

@app.route('/loginPage')
def loginPage():
    return render_template('loginPage.html', template_folder = 'Templates')

@app.route('/loginAttempt', methods = ['POST', 'GET'])
def loginAttempt():
    if request.method == 'POST':
        try:
            usrnm = request.form['usrnm']
            pswd  = request.form['pswd']

            with sql.connect("siteData.db") as con:
                cur = con.cursor()
                con.row_factory = sql.Row

                cur.execute("SELECT rowid FROM Users WHERE Username = ? AND Pass = ?", (usrnm, pswd,)) # probably reevaluate this
                rows = cur.fetchone()

                if rows is None:
                    msg = "Could not find existing user"
                else:
                    msg = "Found user"   
        except:
            con.rollback()
        finally:
            con.close()
            return result(msg)

@app.route('/createListing')
def createListing():
    return render_template('createListing.html', template_folder = 'Templates')

@app.route('/addListing', methods = ['POST', 'GET'])
def addListing():
    if request.method == 'POST':
        con = sql.connect("siteData.db")
        msg = "Not at try"
        try:
            title   = request.form['title']
            isbn    = request.form['isbn']
            askprc  = request.form['askprc']
            msg = "Finished try"
            
            cur = con.cursor()
            cur.execute("INSERT INTO Listings (Title, ISBN, Asking, HighestBid) VALUES (?,?,?,?)", (title,isbn,askprc,0,))
            con.commit()
            msg = "Successfully created listing"
        except:
            con.rollback()
        finally:
            con.close()
            return result(msg)


@app.route('/result')
def result(msg):
    return render_template('result.html', template_folder = 'Templates', msg = msg)

@app.route('/createTextbook')
def createTextbook():
    return render_template('createTextbook.html', template_folder = 'Templates')

if __name__ == '__main__':      # main
   app.run(debug = True)