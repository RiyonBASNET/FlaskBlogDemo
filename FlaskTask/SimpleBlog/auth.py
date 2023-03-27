from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Email and password mismatch', category='error')
        else:
            flash('Email does not exist!', category='error')

    return render_template("login.html")


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email already exists', category='error')
        elif username_exists:
            flash('Username already exists', category='error')
        elif password != cpassword:
            flash('Passwords don\'t match', category='error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters', category='error')
        elif len(password) < 8:
            flash('Password must be 8 characters', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("register.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
