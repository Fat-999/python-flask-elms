from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'Rednetworks'

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

# Admin system:
@app.route('/admin')
def admin():
      if 'loggedad' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM employee")
        num = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM department")
        dep = cur.fetchone()
        cur.close()
        return render_template('admin/dashboard.html', data=num,  dep=dep, username=session['username'])
      return redirect(url_for('login'))




@app.route('/employee')
def employee():
    if 'loggedad' in session:
        return render_template('admin/employee.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/manageemp')
def manageemp():
    if 'loggedad' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM employee")
        data = cur.fetchall()
        cur.close()
        return render_template("admin/manageemployee.html", employee=data, username=session['username'])
    return redirect(url_for('login'))


@app.route('/department')
def department():
    if 'loggedad' in session:
        return render_template('admin/department.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/managedep')
def managedep():
    if 'loggedad' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM department")
        data = cur.fetchall()
        cur.close()
        return render_template("admin/managedep.html", employee=data, username=session['username'])
    return redirect(url_for('login'))


@app.route('/updep', methods=['POST', 'GET'])
def updep():
    if request.method == 'POST':
        id_data = request.form['id']
        depcode = request.form['depcode']
        depname = request.form['depname']
        depstname = request.form['depstname']

        cursor = mysql.connection.cursor()
        sql = "UPDATE department SET depcode=%s, depname=%s, depstname=%s WHERE id=%s"
        data = (depcode, depname, depstname, id_data)
        cursor.execute(sql, data)
        mysql.connection.commit()
        flash("Data Updated Successfully")

    return redirect(url_for('managedep'))


@app.route('/deldep/<string:id_data>', methods=['GET'])
def deldep(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM department WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('managedep'))

@app.route('/lev')
def lev():
    if 'loggedad' in session:
        return render_template('admin/leavetyp.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/addlev', methods=['GET', 'POST'])
def addlev():
    if 'loggedad' in session:
        if request.method == 'POST' and 'levtype' in request.form and 'description' in request.form:
            # Create variables for easy access
            levtype = request.form['levtype']
            description = request.form['description']
            # Check if account exists using MySQL
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM leaves WHERE levtype = %s', (levtype,))
            account = cur.fetchone()
            # If account exists show error and validation checks
            if account:
                flash('Account already exists!')
            elif not levtype or not description:
                flash('Please fill out the form!')
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cur.execute(
                    'insert into leaves (levtype, description) values (%s, %s)',
                    [levtype, description])
                mysql.connection.commit()
                flash('You have successfully added!')
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            flash('Please fill out the field!')
        # Show registration form with message (if any)
        return render_template('admin/addlev.html',username=session['username'])
    return redirect(url_for('login'))


@app.route('/managelev')
def managelev():
    if 'loggedad' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM leaves")
        data = cur.fetchall()
        cur.close()
        return render_template("admin/managelev.html", employee=data, username=session['username'])
    return redirect(url_for('login'))


@app.route('/updlev', methods=['POST', 'GET'])
def updlev():
    if request.method == 'POST':
        id_data = request.form['id']
        levtype = request.form['levtype']
        description = request.form['description']
        cursor = mysql.connection.cursor()
        sql = "UPDATE leaves SET levtype=%s,  description=%s WHERE id=%s"
        data = (levtype, description, id_data)
        cursor.execute(sql, data)
        mysql.connection.commit()
        flash("Data Updated Successfully")

    return redirect(url_for('managelev'))


@app.route('/deletelev/<string:id_data>', methods=['GET'])
def deletelev(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM leaves WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('managelev'))


@app.route('/chgadmpass')
def chgadmpass():
    if 'loggedad' in session:
        return render_template('admin/chgadm_pass.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/changeadm', methods=['GET', 'POST'])
def changeadm():
    if 'loggedad' in session:
        if request.method == 'POST':
           oldpass = request.form['opass']
           newpass = request.form['npass']
           confpass = request.form['cpass']
           id = session['id']
           if newpass != confpass:
               flash("password do not match", 'danger')
               return redirect(url_for('chgadmpass'))
           cur = mysql.connection.cursor()
           sql = "UPDATE admin SET password=%s WHERE id=%s"
           data2 = (newpass, id)
           cur.execute(sql, data2)
           mysql.connection.commit()
           cur.close()
           flash("password changed Successfully", 'success')
           return redirect(url_for('chgadmpass'))

    return redirect(url_for('login'))



# http://localhost:5000/login/ - this will be the admin login page, we need to use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
            # Fetch one record and return result
            admin = cur.fetchone()
            # If account exists in accounts table in out database
            if admin:
                # Create session data, we can access this data in other routes
                session['loggedad'] = True
                session['username'] = admin['username']
                session['password'] = admin['password']
                session['id'] = admin['id']
                # Redirect to home page
                return redirect(url_for('admin'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect password, try again.', category='error')
                return render_template('login.html')

        except Exception as e:
            print(e)
        finally:
          mysql.connection.commit()
          cur.close()
    return render_template('login.html')


# http://localhost:5000/empl1/addemp - this will be the add employee page, we need to use both GET and POST requests
@app.route('/addemp', methods=['GET', 'POST'])
def addemp():
    if 'loggedad' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT depname FROM department")
        data = cur.fetchall()
        cur.close()
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
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM employee WHERE empname = %s', (empname,))
            account = cur.fetchone()
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
                cur.execute('insert into employee (empname,empid,contact,email,password,password2,dep,gender,birthdate) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                            [empname, empid, contact, email,  password, password2, dep, gender, birthdate])
                mysql.connection.commit()
                flash('You have successfully registered!')
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            flash('Please fill out the form!')
        # Show registration form with message (if any)
        return render_template('admin/addemployee.html', department=data, username=session['username'])
    return redirect(url_for('login'))


# http://localhost:5000/empl1/adddep - this will be the add department page, we need to use both GET and POST requests
@app.route('/adddep', methods=['GET', 'POST'])
def adddep():
    if 'loggedad' in session:
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'depcode' in request.form and 'depname' in request.form and 'depstname' in request.form:
            # Create variables for easy access
            depcode = request.form['depcode']
            depname = request.form['depname']
            depstname = request.form['depstname']
            # Check if account exists using MySQL
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM department WHERE depcode = %s', (depcode,))
            dep = cur.fetchone()
            # If account exists show error and validation checks
            if dep:
                flash('Account already exists!')
            elif not depname or not depcode or not depstname:
                flash('Please fill out the form!')
            elif not re.match(r'[0-9]+', depcode):
                flash('depcode must contain only numbers!')
                # Show registration form with message (if any)
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cur.execute(
                    'insert into department (depcode,depname,depstname) values (%s, %s, %s)',
                    [depcode, depname, depstname])
                mysql.connection.commit()
                flash('You have successfully registered!')

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            flash('Please fill out the form!')
        # Show registration form with message (if any)
        return render_template('admin/adddepartment.html', username=session['username'])
    return redirect(url_for('login'))


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
        sql = "UPDATE employee SET empname=%s, empid=%s, contact=%s, email=%s, dep=%s, gender=%s, birthdate=%s WHERE id=%s"
        data = (empname, empid, contact, email, dep, gender, birthdate, id_data)
        cursor.execute(sql, data)
        mysql.connection.commit()
        flash("Data Updated Successfully")

    return redirect(url_for('manageemp'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('manageemp'))


#Employee System:

@app.route('/empdash')
def empdash():
    if 'loggedad' in session:
        return render_template('empdashboard.html', empname=session['empname'])
    return redirect(url_for('login_emp'))


@app.route('/applylev', methods=['POST', 'GET'])
def applylev():
     if 'loggedad' in session:
         cur = mysql.connection.cursor()
         cur.execute("SELECT levtype FROM leaves")
         data = cur.fetchall()
         cur.close()
         if request.method == 'POST':
             empid = session['id']
             fromdate = request.form['fdate']
             todate = request.form['tdate']
             levtype = request.form['ltype']
             description = request.form['description']
             mgstatus=0
             status=0
             isread=0
             isreadmg=0

             cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             cur.execute('insert into applyleaves (fromdate,todate,levtype,description,status,mgstatus,isread,isreadmg,empid) values (%s, %s, %s, %s, %s, %s,%s, %s,%s)',[fromdate, todate, levtype, description, status, mgstatus, isread, isreadmg, empid])
             mysql.connection.commit()
             flash('You have successfully registered!')

             cur = mysql.connection.cursor()
             cur.execute("SELECT levtype FROM leaves")
             data = cur.fetchall()
             cur.close()
         return render_template("applylev.html", leave=data, empname=session['empname'])
     return redirect(url_for('login_emp'))


@app.route('/chgpass')
def chgpass():
    if 'loggedad' in session:
        return render_template("chgemp_pass.html", empname=session['empname'])
    return redirect(url_for('login_emp'))



@app.route('/changeemp', methods=['GET', 'POST'])
def changeemp():
    if 'loggedad' in session:
        if request.method == 'POST':
           oldpass = request.form['opass']
           newpass = request.form['npass']
           confpass = request.form['cpass']
           id = session['id']
           if newpass != confpass:
               flash("password do not match", 'danger')
               return redirect(url_for('chgpass'))
           cur = mysql.connection.cursor()
           sql = "UPDATE employee SET password=%s, password2=%s WHERE id=%s"
           data2 = (newpass, confpass, id)
           cur.execute(sql, data2)
           mysql.connection.commit()
           cur.close()
           flash("password changed Successfully", 'success')
           return redirect(url_for('chgpass'))

    return redirect(url_for('login'))


@app.route('/levhistory')
def levhistory():
    if 'loggedad' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fromdate,id,empid,todate,levtype,description,postingdate,mgremark,mgremarkdate,mgstatus FROM applyleaves WHERE empid=%s", (session['id'],))
        val = cur.fetchall()
        cur.close()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT count(levtype) AS X FROM applyleaves where levtype = 'Sick Leave' and empid=%s;", (session['id'],))
        lev1 = cur.fetchone()
        #x=lev1["count(levtype)"]
        #y=6-x
        #print(lev1)
        cur.execute("SELECT count(levtype)  FROM applyleaves where levtype = 'Casual leave' and empid=%s;", (session['id'],))
        lev2 = cur.fetchone()
        #print(lev2)
        cur.execute("SELECT count(levtype)  FROM applyleaves where levtype = 'Other Leave' and empid=%s;",(session['id'],))
        lev3 = cur.fetchone()
        #print(lev3)
        cur.close()
        return render_template("levhistory.html", details=val, d1=lev1, d2=lev2, d3=lev3, empname=session['empname'], id=session['id'])
    return redirect(url_for('login_emp'))


# Employee login page :
@app.route('/login_emp', methods=['GET', 'POST'])
def login_emp():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'empid' in request.form and 'password' in request.form:
        # Create variables for easy access
        empid = request.form['empid']
        password = request.form['password']
        # Check if account exists using MySQL
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM employee WHERE empid = %s AND password = %s', (empid, password,))
            # Fetch one record and return result
            emp = cur.fetchone()
            # If account exists in accounts table in out database
            if emp:
                # Create session data, we can access this data in other routes
                session['loggedad'] = True
                session['empid'] = emp['empid']
                session['empname'] = emp['empname']
                session['email'] = emp['email']
                session['contact'] = emp['contact']
                session['dep'] = emp['dep']
                session['gender'] = emp['gender']
                session['birthdate'] = emp['birthdate']
                session['id'] = emp['id']
                # Redirect to home page
                return redirect(url_for('empdash'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect password, try again.', category='error')
                return render_template('login_emp.html')

        except Exception as e:
            print(e)
        finally:
          mysql.connection.commit()
          cur.close()
    return render_template('login_emp.html')

@app.route('/tllogin', methods=['GET', 'POST'])
def tllogin():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        tlusername = request.form['username']
        tlpassword = request.form['password']
        # Check if account exists using MySQL
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM teamleader WHERE tlusername = %s AND tlpassword = %s', (tlusername, tlpassword,))
            # Fetch one record and return result
            team = cur.fetchone()
            # If account exists in accounts table in out database
            if team:
                # Create session data, we can access this data in other routes
                session['loggedad'] = True
                session['tlusername'] = team['tlusername']
                session['tlpassword'] = team['tlpassword']
                session['id'] = team['id']
                # Redirect to home page
                return redirect(url_for('tldashboard'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect password, try again.', category='error')
                return render_template('login_tl.html')

        except Exception as e:
            print(e)
        finally:
            mysql.connection.commit()
            cur.close()

    return render_template('login_tl.html')


@app.route('/tldashboard')
def tldashboard():
    if 'loggedad' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM employee")
        num = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM department")
        dep = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select applyleaves.id as lid, employee.empname, employee.empId, employee.dep, employee.id, applyleaves.levtype, applyleaves.postingdate, applyleaves.status from applyleaves join employee on applyleaves.empid=employee.id  order by lid desc limit 10")
        val = cur.fetchall()
        count = 1
        cur.execute("SELECT count(isread)  FROM applyleaves where isread = '0';")
        a = cur.fetchone()
        #print(a)
        cur.close()
        return render_template('TL/tldashboard.html', data=num, count=count, icon=a, dep=dep, val=val, username=session['tlusername'])
    return redirect(url_for('tllogin'))


@app.route('/levdetails/<string:id>')
def levdetails(id):
    if 'loggedad' in session:
        isRead = 1
        cursor = mysql.connection.cursor()
        sql = "UPDATE applyleaves SET isread=%s WHERE id=%s"
        data = (isRead, id)
        cursor.execute(sql, data)
        mysql.connection.commit()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select applyleaves.id as lid, employee.empname, employee.empid, employee.id, employee.gender, employee.contact, employee.email, applyleaves.levtype, applyleaves.todate, applyleaves.fromdate, applyleaves.description, applyleaves.postingdate, applyleaves.status, applyleaves.tlremark, applyleaves.tlremarkdate from applyleaves join employee on applyleaves.empid=employee.id where applyleaves.id=%s", (id,))
        val = cur.fetchall()
        cur.execute("SELECT count(isread)  FROM applyleaves where isread = '0';")
        a = cur.fetchone()
        #print(a)
        cur.close()
        return render_template('TL/leave_details.html', data=val, icon=a, username=session['tlusername'])
    return redirect(url_for('tllogin'))


@app.route('/takeaction/<string:lid>', methods=['POST', 'GET'])
def takeaction(lid):
    if 'loggedad' in session:
        if request.method == 'POST':
            status = request.form['status']
            description = request.form['description']
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor = mysql.connection.cursor()
            sql = "UPDATE applyleaves SET status=%s, tlremarkdate=%s, tlremark=%s WHERE id=%s"
            data = (status, formatted_date, description, lid)
            cursor.execute(sql, data)
            mysql.connection.commit()
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT count(isread)  FROM applyleaves where isread = '0';")
            a = cur.fetchone()
            # print(a)
            cur.close()
            flash("Data Updated Successfully")
            return render_template('TL/tldashboard.html', icon=a, username=session['tlusername'])
    return redirect(url_for('tllogin'))



# http://localhost:5000/python/logout - this will be the logout page
@app.route('/mglogin', methods=['GET', 'POST'])
def mglogin():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        mgusername = request.form['username']
        mgpassword = request.form['password']
        # Check if account exists using MySQL
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM manager WHERE mgusername = %s AND mgpassword = %s', (mgusername, mgpassword,))
            # Fetch one record and return result
            mg = cur.fetchone()
            # If account exists in accounts table in out database
            if mg:
                # Create session data, we can access this data in other routes
                session['loggedad'] = True
                session['mgusername'] = mg['mgusername']
                session['mgpassword'] = mg['mgpassword']
                session['id'] = mg['id']
                # Redirect to home page
                return redirect(url_for('mgdashboard'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect password, try again.', category='error')
                return render_template('login_mg.html')

        except Exception as e:
            print(e)
        finally:
            mysql.connection.commit()
            cur.close()
    return render_template('login_mg.html')


@app.route('/mgdashboard')
def mgdashboard():
    if 'loggedad' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM employee")
        num = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM department")
        dep = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select applyleaves.id as lid, employee.empname, employee.empId, employee.dep, employee.id, applyleaves.levtype, applyleaves.postingdate, applyleaves.status,applyleaves.mgstatus from applyleaves join employee on applyleaves.empid=employee.id order by lid desc limit 10")
        val = cur.fetchall()
        count = 1
        cur.execute("SELECT count(isreadmg)  FROM applyleaves where isreadmg = '0';")
        b = cur.fetchone()
        #print(b)
        cur.close()
        return render_template("manager/mgdashboard.html", data=num, icon=b, count=count, dep=dep, val=val,
                               username=session['mgusername'])
    return redirect(url_for('mglogin'))


@app.route('/levdetailsmg/<string:id>')
def levdetailsmg(id):
    if 'loggedad' in session:
        isReadmg = 1
        cursor = mysql.connection.cursor()
        sql = "UPDATE applyleaves SET isreadmg=%s WHERE id=%s"
        data = (isReadmg, id)
        cursor.execute(sql, data)
        mysql.connection.commit()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select applyleaves.id as lid, employee.empname, employee.empid, employee.id, employee.gender, employee.contact, employee.email, applyleaves.levtype, applyleaves.todate, applyleaves.fromdate, applyleaves.description, applyleaves.postingdate, applyleaves.status, applyleaves.tlremark, applyleaves.tlremarkdate, applyleaves.mgstatus, applyleaves.mgremark, applyleaves.mgremarkdate from applyleaves join employee on applyleaves.empid=employee.id where applyleaves.id=%s", (id,))
        val = cur.fetchall()
        cur.execute("SELECT count(isreadmg)  FROM applyleaves where isreadmg = '0';")
        b = cur.fetchone()
        cur.close()
        return render_template('Manager/leave_details.html', data=val, icon=b, username=session['mgusername'])
    return redirect(url_for('login'))


@app.route('/mgtakeaction/<string:lid>', methods=['POST', 'GET'])
def mgtakeaction(lid):
    if 'loggedad' in session:
        if request.method == 'POST':
            status = request.form['status']
            description = request.form['description']
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor = mysql.connection.cursor()
            sql = "UPDATE applyleaves SET mgstatus=%s, mgremarkdate=%s, mgremark=%s WHERE id=%s"
            data = (status, formatted_date, description, lid)
            cursor.execute(sql, data)
            mysql.connection.commit()
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT count(isreadmg)  FROM applyleaves where isreadmg = '0';")
            b = cur.fetchone()
            cur.close()
            flash("Data Updated Successfully")
            return render_template('manager/mgdashboard.html', icon=b, username=session['mgusername'])
    return redirect(url_for('mglogin'))


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
   session.pop('loggedad', None)
   session.clear()
   return redirect(url_for('index'))


app.run(debug=True)

"""
SELECT COUNT(levtype) FROM applyleaves WHERE levtype="Sick Leave" AND empid=4
"""
