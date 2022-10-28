import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from common.database import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['first name']
        lastname = request.form['last name']
        phonenum = request.form['phone number']
        # TODO... check box that will open up extra inputs based on selection ie. teacher, volunteer etc
        db = get_db()
        error = None

        if not email:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user_info (email, password, firstname, lastname, phonenum) VALUES (?, ?, ?, "
                    "?, ?, ?)",
                    (email, generate_password_hash(password), firstname, lastname, phonenum),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User with {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# noinspection DuplicatedCode
@bp.route('/teacherinfo', methods=('GET', 'POST'))
def teacher_info():
    if request.method == 'POST':
        background_check_status = request.form['background check status']
        teacher_bg_description = request.form['artistic background description']
        # TODO... some sort of tag allowing access to creation of a class pending background check status
        db = get_db()
        error = None

        if not background_check_status:
            error = 'Background Check needs to be completed before teacher registration.'
        elif not teacher_bg_description:
            error = 'Your artistic background is needed for class descriptions.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user_info (background_check, teacher_bg_description) VALUES (?, ?)",
                    (background_check_status, teacher_bg_description),
                )
                db.commit()
            # TODO... I can see this as something that will be needed but I'm not sure how... background check status?
            except db.IntegrityError:
                error = f"Background Check Status is {background_check_status} and will need to be updated"
            else:
                # TODO... create "home" or return to previous form or page?
                return redirect(url_for("auth.home"))

        flash(error)

    return render_template('auth/teacherinfo.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
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


@bp.route('/class_submission', methods=('GET', 'POST'))
def class_submission():
    if request.method == 'POST':
        teacher_name = request.form['teacher name']
        class_name = request.form['class name']
        class_description = request.form['class description']
        max_students = request.form['max number of students']
        db = get_db()
        error = None

        if not teacher_name:
            error = 'Name Required'
        elif not class_name:
            error = 'Class Name is required.'
        elif not not class_description:
            error = 'Class Description is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO course_info (teacher_name, class_name, class_description, max_students) VALUES (?,"
                    "?, ?, ?, ?)",
                    (teacher_name, class_name, class_description, max_students),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Class {class_name} already exists."
            else:
                flash("Submission Complete")
                return redirect(url_for("auth.class_submission"))

        flash(error)

    return render_template('auth/class_submission.html')
