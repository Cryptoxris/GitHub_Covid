from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from flask_login import LoginManager, login_manager
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Employee
from flask_mail import Mail, Message
import psycopg2
import psycopg2.extras

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    employee = Employee.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not employee or not check_password_hash(employee.password, password):
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(employee, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route("/signup")
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')
    site = request.form.get('site')
    is_admin = True if request.form.get('is_admin') == "True" else False
    is_visitor = True if request.form.get('is_visitor') == "True" else False

    employee = Employee.query.filter_by(
        email=email).first()

    if employee:
        flash('Email address already exists')
        return redirect(url_for("auth.login"))

    new_employee = Employee(email=email, firstname=firstname, lastname=lastname,
                            password=generate_password_hash(password, method='sha256'), site=site, is_admin=is_admin, is_visitor=is_visitor)

    db.session.add(new_employee)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route("/admins")
def create_admin():
    return render_template('admin.html')


@auth.route('/admins', methods=['POST'])
def create_admin_post():
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')
    site = request.form.get('site')
    is_admin = True if request.form.get('is_admin') == "True" else False
    is_visitor = True if request.form.get('is_visitor') == "True" else False

    new_admin = Employee.query.filter_by(
        email=email).first()

    if new_admin:
        flash('Email address already exists')
        return redirect(url_for("auth.login"))

    new_admin = Employee(email=email, firstname=firstname, lastname=lastname,
                         password=generate_password_hash(password, method='sha256'), site=site, is_admin=is_admin, is_visitor=is_visitor)

    db.session.add(new_admin)
    db.session.commit()
    return redirect(url_for('auth.login'))


@login_required
@auth.route('/results')
def results():
    User_id = current_user.id
    DB_HOST = "postgresql_database"
    DB_NAME = "covid"
    DB_USER = "admin"
    DB_PASS = "admin1234"

    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM public.questionnairesummary ORDER BY datetime DESC LIMIT 50')
    results = (cur.fetchall())
    cur.close()
    connection.close()

    headings = ["DateTime", "Site", "First Name", "Last Name", "Email", "InContact", "Temperature", "Fever",
                "Dry Cough", "Sore Throat", "Fever & Dry Cough", "Fever & Sore Throat", "Dry cough & Sore Throat",
                "Difficulty breathing"]
    data = (results)

    def is_accessible(self):
        if current_user.is_admin:
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    return render_template('results.html', headings=headings, data=data)


# mail = Mail()
# msg = Message('Covid-19 Self Assessment', sender='',
# recipients=[current_user.email])
# msg.html = "Hi, Thank you for submitting your covid-19 self assessment"
# mail.send(msg)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
