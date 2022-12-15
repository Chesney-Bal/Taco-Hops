"""CRUD operations"""
from model import db, User, Brewery, Tacoshop, Pairing, connect_to_db


#functions start here!

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_user_by_email (email):
    """Return a user by email"""
    return User.query.filter(User.email == email).first()


def are_you_21 (DOB):
    """Is the user old enough?"""
    #if today's date - DOB != 21 years
        #return flash message, "You are not old enough. Goodbye!"
        #return user to Goodbye page
    #else:
        # return user to homepage to log in


if __name__=="__main__":
    from server import app
    connect_to_db(app)