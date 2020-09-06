import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        category = None

        if not username:
            error = 'Username is required!'
            category = "error"
        elif not password:
            error = 'Password is required!'
            category = "error"
        elif db.execute(
            'SELECT id_user FROM users WHERE user_name = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registerd!'.format(username)
            category = "Info"

        if error is None:
            db.execute(
                'INSERT INTO users (user_name,password) VALUES (?,?)', (
                    username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error,category)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT user_name FROM users WHERE user_name = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username!'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password!'

        if error is None:
            session.clear()
            session['id_user'] = user['id_user']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    id_user = session.get('id_user')

    if id_user is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id_user = ?', (id_user,)
        ).fetchone()


@bp.route('/logout')
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
