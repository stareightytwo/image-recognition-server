"""Configuration file for gunicorn. Not able to make a class like
the test/prod app configs in config.py

http://docs.gunicorn.org/en/stable/settings.html
"""

import os


bind = '0.0.0.0:{}'.format(os.environ.get('PORT', 8000))
workers = int(os.environ.get('PROCESSES', 1))
threads = int(os.environ.get('THREADS', 4))

# http://docs.gunicorn.org/en/stable/settings.html#loglevel
loglevel = os.environ.get('LOG_LEVEL', 'debug')