"""Script to seed database."""

import os
from random import choice, randint

import crud
import model
import server

os.system('dropdb users')
os.system('createdb users')

model.connect_to_db(server.app)
model.db.create_all()

#create fake users
for n in range(10):
    
    email = f'beerdrinker{n}@taco.com'  
    password = 'cheers'

    user=crud.create_user(email, password)
    model.db.session.add(user)

model.db.session.commit()