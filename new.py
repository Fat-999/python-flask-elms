from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'empl1'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/admin')
def admin():
    # Check if user is loggedin
    if 'loggedinad' in session:
        # User is loggedin show them the home page
        return render_template('dashboard.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/employee')
def employee():
    return render_template("employee.html")


@app.route('/department')
def department():
    return render_template("department.html")


@app.route('/manageemp')
def manageemp():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT  * FROM employee")
    data = cursor.fetchall()
    cursor.close()
    return render_template("manageemployee.html", employee=data)

@app.route('/empdash')
def empdash():
    # Check if user is loggedin
    if 'loggedinemp' in session:
        # User is loggedin show them the home page
        return render_template('empdashboard.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login_emp'))

@app.route('/applylev')
def applylev():
    return render_template("applylev.html")


@app.route('/chgpass')
def chgpass():
    return render_template("chgemp_pass.html")


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login_emp', methods=['GET', 'POST'])
def login_emp():
    # Output message if something goes wrong...

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'empid' in request.form and 'password' in request.form:
        # Create variables for easy access
        empid = request.form['empid']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE empid = %s AND password = %s', (empid, password,))
        # Fetch one record and return result
        accounts = cursor.fetchone()
        # If account exists in accounts table in out database
        if employee:
            # Create session data, we can access this data in other routes
            session['loggedinemp'] = True
            session['id'] = accounts['id']
            session['empname'] = accounts['empname']
            # Redirect to home page
            return render_template('empdashboard.html', msg='')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect password, try again.', category='error')

    return render_template('login_emp.html', msg='')


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        admin = cursor.fetchone()
        # If account exists in accounts table in out database
        if admin:
            # Create session data, we can access this data in other routes
            session['loggedinad'] = True
            session['id'] = admin['id']
            session['username'] = admin['username']
            # Redirect to home page
            return render_template('dashboard.html', msg='')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect password, try again.', category='error')

    return render_template('login.html', msg='')


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logoutad')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedinad', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login_emp'))


@app.route('/logoutemp')
def logoutemp():
    # Remove session data, this will log the user out
   session.pop('loggedinad', None)
   session.pop('id', None)
   session.pop('empname', None)
   # Redirect to login page
   return redirect(url_for('login_emp'))


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM info_table WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO info_table VALUES (NULL, %s, %s, %s, %s)', (username, password, password2, email,))
            mysql.connection.commit()
            flash('You have successfully registered! Please login')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('signup.html', msg=msg)


 # http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM info_table WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/empl1/addemp - this will be the registration page, we need to use both GET and POST requests
@app.route('/addemp', methods=['GET', 'POST'])
def addemp():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'empname' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        empname = request.form['empname']
        empid = request.form['empid']
        email = request.form['email']
        contact = request.form['contact']
        dep = request.form['dep']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        password = request.form['password']
        password2 = request.form['password2']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE empname = %s', (empname,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', empname):
            flash('Username must contain only characters and numbers!')
        elif not re.match(r'[0-9]+', empid):
            flash('empid must contain only numbers!')
        elif not empname or not password or not email or not empid:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO employee VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (empname, empid, contact, email,  password, password2, dep, gender, birthdate))
            mysql.connection.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('addemployee.html', msg=msg)


# http://localhost:5000/empl1/adddep - this will be the registration page, we need to use both GET and POST requests
@app.route('/adddep', methods=['GET', 'POST'])
def adddep():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'depcode' in request.form and 'depname' in request.form and 'depstname' in request.form:
        # Create variables for easy access
        depcode = request.form['depcode']
        depname = request.form['depname']
        depstname = request.form['depstname']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM department WHERE depcode = %s', (depcode,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not depname or not depcode or not depstname:
            flash('Please fill out the form!')
        elif not re.match(r'[0-9]+', depcode):
            flash('depcode must contain only numbers!')
            # Show registration form with message (if any)
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO department VALUES ( NULL, %s, %s, %s)', (depcode, depname, depstname))
            mysql.connection.commit()
            flash('You have successfully registered!')

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('adddepartment.html', msg=msg)


@app.route('/update', methods=['POST', 'GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        empname = request.form['empname']
        empid = request.form['empid']
        contact = request.form['contact']
        email = request.form['email']
        dep = request.form['dep']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        cursor = mysql.connection.cursor()
        cursor.execute("update users set empname=%s,empid=%s,contact=%s,email=%s,dep=%s,gender=%s birthdate=%s,where id=%s", [empname, empid, contact, email, dep, gender, birthdate, id_data])
        flash("Data Updated Successfully")
        mysql.connection.commit()
    return redirect(url_for('manageemp'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM employee WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('manageemp'))

app.run(debug=True)
