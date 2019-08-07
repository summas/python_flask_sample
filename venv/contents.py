from flask import Flask, request, render_template, redirect, url_for, abort
from werkzeug.utils import secure_filename
from random import random
from datetime import datetime
# from flask import Flask, login_user, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Contents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=True)
    contents = db.Column(db.String(144), index=True, unique=True)
    date_published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Contents%r>' % self.contents
