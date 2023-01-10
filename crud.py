"""CRUD operations"""
from model import db, User, Brewery, Tacoshop, Favorites, connect_to_db
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
    
    
    user_id=User.email
    
    print(user_id)

    return User.query.filter(user_id == user_id)


def get_brewery_info_from_api():
    
#from @app.route('brewery_trip_planner/search'): is the following code- will this work in crdu.py?????
    url ='https://api.yelp.com/v3/businesses/search' 
    headers = {'Authorization': 'Bearer '+API_KEY
    }
    
    payload ={  'term': 'brewery',
                'location': location
    }
    response = requests.get(url, headers=headers, params=payload)
    brewery_results=response.json()
    breweries=brewery_results['businesses']
    return breweries



def add_fav_brewery(email, brewery_name):
    """Add user favorite brewery to database"""

#??How do I ensure that the brewery_record info is coming from API after a search (is above call sufficient????)
#??Should the brewery_record go in Brewery db or Favorites db? (currently going to Brewery)
#??favorites can be an Association databse between Users and Brewery/Tacoshop db but Brewery/Tacoshops should update from search not from db

    if not Brewery.query.get(brewery_name):
        print("Brewery not found in db yet")
        brewery= get_brewery_info_from_api()  #??create this function to get info from search-do I need to specify a specific establishment?
        dispaly_address=get_address_from_brewery(brewery)
        image_url=get_image_url(brewery)

    brewery_record = create_brewery(
        brewery_id=brewery_id #brewery_id is primary_key in Brewery.db in model.py
        brewery_name=breweries['name'], #will this pull the name from the API search
        brewery_address=breweries['locatin']['display_address'],     #will this pull the address from the API search   
        brewery_website=breweries['url'], #will this pull the url from the API search
        brewery_image=breweries['image_url'], #will this pull image name from the API search
    )

    print('Created brewery')
    db.session.add(brewery_record)
    db.session.commit()

    #add this brewery to user favorites (Favorite db)
    favorite_brewery= Favorites(brewery_name=brewery_name, email=email)
    db.session.add(favorite_brewery)
    db.session.commit()
    # try:
    #     db.session.commit()
    # except IntegrityError as e:
    #     print("exception was caught")
    #     return "Fail"
    # return "Success"


if __name__=="__main__":
    from server import app
    connect_to_db(app)