"""Models for TacoHops app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Establish Classes"""

def connect_to_db(flask_app):
    pass
    # flask_app.config["pass"] = pass

    db.app=flask_app
    db.init_app(flask_app)

    print("Connected to db!")

if __name__=="__main__":
    # from server import app
    pass

# connect_to_db(app)