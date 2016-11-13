from flask import Flask, render_template, flash, request, redirect, url_for, session

import database
database.create_table()

import util

suspiciousTransactions = util.weirdTransaction("Don")

import msg

if not suspiciousTransactions == None:
    msg.send_message("You have suspicious transactions. Please click the following link to review them.")
else:
    msg.send_message("You have no suspicious transactions. Your next update will be in a week from now.")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tk'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/testing")
def testing():
    return render_template('testing.html')
    
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password']
        if database.user_authentication(email,password):
            session['email']= request.form['email']
            return redirect(url_for('home'))
        return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method =='POST':
        first_name= request.form['first_name']
        last_name= request.form['last_name']
        session['email']= request.form['email']
        email= request.form['email']
        phoneNumber= request.form['phoneNumber']
        password= request.form['password']
        database.create_user(first_name, last_name, email, phoneNumber, password, '0');
        return render_template("survey.html")
    else:
        return render_template("signup.html")
    
@app.route("/survey", methods= ['GET','POST'])
def survey():
    if request.method == 'POST':
        profileType= request.form['profileType']
        database.user_update(session['email'],profileType)
        return render_template('home.html')
    else: 
        return render_template("survey.html")
    print tr
@app.route("/home")
def home():
    accounts = util.account("Don")
    transactions = util.transactionHistory("Don")
    print suspiciousTransactions  
    for t in transactions:
        t['withdrawal'] = float(t['withdrawal'])
        t['deposit'] = float(t['deposit'])
    return render_template("home.html", accounts=accounts, transactions=transactions, suspicious=suspiciousTransactions)
    
@app.route("/about")
def about():
    return render_template("about.html")
    
@app.route("/settings")
def settings():
    return render_template("settings.html")
    
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
