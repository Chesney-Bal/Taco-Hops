"""CRUD operations"""
from model import db, User, Fav_Brewery, Fav_Tacoshop, connect_to_db
from datetime import date
from flask import (flash)

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

    return User.query.filter_by(email = email).first().user_id


def add_fav_brewery(user_id, brewery_id, name, address, is_favorite):
    """Creates and returns a brewery"""
    favorite=Fav_Brewery.query.filter((Fav_Brewery.brewery_id==brewery_id) & (Fav_Brewery.user_id==user_id)).first()
    if not favorite:
        print("brewery_id & user_id not found in Fav_brewery DB, create new record") #need this to search for brewery_id and User_id in one instance

        brewery= Fav_Brewery(
            user_id=user_id,
            brewery_id=brewery_id,  
            brewery_name=name,  #brewery_name naming convention is from db
            brewery_address=address,
            is_favorite=is_favorite,
        )

        db.session.add(brewery)
        db.session.commit()
        return True
    else:
        print("did not create new record")
        return False




if __name__=="__main__":
    from server import app
    connect_to_db(app)