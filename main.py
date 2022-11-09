from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user

from flask import Blueprint, render_template, send_from_directory
from models import db, Questionnaire, Recommendations
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    flash(current_user.firstname)

    return render_template('profile.html', firstname=current_user.firstname)


@main.route('/profile', methods=['POST'])
def profile_post():

    datetime = request.form.get('datetime')
    incontact = request.form.get('incontact')
    temperature = request.form.get('temperature')
    fever = request.form.get('fever')
    drycough = request.form.get('drycough')
    sorethroat = request.form.get('sorethroat')
    feverdrycough = request.form.get('feverdrycough')
    feversorethroat = request.form.get('feversorethroat')
    drycoughsorethroat = request.form.get('drycoughsorethroat')
    difficultyinbreathing = request.form.get('difficultyinbreathing')

    new_questionnaire = Questionnaire(datetime=datetime, incontact=incontact, temperature=temperature, fever=fever,
                                      drycough=drycough, sorethroat=sorethroat, feverdrycough=feverdrycough,
                                      feversorethroat=feversorethroat, drycoughsorethroat=drycoughsorethroat,
                                      difficultyinbreathing=difficultyinbreathing, employee_id=current_user.id)

    db.session.add(new_questionnaire)
    db.session.commit()

    return redirect(url_for('main.index'))
