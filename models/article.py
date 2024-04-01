from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from database import db

class Article(db.Model):
    """Article database schema"""
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user = db.relationship('User', back_populates='articles')

    def __init__(self, user_id, title, content):
        self.user_id = user_id
        self.title = title
        self.content = content
