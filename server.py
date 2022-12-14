"""Flask site for TacoHops app."""

from flask import (Flask, session, render_template, request, flash, redirect, jsonify)
from os import environ
from datetime import date, datetime
from pprint import pformat
import requests
import json


from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "TacosBeerTacosBeer"
app.jinja_env.undefined = StrictUndefined
API_KEY=environ.get('API_TOKEN')
G_API_KEY=environ.get('G_API_TOKEN')
MB_API_TOKEN=environ.get('MB_API_TOKEN')


@app.route('/')
def verify_age_page():
    """returns index page and collects DOB of user"""

    return render_template('index.html')


@app.route('/', methods=['POST'])
def verify_age():
    """takes users DOB and verifies if they are 21 or over"""
    birthDate=request.form['birthDate']
    birthDate_object=datetime.strptime(birthDate, '%Y-%m-%d').date()

    #verifies age and only lets 21 and over get to homepage.html
    if crud.are_you_21(birthDate_object) is True:
        session['is of age']=True
        return redirect('/homepage')



    #if not 21- user gets redirected to goodbye page
    return redirect('/goodbye')


#homepage that gives option to log in or create account
@app.route('/homepage')
def homepage():
    """Ensures that age remains in session to block out anyone not of age"""
    old_enough=session.get('is of age', False)

    if old_enough is False:
        return redirect('/goodbye')

    return render_template('homepage.html')
    

#users can log in with their account credentials
@app.route('/login', methods=["POST"])
def login_user():
    """Logs in existing user."""

    email = request.form.get("email")
    password=request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect ('/homepage')
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
        return redirect ('/brewery_trip_planner')


#users can create an account with email and password
@app.route('/create_new_user', methods =["POST"])
def create_new_user():
    """Creates a new user"""

    ###getting input from homepage.html Log-In Form
    email=request.form.get("email")
    password=request.form.get("password")

    ###function from crud.py to look up user info in User class
    user = crud.get_user_by_email(email)

    if user:
        flash("Email already in use. Try again.")
        return redirect ('/homepage')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.")
        return redirect("/homepage") 


#search page - user can view a map and start a search for a brewery
@app.route('/brewery_trip_planner')
def trip_planner():
    """Returns page to plan brewery and taco trip"""

    return render_template('brewery_trip_planner.html')

#user profile page
@app.route('/user_profile')
def user_profile():
    """Returns a page that has user profile info on it"""
    
    user=session["user_email"]

    
    return render_template('user_details.html', user=user)

#route for page display brewery's found and map
@app.route('/brewery_trip_planner/search')
def search_for_brewery():
    """Search for brewery through Yelp"""

    location = request.args.get('location')
    if not location:
        flash('Location required!')
        return redirect('/brewery_trip_planner')

    url ='https://api.yelp.com/v3/businesses/search' 
    headers = {'Authorization': 'Bearer '+API_KEY
    }
    
    payload ={  'term': 'brewery',
                'location': location
    }

    response = requests.get(url, headers=headers, params=payload)
    brewery_results=response.json()
    breweries=brewery_results['businesses']
    center=[brewery_results['region']['center']['longitude'], brewery_results['region']['center']['latitude']]

    for brewery in breweries:
        address=" ".join(brewery['location']['display_address'])
        brewery['address']=address

    return render_template("brewery_search_results.html", breweries=breweries,  center=center, location=location)


@app.route('/fav_brewery')
def favorite_brewery(user, brewery):
    """user can click on button to save favorite brewery when logged in"""

    print("Who is user in session?")
    user=session["user_email"] # should this be user id instead?

    #PROCESS POST REQUEST

    brewery=crud.add_fav_brewery (brewery_id, name, address, favorite_brewery)

    flash("Brewery Added to Favorites Succesfully!")
    
    return ("Success")  #what should be returned to Fetch? Is "success" adequate?


#route for page dispaly taco shops found near brewery and map
@app.route('/taco')
def tacoshops_nearby():
    "Search for tacoshop based on selected brewery location through Yelp"

    lat=request.args.get("lat")
    long=request.args.get("long")

    name=request.args.get("name")

    url ='https://api.yelp.com/v3/businesses/search' 
    headers = {'Authorization': 'Bearer '+API_KEY
    }
    
    payload ={  'term': 'taco shop',
                'longitude': long,
                'latitude': lat
    }

    taco_map_center=[long, lat]
    print(taco_map_center) #prints correct long, lat

    response = requests.get(url, headers=headers, params=payload)
    tacoshop_results=response.json()
    tacoshops=tacoshop_results['businesses']

    for tacoshop in tacoshops:
        address=" ".join(tacoshop['location']['display_address'])
        tacoshop['address']=address


    return render_template('tacoshops_nearby.html', tacoshops=tacoshops, name=name, taco_map_center=taco_map_center )


@app.route('/goodbye')
def goodbye_page():
    """Displays Goodbye page"""

    return render_template('goodbye.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


    ##example of returned infor from yelp api
    # {
#   "businesses": [
#     {
#       "alias": "golden-boy-pizza-hamburg",
#       "categories": [
#         {
#           "alias": "pizza",
#           "title": "Pizza"
#         },
#         {
#           "alias": "food",
#           "title": "Food"
#         }
#       ],
#       "coordinates": {
#         "latitude": 41.7873382568359,
#         "longitude": -123.051551818848
#       },
#       "display_phone": "(415) 982-9738",
#       "distance": 4992.437696561071,
#       "id": "QPOI0dYeAl3U8iPM_IYWnA",
#       "image_url": "https://yelp-photos.yelpcorp.com/bphoto/b0mx7p6x9Z1ivb8yzaU3dg/o.jpg",
#       "is_closed": true,
#       "location": {
#         "address1": "Herr",
#         "address2": "Wesselstraat",
#         "address3": "68c",
#         "city": "Hamburg",
#         "country": "US",
#         "display_address": [
#           "Herr",
#           "Wesselstraat",
#           "68c",
#           "Hamburg, CA 22399"
#         ],
#         "state": "CA",
#         "zip_code": "22399"
#       },
#       "name": "Golden Boy Pizza",
#       "phone": "+14159829738",
#       "price": "$",
#       "rating": 4,
#       "review_count": 903,
#       "transactions": [
#         "restaurant_reservation"
#       ],
#       "url": "https://www.yelp.com/biz/golden-boy-pizza-hamburg?adjust_creative=XsIsNkqpLmHqfJ51zfRn3A&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=XsIsNkqpLmHqfJ51zfRn3A"
#     }
#   ],
#   "region": {
#     "center": {
#       "latitude": 37.76089938976322,
#       "longitude": -122.43644714355469
#     }
#   },
#   "total": 6800
# }