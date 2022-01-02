"""Initialize Flask app."""
from flask import Flask


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

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