"""Flask site for TacoHops app."""

from flask import (Flask, session, render_template, request, flash, redirect)
from os import environ
from datetime import date, datetime

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "TacosBeerTacosBeer"
app.jinja_env.undefined = StrictUndefined
print(environ.get('API_TOKEN'))

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
        return redirect ('/search_by_brewery')


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
@app.route('/search_by_brewery')
def search_brewery():
    """Returns page to search for brewery"""

    return render_template('search_by_brewery.html')



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