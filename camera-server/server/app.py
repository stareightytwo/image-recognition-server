#!/usr/bin/env python
import os
import time

from flask import Flask

from server import routes

def create_app():

    app = Flask(__name__)
    app = routes.add_app_routes(app)
    return app