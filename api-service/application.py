from flask import Flask
from Flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app(**config_overides):
  app = Flask(__name__)

  # load config
  app.config_from_pyfile('settings.py')

  # apply overides
  app.config_update(config_overides)

  # set up db
  db.init_app(app)

  #import blueprints
  from home.views import home_app

  # register
  app.register_blueprints(home_app)

  return app 
