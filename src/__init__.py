"""Initialize Flask app."""
from flask import Flask
from .models import db
from .dashapp import dataprocessor
from tempfile import mkdtemp


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)

    # Path and files
    UPLOAD_FOLDER = dataprocessor.get_data_path("DATA_PATH")
    DATABASE_URI = dataprocessor.get_data_path("DATABASE_URI")

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
    db.init_app(app)
    # app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        db.create_all()
        # # Import Dash applications
        from .dashapp.oncomine import create_oncomine
        from .dashapp.targeted import create_targeted
        from .dashapp.rapidexome import create_rapidexome
        from .dashapp.prenatal import create_prenatal
        from .dashapp.familial import create_familial
        from .dashapp.exome import create_exome

        app = create_oncomine(app)
        app = create_targeted(app)
        app = create_rapidexome(app)
        app = create_prenatal(app)
        app = create_familial(app)
        app = create_exome(app)

        return app