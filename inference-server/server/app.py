import os
import time

from flask import Flask
from flask_cors import CORS

import server.routes as routes

def create_app():

    app = Flask(__name__)
    CORS(app)
    app = routes.add_app_routes(app)
    return app