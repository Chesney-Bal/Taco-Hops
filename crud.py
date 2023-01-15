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


def add_fav_brewery(user_id, brewery_id, name, address, is_favorite, brewery_long, brewery_lat, brewery_image_url, brewery_url):
    """Creates a favorite brewery in Fav_Brewery Databse"""
    favorite=Fav_Brewery.query.filter((Fav_Brewery.brewery_id==brewery_id) & (Fav_Brewery.user_id==user_id)).first()
    #need this to search for brewery_id and User_id in one instance
    if not favorite:

        brewery= Fav_Brewery(
            user_id=user_id,
            brewery_id=brewery_id,  
            brewery_name=name,  #brewery_name naming convention is from db
            brewery_address=address,
            is_favorite=is_favorite,
            brewery_long=brewery_long,
            brewery_lat=brewery_lat,
            brewery_image_url=brewery_image_url,
            brewery_url=brewery_url,
        )

        db.session.add(brewery)
        db.session.commit()
        return True
    else:
        return False

def add_fav_tacoshop(user_id, tacoshop_id, tacoshop_name, tacoshop_address, is_fav_tacoshop, nearby_brewery):
    """Creates a favorite tacoshop in Fav_Tacoshop Databse"""
    fav_T=Fav_Tacoshop.query.filter((Fav_Tacoshop.tacoshop_id==tacoshop_id) & (Fav_Tacoshop.nearby_brewery==nearby_brewery) & (Fav_Tacoshop.user_id==user_id)).first()
    #need this to search for tacoshop_id and User_id in one instance
    if not fav_T:

        tacoshop= Fav_Tacoshop(
            user_id=user_id,
            tacoshop_id=tacoshop_id,  
            tacoshop_name=tacoshop_name,  #tacoshop_name naming convention is from db
            tacoshop_address=tacoshop_address,
            is_fav_tacoshop=is_fav_tacoshop,
            nearby_brewery=nearby_brewery,  #user hits to add brewery as a favorite if taco shop is favorited
        )

        db.session.add(tacoshop)
        db.session.commit()
        return True
    else:

        return False


def get_favorites_by_user_id(user_id):
    """returns favorite breweries by user_id"""
    
     #change function name to get_fav_brewery_by_user_id
     #confirm naming update across project

    return Fav_Brewery.query.filter_by(user_id=user_id).order_by(Fav_Brewery.brewery_name).all()

def get_fav_tacoshop_by_user_id(user_id):
    """returns favorite tacoshops by user_id"""

    return Fav_Tacoshop.query.filter_by(user_id=user_id).order_by(Fav_Tacoshop.tacoshop_name).all()


if __name__=="__main__":
    from server import app
    connect_to_db(app)