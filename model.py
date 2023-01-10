"""Models for TacoHops app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Establish Classes"""

class User(db.Model):
    """A user."""
    __tablename__ ="users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String (100), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

    favorites=db.relationship("Favorites", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Brewery(db.Model):
    """A brewery."""
    __tablename__ ="breweries"

    brewery_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.Integer, db.ForeignKey('users.email'))
    brewery_name=db.Column(db.String(50)) #businesses['name']
    brewery_address=db.Column(db.String(250))
    brewery_website=db.Column(db.String) #businesses['url']
    brewery_image=db.Column(db.String) #businesses['image_url']

    favorites=db.relationship("Favorites", back_populates="brewery")

    def __repr__(self):
        return f'<Brewery brewery_id={self.brewery_id} brewery_name={self.brewery_name}>'    

class Tacoshop(db.Model):
    """A Tacoshop."""
    __tablename__ ="tacoshops"

    tacoshop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tacoshop_name=db.Column(db.String(50))
    tacoshop_address=db.Column(db.String(250))
    tacoshop_website=db.Column(db.String)
    tacoshop_image=db.Column(db.String)

    favorites=db.relationship("Favorites", back_populates="tacoshop")

    def __repr__(self):
        return f'<Tacoshop tacoshop_id={self.tacoshop_id} tacoshop_name={self.tacoshop_name}>'  

class Favorites(db.Model):
    """Users favorite taco shops and breweries"""
    __tablename__="favorites"

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.Integer, db.ForeignKey('users.email'))
    brewery_id=db.Column(db.Integer, db.ForeignKey('breweries.brewery_id'))
    tacoshop_id=db.Column(db.Integer, db.ForeignKey('tacoshops.tacoshop_id'))

    user=db.relationship("User", back_populates="favorites")
    brewery=db.relationship("Brewery", back_populates="favorites")
    tacoshop=db.relationship("Tacoshop", back_populates="favorites")

    def __repr__(self):
        return f'<Favorites favorite_id={self.favorite_id} tacoshop_id={self.tacoshop_id} brewery_id={self.brewery_id} email={self.email}>'  


def connect_to_db(flask_app, db_uri="postgresql:///users", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.app=flask_app
    db.init_app(flask_app)

    print("Connected to db!")

if __name__=="__main__":
    from server import app
    connect_to_db(app)