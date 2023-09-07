from flask import Blueprint, flash, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFError
from . import app
from .models import User, Level
from .tools.upload import UploadFileForm, save_hero
import logger


views = Blueprint("views", __name__)


@views.route('/')
@views.route("/home", meethods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form.get("password")
        if check_password_hash(, password):

        
    return render_template("home.html", user=current_user)


@views.route('/overview')
@login_required
def overview():
    return render_template("overview.html", user=current_user)

@views.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)


# @views.route('/admin-panel', methods=['GET', 'POST'])
# @login_required
# def admin_panel():
#     if current_user.access_lvl == Level.ADMIN:
#         if request.method == "GET":
#             all_users = User.query.all()
#         return render_template("admin-panel.html", user=current_user, all_users=all_users)
#     else:
#         return redirect(url_for("views.home"))


# Server request size to large
@app.errorhandler(413)
def too_large(e):
    flash("Upload size too large", category='error')
    return redirect(url_for("views.overview"))

# wrong url
@app.errorhandler(404)
def server_error(e):
    return "<h1>Page not found</h1>"

#internal server error
@app.errorhandler(500)
def server_error(e):
    return "<h1>Internal server error</h1><p>Please contact me with the steps you just made before this happened</p>"

@app.errorhandler(CSRFError)
def csrf_error(e):
    logger.error(f"CSRF error: {e}")
    return f"Sorry, this request could not be executed.\nError: {e}"