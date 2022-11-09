from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_login import current_user
from flask import Blueprint, render_template, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_manager
from models import db, Employee
from models import db, Questionnaire

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hifhkbkhabenbnihoehhednehja;ru;aejralmeell'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin1234@postgresql_database:5432/covid'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Email configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
admin = Admin(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Employee.query.get(int(user_id))


# blueprint for auth routes in our app
from auth import auth as auth_blueprint, login

app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint

app.register_blueprint(main_blueprint)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

if __name__ != "__main__":
    pass
else:
    app.run(debug=False, host='0.0.0.0')
