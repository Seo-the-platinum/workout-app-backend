from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime
    )
import os
db = SQLAlchemy()

database_path = (
    os.environ.get('DATABASE_URI')
)

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    
class Record(db.Model):
    __tablename__ = 'record'

    id = Column(Integer, primary_key=True)
    reps = Column(Integer)
    rest = Column(String)
    weight = Column(Integer, nullable=False)
    weight_units = Column(String(3), nullable=False)
    exercise = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    def __init__(self, reps, rest, weight, exercise, user_id, weight_units):
        self.reps = reps
        self.rest = rest
        self.weight = weight
        self.exercise= exercise
        self.user_id = user_id
        self.weight_units = weight_units

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'reps': self.reps,
            'rest': self.rest,
            'weight': self.weight,
            'exercise': self.exercise,
            'weight_units': self.weight_units,
        }

class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    email = Column(String(40), nullable=False)
    sex = Column(String(1), nullable=False)
    user_name = Column(String(25), nullable=False)
    feet = Column(Integer, nullable=False)
    inches = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    weight_units = Column(String(3), nullable=False)
    records = db.relationship(
        'Record',
        cascade = 'all, delete-orphan',
        backref = db.backref('lifter')
    )
 
    def __init__(self, age, email, user_name, feet, inches, weight, sex, weight_units):
        self.age = age
        self.email = email
        self.feet = feet
        self.inches = inches
        self.sex = sex
        self.user_name = user_name
        self.weight = weight
        self.weight_units = weight_units

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'age': self.age,
            'email': self.email,
            'feet': self.feet,
            'inches':self.inches,
            'sex': self.sex,
            'user_name': self.user_name,
            'weight': self.weight,
            'weight_units': self.weight_units,
        }
