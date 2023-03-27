from flask import Blueprint, render_template
from flask_login import login_remembered, current_user

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", name=current_user.username)
