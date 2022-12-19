"""Flask site for TacoHops app."""

from flask import (Flask, session, render_template, request, flash, redirect)
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

#create routes and view functions


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


@app.route('/brewery_trip_planner/search')
def search_for_brewery():
    "Search for brewery through Yelp"

    term = request.args.get('term', 'brewery')
    location = request.args.get('location', '')
    radius = request.args.get('radius', '')


    url ='https://api.yelp.com/v3/businesses/search' 
    headers = {'Authorization': 'Bearer '+API_KEY

    }
    payload ={  'term': term,
                'location': location,
                'radius': radius
    }

    response = requests.get(url, headers=headers, params=payload)
    brewery_results=response.json()
  
    for brewery in brewery_results:
        brewery_name=brewery_results['name']
        brewery_image=brewery_results['image_url']
        brewery_closed=brewery_results['is_closed']
        brewery_yelp_url=brewery_results['url']
        brewery_long_lat=brewery_results['coordinates']
        brewery_address=brewery_results["location['display_address']"]


    # print(f'Attempt to access Yelp API: {brewery_results}')
    
###this variables? are throwing an erroras syntax error- how do I take the dict results and transfer them into Jinja? Also not showing up in html being rendered
    return render_template("brewery_search_results.html", brewery, brewery_name=brewery_name, brewery_image=brewery_image, brewery_closed=brewery_closed, brewery_yelp_url=brewery_yelp_url, brewery_yelp_url=brewery_long_lat, brewery_address=brewery_address)


#results page - user can view a map and results from search
@app.route('/brewery_search_results')
def search_results():
    """Returns page with brewery search results"""

    return render_template('brewery_search_results.html')

@app.route('/brewery_search_results/results')
def display_results():
    """Displays the results from the search"""
    #TODO: display the results of the YELP API search and coordainte with map


#another page or view route?
    #search returns- brewery with list of tacoshops near by

    #user can click on brewery name and get...(Yelp page?)


@app.route('/goodbye')
def goodbye_page():
    """Displays Goodbye page"""

    return render_template('goodbye.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)