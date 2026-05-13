from flask import Flask, render_template, request, redirect, url_for, g, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DATABASE = './test1.db'
app.config['SECRET_KEY'] = "yfgh8756"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.commit()
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route("/signin", methods=["GET", "POST"])
def sign_in():
    cur = get_db().cursor()
    if request.method == "POST":
        #Get data from form and query database
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        cur.execute("SELECT username, hash FROM users WHERE username = ?", (username,))
        result = cur.fetchone()
        close_connection()
        print(result)
        if result:
            USERNAME, PASSWORD = result
        else:
            return render_template("sign_in.html",
                                      error="No account with that username")

        #Check credentials
        if check_password_hash(PASSWORD, password):
            session['username'] = USERNAME
            return redirect(url_for("welcome"))
        else:
            return render_template("sign_in.html",
                                   error="Invalid username or password")
    return render_template("sign_in.html")

@app.route("/welcome")
def welcome():
    session['logged_in'] = True
    return render_template('index.html')

@app.route('/logout')
def logout():
    # Remove data from the session
    session.pop('username', None)
    session.pop('logged_in', None)
    return render_template('index.html')

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    cur = get_db().cursor()

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        con_password = request.form.get("con-password")
        if password == con_password:
            cur.execute("SELECT username FROM users WHERE username = ?", (username,))
            u_result=cur.fetchone()
            cur.execute("SELECT email FROM users WHERE email = ?", (email,))
            e_result = cur.fetchone()

            if u_result == None and e_result == None:  
                print(username, ", ", password, ", ", con_password)
                hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
                cur.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", (username, email, hash,))
                close_connection()
                flash("Sign Up Successful", "Success")
                return redirect(url_for("sign_in"))      

            else:
                if u_result != None:
                    return render_template("sign_up.html",
                                        error="Username already in use")
                else:
                    return render_template("sign_up.html",
                                           error="Email already in use")
                    

        else:
            return render_template("sign_up.html",
                                      error="Passwords do not match")
    return render_template("sign_up.html")

if __name__ == "__main__":
    app.run(debug=True)