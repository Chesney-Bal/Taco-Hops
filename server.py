"""Flask site for TacoHops app."""

from flask import (Flask, session, render_template, request, flash, redirect)
from os import environ

from model import connect_to_db, db
import crud

#from jinja2 import...

app = Flask(__name__)
app.secret_key = "TacosBeerTacosBeer"
#app.jinja...
print(environ.get('API_TOKEN'))

#create view routes

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)