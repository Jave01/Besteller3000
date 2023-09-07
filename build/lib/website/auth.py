from pathlib import Path
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Level
from . import db
from . import app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
import os

auth = Blueprint("auth", __name__)


def valid_char_set(string: str, allowed_charset: set):
    string = set(string)

    return string.issubset(allowed_charset)


def username_valid(username: str):
    secure_uname: str = secure_filename(username).lower()

    if secure_filename != username or not secure_filename.isalpha():
        return False, "contains invalid chars"
    if not secure_filename.is_alpha():
        return False, "contains non-valid chars"
    elif secure_filename == "admin":
        return False, "nope, not that one"


@auth.route("/login", methods=["GET", "POST"])
def login():

            login_user(user, remember=True)
            return redirect(url_for("views.home"))
        else:
            flash("Wrong", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get(
            "username"
        )  # id must match the 'name' attribute in the html file
        # email = request.form.get('email')     # not used yet
        password = request.form.get("password")
        confPassword = request.form.get("confPassword")
        acces_code = request.form.get("accessCode")

        user = User.query.filter_by(username=username).first()

        uname_valid, username_error_msg = username_valid(str(username))
        passwd_valid = valid_char_set(password, PASSWD_CHARS)

        if user:
            if "admin" in username:
                flash("Nope not that one please", category="error")
            else:
                flash("Username already taken", category="error")
        elif not uname_valid:
            flash(username_error_msg, category="error")
        elif not passwd_valid:
            flash(
                f"For passwords only characters, numbers and {ALLOWED_SPECIAL_CHARS} please",
                category="error",
            )
        elif password != confPassword:
            flash("Passwords are not matching", category="error")
        elif acces_code != app.config["ACCESS_CODE"]:
            flash("Alpha access code invalid", category="error")
        else:
            # personal files get stored in a folder named heroes/user_[username]
            heroes_path = os.path.join(app.config["UPLOAD_FOLDER"], "user_" + username)
            Path(heroes_path).mkdir(parents=True, exist_ok=True)
            new_user = User(
                username=username,
                password=generate_password_hash(password, method="sha256"),
                heroes_path=heroes_path,
                access_lvl=Level.USER,
            )  # add e-mail for later use
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(
                "Congratulations, you are now the proud owner, of a new account on this wonderful website!",
                category="success",
            )
            return redirect(url_for("views.home"))

    return render_template("sign-up.html", user=current_user)
