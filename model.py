"""Models for TacoHops app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Establish Classes"""

class User(db.Model):
    """A user."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String (25),nullable=False)
    email = db.Column(db.String (100), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

    pairing=db.relationship("Pairing", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} user_name={self.user_name}>'

class Brewery(db.Model):
    """A brewery."""
    __tablename__ = "breweries"

    brewery_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    brewery_name=db.Column(db.String(50))
    # brewery_lat_long=db.Column(pass) ###CONFIRM DATATYPE#####
    brewery_address=db.Column(db.String(250))
    brewery_website=db.Column(db.String)
    brewery_image=db.Column(db.String)

    pairing=db.relationship("Pairing", back_populates="brewery")

    def __repr__(self):
        return f'<Brewery brewery_id={self.brewery_id} brewery_name={self.brewery_name}>'    

class Tacoshop(db.Model):
    """A Tacoshop."""
    __tablename__ = "tacoshops"

    tacoshop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tacoshop_name=db.Column(db.String(50))
    # tacoshop_lat_long=db.Column(pass) ###CONFIRM DATATYPE#####
    tacoshop_address=db.Column(db.String(250))
    tacoshop_website=db.Column(db.String)
    tacoshop_image=db.Column(db.String)

    pairing=db.relationship("Pairing", back_populates="tacoshop")

    def __repr__(self):
        return f'<Tacoshop tacoshop_id={self.tacoshop_id} tacoshop_name={self.tacoshop_name}>'  

class Pairing(db.Model):
    """A pairing of a brewery and tacoshop"""
    __tablename__= "pairings"

    pairing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    brewery_id=db.Column(db.Integer, db.ForeignKey('breweries.brewery_id'))
    tacoshop_id=db.Column(db.Integer, db.ForeignKey('tacoshops.tacoshop_id'))

    user=db.relationship("User", back_populates="pairing")
    brewery=db.relationship("Brewery", back_populates="pairing")
    tacoshop=db.relationship("Tacoshop", back_populates="pairing")

    def __repr__(self):
        return f'<Pairing pairing_id={self.pairing_id} tacoshop_id={self.tacoshop_id} brewery_id={self.brewery_id}>'  


def connect_to_db(flask_app):
    pass
    # flask_app.config["pass"] = pass

    db.app=flask_app
    db.init_app(flask_app)

    print("Connected to db!")

if __name__=="__main__":
    from server import app


connect_to_db(app)