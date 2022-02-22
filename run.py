"""Entry point to flask application that is called with gunicorn"""

from api import app

if __name__ == "__main__":
    # Can run app from bash with command - python3 run.py
    app.run()
