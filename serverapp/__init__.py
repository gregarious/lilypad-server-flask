from flask import Flask
from mongokit import Connection

app = Flask(__name__)

app.config.from_object('config.default')
app.config.from_envvar('LILYPAD_DEPLOY_SETTINGS')

connection = Connection(
    app.config.get('MONGODB_HOST', 'localhost'),
    app.config.get('MONDODB_PORT', 27017))

db = connection[app.config.get('MONGODB_DATABASE')]

import serverapp.views
