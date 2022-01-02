import os
from . import sql
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from . import helpers 
from flask import current_app as flask_app

login_required = helpers.login_required
allowed_file = helpers.allowed_file

# Path and files
UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Ensure templates are auto-reloaded
flask_app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@flask_app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
flask_app.config["SESSION_FILE_DIR"] = mkdtemp()
flask_app.config["SESSION_PERMANENT"] = False
flask_app.config["SESSION_TYPE"] = "filesystem"
flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(flask_app)

# Configure CS50 Library to use SQLite database
db = sql.SQL("sqlite:///users.db")


# Routes
@flask_app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username", "warning")
            return render_template("login.html")
        elif not request.form.get("password"):
            flash("must provide password", "warning")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password", "danger")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/upload")

    # User reached route via GET
    else:
        return render_template("login.html")


@flask_app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@flask_app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        try:
            db.execute("CREATE TABLE if not exists users(id integer primary key ,username text unique, hash text)")
        except:
            flash('Internal server error occured.', "warning")
            return render_template("register.html")

        if not username:
            flash('Username is required.', "warning")
            return render_template("register.html") 
        elif not password:
            flash('Password is required', "warning")
            return render_template("register.html") 
        elif not confirmation:
            flash('Password is required', "warning")
            return render_template("register.html")
        elif password != confirmation:
            flash('Passwords do not match', "danger")
            return render_template("register.html") 

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect('/login')
        except:
            flash('Username has already been registered.', "info")
            return render_template("register.html")
    else:
        return render_template("register.html")

@flask_app.route("/")
def index():
    return redirect("/oncomine")


@flask_app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    filesdir = os.listdir(UPLOAD_FOLDER)
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', "danger")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file', "danger")
            return redirect(request.url)

        if not allowed_file(file.filename, ALLOWED_EXTENSIONS):
            flash("File type not allowed", "danger")
            return redirect(request.url)

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            os.makedirs(flask_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(flask_app.config['UPLOAD_FOLDER'], filename))
            flash("file uploaded sucessfully.", "success")
            return redirect(request.url)
    else:
        return render_template("upload.html", filesdir=filesdir)


@flask_app.route("/oncomine")
def oncomine_fn():
    return render_template("oncomine.html")

@flask_app.route("/prenatal")
def prenatal_fn():
    return render_template("oncomine.html")

@flask_app.route("/familial")
def familial_fn():
    return render_template("oncomine.html")

@flask_app.route("/targeted")
def targeted_fn():
    return render_template("oncomine.html")

@flask_app.route("/exome")
def exome_fn():
    return render_template("oncomine.html")

@flask_app.route("/flashexome")
def flashexome_fn():
    return render_template("oncomine.html")
