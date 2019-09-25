import functools

from flask import (
    Blueprint, flash, g, redirect,
    render_template, request, session,
    url_for
)
from werkzeug.security import (
    check_password_hash, generate_password_hash
)

from . import db

authBlueprint = Blueprint('auth', __name__, url_prefix='/auth')


@authBlueprint.route('/register', methods=('GET', 'POST'))
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            dbSession = db.GetSession()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'

            userExists = dbSession.query(db.User).filter_by(
                username=username).scalar()

            if userExists:
                error = 'User already exists.'

            if error is None:
                password = generate_password_hash(password)
                newUser = db.User(username=username, password=password)
                dbSession.add(newUser)
                dbSession.commit()
                dbSession.close()
                return redirect(url_for('auth.login'))

            flash(error)

        return render_template('auth/register.html')
    except Exception as authBlueprintException:
        dbSession.close()
        error = f"Something went wrong: {str(authBlueprintException)}"
        flash(error)
        return render_template('auth/register.html')


@authBlueprint.route('/login', methods=('GET', 'POST'))
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            dbSession = db.GetSession()
            error = None
            existingUser = dbSession.query(db.User).filter_by(
                username=username).scalar()

            if existingUser is None:
                error = 'Incorrect username.'
            elif not check_password_hash(existingUser.password, password):
                error = 'Incorrect password.'

            if error is None:
                dbSession.close()
                session['userId'] = existingUser.id
                return redirect(url_for('home.index'))
            
            flash(error)
        return render_template('auth/login.html')
    except Exception as authBlueprintException:
        dbSession.close()
        error = f"Something went wrong: {str(authBlueprintException)}"
        flash(error)
        return render_template('auth/login.html')


@authBlueprint.before_app_request
def load_logged_in_user():
    userId = session.get('userId')
    dbSession = db.GetSession()

    if userId is None:
        g.user = None
    else:
        existingUser = dbSession.query(db.User).filter_by(id=userId).scalar()
        g.user = existingUser


@authBlueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
