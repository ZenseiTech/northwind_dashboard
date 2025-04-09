"""Authorization view."""
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from ..models import User
from . import auth
from .forms import LoginForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Login user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid email or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """Logout user."""
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))
