"""Flask site for TacoHops app."""

from flask import (Flask, session, render_template, request, flash, redirect)
# from model import ...

#from jinja2 import...

app = Flask(__name__)
app.secret_key = "TacosBeerTacosBeer"
#app.jinja...
