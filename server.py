"""Flask site for TacoHops app."""

from flask import (Flask, session, render_template, request, flash, redirect)
from os import environ

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "TacosBeerTacosBeer"
app.jinja_env.undefined = StrictUndefined
print(environ.get('API_TOKEN'))

#create routes and view functions

#index page verify user age to access website
@app.route('/')
def verify_age_page():
    """returns index page and verifies user's age"""
    #html form should veriyf that DOB is 21 years ago
    #if DOB is less than 21 years ago reroute to goodbye page
    #if DOB is 21 years or older reroute to homepage
    
    return render_template('index.html')

@app.route('/', methods=['POST'])
def verify_age():
    #TODO:
    #user input-Date
        # #if the date < 21 years ago
        #     redirect ('/goodbye')
        # else:
            session['is of age']=True
            return redirect('/homepage')

#homepage that gives option to log in or create account

@app.route('/homepage')
def homepage():
#     #button/form option to log-in for exisiting users
#         #do i need a listening event for submit button?
#     #button/form option to create a new account
#         #do i need a listening event for submit button?
#     #?do I want a non-log-in option to just go to search page?
    old_enough=session.get('is of age', False)
    print(old_enough)
    if old_enough is False:
        return redirect('/goodbye')
        #TODO:make goodbye route

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
    else:
        # Log in user by storing the user's email in session
        session["email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect ("/search_by_brewery")

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
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.")

    return redirect("/homepage") 

#search page - user can view a map and start a search for a brewery
@app.route('/search_by_brewery')
def search_brewery():
    """Returns page to search for brewery"""

    return render_template('search_by_brewery.html')



#another page or view route?
    #search returns- brewery with list of tacoshops near by

    #user can click on brewery name and get...(Yelp page?)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)