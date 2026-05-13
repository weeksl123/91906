from flask import Flask, render_template, request
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)

conn = sqlite3.connect("ordering.db")
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        attempted_email=request.form['email']
        attempted_password=request.form['password']
        if check_password_hash(stored_hash, attempted_password):
            print("Password correct")
    return render_template('sign_in.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        con_password=request.form['con-password']
    return render_template('sign_up.html')

if __name__ == "__main__":
    app.run(debug=True)