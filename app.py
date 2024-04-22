from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'test'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s AND password=%s', (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            #session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully'
            return render_template('index.html', message=message)
        else:
            message = 'Please enter correct email/password'
    return render_template('login.html', message=message)



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account Already Exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid Email'
        elif not username or not password or not email:
            message = 'Please Fill all Details'
        else:
            cursor.execute('INSERT INTO user VALUES(%s,%s,%s)', (username, email, password, ))
            mysql.connection.commit()      
            message = 'Register Successfully!!'
    elif request.method == 'POST':
        message = 'Please Fill all Details'
    return render_template('register.html', message=message) 
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/speech-to-sign",methods=['GET','POST'])
def speechtosign():
    if request.method == 'POST':
        tests = request.form['letter']
        lis = []
        for word in tests.split():
            alphabet_list = list(word)
            lis.append(alphabet_list)
    else:
        lis = []
    return render_template("speechtosign.html", test=lis)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='4999', debug=True)
