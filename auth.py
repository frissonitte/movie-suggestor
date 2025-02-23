from flask import Blueprint, render_template, redirect, flash, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

auth = Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@auth.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username:
            flash("must provide username", "danger")
            return redirect("/login")

        elif not password:
            flash("must provide password", "danger")
            return redirect("/login")
        from app import get_db
        rows = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchall()

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password):
            flash("invalid username and/or password", "danger")
            return redirect("/login")

        session["user_id"] = rows[0]["id"]
        flash("Login successful!", "success")
        return redirect("/")

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/")

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            flash("Must provide username, password, and confirmation", "danger")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords do not match", "danger")
            return redirect("/register")

        from app import get_db
        existing_user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if existing_user:
            flash("username already taken", "danger")
            return redirect("/register")

        hash = generate_password_hash(password)

        get_db().execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
        get_db().commit()

        flash("Registration successful! Please log in.", "success")
        return redirect("/login")

    return render_template("register.html")

