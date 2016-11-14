from flask import Flask, render_template, flash, request, redirect, url_for, session
from twilio import twiml
import database
database.create_table()

import util

suspiciousTransactions = util.weirdTransaction("Don")

import msg
        
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

@app.route("/home")
def home():
    accounts = util.account("Don")
    transactions = util.transactionHistory("Don")
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
    
@app.route("/home2")
def home2():
    msg.send_message("Thank you for signing up for Easy Bank. Weekly push notifications have been enabled. We hope you enjoy taking back your finances.")
    for s in suspiciousTransactions:
        if "Amazon Services-kindle" in s["description"]:
            msg.send_message("We have found several suspicious transactions this week. Did you spend $"+ s["withdrawal"] + " on "+ s["description"] +"? Respond Y if you did. Respond N for more information.")
    accounts = util.account("Don")
    transactions = util.transactionHistory("Don")
    for t in transactions:
        t['withdrawal'] = float(t['withdrawal'])
        t['deposit'] = float(t['deposit'])
    return render_template("home2.html", accounts=accounts, transactions=transactions, suspicious=suspiciousTransactions)

    
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
