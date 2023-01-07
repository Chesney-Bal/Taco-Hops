"""CRUD operations"""
from model import db, User, Brewery, Tacoshop, Pairing, connect_to_db
from datetime import date

#functions start here!

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)


    return user

def get_user_by_email (email):
    """Return a user by email"""
    return User.query.filter(User.email == email).first()


def calculateAge(birthDate):
    today=date.today()
    age= today.year -birthDate.year - ((today.month, today.day)<(birthDate.month, birthDate.day))
    return age

def are_you_21 (birthDate):
    """Is the user old enough?"""
    age = calculateAge(birthDate)
    if age >= 21:
        return True

    else:
        return False


def get_user_id_by_email (email):
    """returns user_id using email to search database"""
    
    
    user_id=User.email(user_id=user_id)
    
    print(user_id)

    return User.query.filter(user_id == user_id)





if __name__=="__main__":
    from server import app
    connect_to_db(app)