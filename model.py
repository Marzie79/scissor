from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

Migrate(app, db)


class Url(db.Model):
    __tablename__ = 'my_url'
    id = db.Column(db.INTEGER, primary_key=True)
    long_url = db.Column(db.Text)
    short_url = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=True)
