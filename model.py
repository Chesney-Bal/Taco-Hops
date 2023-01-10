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

    fav_breweries=db.relationship("Fav_Brewery", back_populates="user")
    fav_tacoshops=db.relationship("Fav_Tacoshop", back_populates="user")
    

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Fav_Brewery(db.Model):
    """A brewery."""
    __tablename__ ="breweries"

    brewery_id = db.Column(db.String, primary_key=True) #come from yelp API bussiness[id]
    brewery_name=db.Column(db.String(50)) #businesses['name']
    brewery_address=db.Column(db.String(250))

    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    user=db.relationship("User", back_populates="fav_breweries") 

    def __repr__(self):
        return f'<Brewery brewery_id={self.brewery_id} brewery_name={self.brewery_name}>'    

class Fav_Tacoshop(db.Model):
    """A Tacoshop."""
    __tablename__ ="tacoshops"

    tacoshop_id = db.Column(db.String, primary_key=True) #come from yelp API bussiness[id]
    tacoshop_name=db.Column(db.String(50)) #businesses['name']
    tacoshop_address=db.Column(db.String(250))

    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user=db.relationship("User", back_populates="fav_tacoshops")

    def __repr__(self):
        return f'<Tacoshop tacoshop_id={self.tacoshop_id} tacoshop_name={self.tacoshop_name}>'  


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