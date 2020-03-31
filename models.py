from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    participants = db.relationship('Participant')

    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"))
    enrollments = db.relationship('Enrollment')

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship('Location')

class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, unique=True)
    picture = db.Column(db.String(100))
    location = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(500))

    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"))
    enrollments = db.relationship('Enrollment')

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event')

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(30), nullable=False)
    event = db.relationship('Event')
    participant = db.relationship('Participant')

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    events = db.relationship('Event')


if __name__ == '__main__':
    db.create_all()