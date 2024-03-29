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
MB_API_TOKEN=environ.get('MB_API_TOKEN')


@app.route('/')
def verify_age_page():
    """returns index page and collects DOB of user"""

    return render_template('index.html')


@app.route('/', methods=['POST'])
def verify_age():
    """takes users DOB and verifies if they are 21 or over"""

    birthDate=request.form['birthDate']
    if not birthDate:
        flash('Please enter full DOB mm/dd/yyyy.')
        return redirect('/')

    birthDate_object=datetime.strptime(birthDate, '%Y-%m-%d').date()


    #verifies age and only lets 21 and over get to homepage.html
    if crud.are_you_21(birthDate_object) is True:
        
        return redirect('/homepage')

    #if not 21- user gets redirected to goodbye page
    return redirect('/goodbye')


#homepage that gives option to log in or create account
@app.route('/homepage')
def homepage():
    """Ensures that age remains in session to block out anyone not of age"""

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
        
        return redirect ('/brewery_trip_planner')


@app.route('/logout')
def logout():
    """logs user out"""
    del session["user_email"]

    return redirect('/homepage')


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

    if 'user_email' in session:     #if logged in-user can access user profile page
        user_email=session["user_email"]

    else:
        user_email= None            #if not-logged in user can't acces user profile page
        flash ("Must be logged in to use see user profile page.") 
        return redirect('/brewery_trip_planner')

    user_id=crud.get_user_id_by_email(user_email)

    fav_breweries=crud.get_favorites_by_user_id(user_id)

    fav_tacoshops=crud.get_fav_tacoshop_by_user_id(user_id)
    
    return render_template('user_details.html', user_email=user_email, fav_breweries=fav_breweries, fav_tacoshops=fav_tacoshops)


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

    location=location.title()

    response = requests.get(url, headers=headers, params=payload)
    brewery_results=response.json()
    breweries=brewery_results['businesses']
    center=[brewery_results['region']['center']['longitude'], brewery_results['region']['center']['latitude']]

    for brewery in breweries:
        address=" ".join(brewery['location']['display_address'])
        brewery['address']=address

    return render_template("brewery_search_results.html", breweries=breweries,  center=center, location=location)


@app.route('/fav_brewery', methods=['POST'])
def favorite_brewery():
    """user can click on button to save favorite brewery when logged in"""

    if 'user_email' in session:     
        user_email=session["user_email"]
    else:
        user_email= None            
        flash ("Must be logged in to use Favorites Feature") 

    user_id=crud.get_user_id_by_email(user_email)

    brewery_id=request.json['brewery_id']
    name=request.json['brewery_name']
    address=request.json['brewery_address']
    is_favorite=True
    brewery_long=request.json['brewery_long']
    brewery_lat=request.json['brewery_lat']
    brewery_image_url=request.json['brewery_image_url']
    brewery_url=request.json['brewery_url']

    is_created = crud.add_fav_brewery (user_id, brewery_id, name, address, is_favorite, brewery_long=brewery_long, brewery_lat=brewery_lat, brewery_image_url=brewery_image_url, brewery_url=brewery_url)

    if is_created:
        return "Success", 201
        
    #return Success goes to response in javascript fetch
    return "Failure" , 409

        
#route for page dispaly taco shops found near brewery and map
@app.route('/taco')
def tacoshops_nearby():
    "Search for tacoshop based on selected brewery location through Yelp"

    lat=request.args.get("lat")
    long=request.args.get("long")

    brewery_name=request.args.get("name")

    url ='https://api.yelp.com/v3/businesses/search' 
    headers = {'Authorization': 'Bearer '+API_KEY
    }
    
    payload ={  'term': 'taco shop',
                'longitude': long,
                'latitude': lat
    }

    taco_map_center=[long, lat]

    response = requests.get(url, headers=headers, params=payload)
    tacoshop_results=response.json()
    tacoshops=tacoshop_results['businesses']

    for tacoshop in tacoshops:
        address=" ".join(tacoshop['location']['display_address'])
        tacoshop['address']=address

    return render_template('tacoshops_nearby.html', tacoshops=tacoshops, brewery_name=brewery_name, taco_map_center=taco_map_center )


@app.route('/fav_tacoshop', methods=['POST'])
def favorite_tacoshop():
    """user can click on button to save favorite tacoshop when logged in"""

    if 'user_email' in session:     
        user_email=session["user_email"]
    else:
        user_email= None           
        flash ("Must be logged in to use Favorites Feature") 

    user_id=crud.get_user_id_by_email(user_email)

    tacoshop_id=request.json['tacoshop_id']
    tacoshop_name=request.json['tacoshop_name']
    tacoshop_address=request.json['tacoshop_address']
    is_fav_tacoshop=True
    nearby_brewery=request.json['nearby_brewery']

    is_fav_tacoshop_created = crud.add_fav_tacoshop (user_id, tacoshop_id, tacoshop_name, tacoshop_address, is_fav_tacoshop, nearby_brewery)

    if is_fav_tacoshop_created:
        return "Success", 201

    #return Success goes to response in javascript fetch
    return "Failure" , 409


@app.route('/goodbye')
def goodbye_page():
    """Displays Goodbye page"""

    return render_template('goodbye.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)