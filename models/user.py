"""User model for PostgreSQL database"""
from flask_sqlalchemy import SQLAlchemy
from database import db
from models.article import Article

class User(db.Model):
    """User Schema"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=True)
    articles = db.relationship('Article', back_populates='user')


    def __init__(self, email, password_hash, firstname, lastname):
        self.email = email
        self.password_hash = password_hash
        self.firstname = firstname
        self.lastname = lastname
