"""CRUD operations"""
from model import db, User, Brewery, Tacoshop, Pairing, connect_to_db


#functions start here!

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

if __name__=="__main__":
    from server import app
    connect_to_db(app)