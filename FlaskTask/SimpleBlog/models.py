from datetime import datetime
from time import time
from . import db
from flask_login import UserMixin
import re


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(
        timezone=True), default=datetime.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(150), unique=True)
    date_created = db.Column(db.DateTime(
        timezone=True), default=datetime.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}>'
