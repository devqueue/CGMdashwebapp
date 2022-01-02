from src import init_app
import os
from waitress import serve

app = init_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # serve(app, host="0.0.0.0", port=port)


