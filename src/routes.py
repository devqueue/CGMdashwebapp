from flask import redirect, render_template, request, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask import current_app as flask_app
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps 
from .dashapp import dataprocessor
from .wtforms import LoginForm, RegistrationForm
from .models import User, db
import pathlib
import os


# Path and files
UPLOAD_FOLDER = dataprocessor.get_data_path("DATA_PATH")
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Ensure templates are auto-reloaded
flask_app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(flask_app)

# Ensure responses aren't cached
@flask_app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Initialize login manager
login = LoginManager(flask_app)
login.init_app(flask_app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# check allowed files
def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes
@flask_app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    login_form = LoginForm()
        
    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('upload'))

    # User reached route via GET
    return render_template("login.html", form=login_form)


@flask_app.route("/logout")
def logout():
    """Log user out"""

    # logout user
    logout_user()

    # Redirect user to login form
    return redirect("/")


@flask_app.route("/register", methods=["GET", "POST"])
def register():
    reg_form = RegistrationForm()

    # Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = generate_password_hash(password)

        # Add username & hashed password to DB
        user = User(username=username, hashed_pswd=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", form=reg_form)

@flask_app.route("/")
def index():
    return redirect("/oncomine")


@flask_app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    try:
        filesdir = os.listdir(UPLOAD_FOLDER)
    except os.error as e:
        print(e)
        filesdir = ''
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
    return render_template("embedd.html", location="/dashboard/oncomine")

@flask_app.route("/prenatal")
def prenatal_fn():
    return render_template("embedd.html", location='/dashboard/prenatal')

@flask_app.route("/familial")
def familial_fn():
    return render_template("embedd.html", location='/dashboard/familial')

@flask_app.route("/targeted")
def targeted_fn():
    return render_template("embedd.html", location='/dashboard/targeted')

@flask_app.route("/exome")
def exome_fn():
    return render_template("embedd.html", location='/dashboard/exome')

@flask_app.route("/flashexome")
def flashexome_fn():
    return render_template("embedd.html", location='/dashboard/flashexome')
