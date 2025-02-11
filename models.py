from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return self.name
    

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    value = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(100))
    deadline = db.Column(db.DateTime, default=datetime.now, nullable=True)
    created_in = db.Column(db.DateTime, default=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

    def __repr__(self):
        return f'<Item {self.id} - {self.description}>'
