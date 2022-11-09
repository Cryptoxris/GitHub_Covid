from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(UserMixin, db.Model):
    __tablename__ = 'Employee'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(1000))
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    site = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    is_visitor = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, firstname, lastname, site, is_admin, is_visitor):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.site = site
        self.is_admin = is_admin
        self.is_visitor = is_visitor


class Recommendations(UserMixin, db.Model):
    __tablename__ = 'Recommendations'
    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(10), unique=True, nullable=False)
    feedback = db.Column(db.String(100), nullable=False)

    def __init__(self, flag, feedback):
        self.flag = flag
        self.feedback = feedback


class Questionnaire(UserMixin, db.Model):
    __tablename__ = 'Questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    incontact = db.Column(db.String(5))
    temperature = db.Column(db.Float(4))
    fever = db.Column(db.String(5))
    drycough = db.Column(db.String(5))
    sorethroat = db.Column(db.String(5))
    feverdrycough = db.Column(db.String(5))
    feversorethroat = db.Column(db.String(5))
    drycoughsorethroat = db.Column(db.String(5))
    difficultyinbreathing = db.Column(db.String(5))
    employee_id = db.Column(db.Integer, db.ForeignKey('Employee.id'), nullable=False)

    def __init__(self, datetime, incontact, temperature, fever, drycough, sorethroat, feverdrycough, feversorethroat,
                 drycoughsorethroat, difficultyinbreathing, employee_id):
        self.datetime = datetime
        self.incontact = incontact
        self.temperature = temperature
        self.fever = fever
        self.drycough = drycough
        self.sorethroat = sorethroat
        self.feverdrycough = feverdrycough
        self.feversorethroat = feversorethroat
        self.feversorethroat = drycoughsorethroat
        self.drycoughsorethroat = drycoughsorethroat
        self.difficultyinbreathing = difficultyinbreathing
        self.employee_id = employee_id
