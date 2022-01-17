from src import init_app
import os
from gevent.pywsgi import WSGIServer


app = init_app()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print("[Info] Started app on port: ",port)

    server = WSGIServer(('', port), app)
    server.serve_forever()

