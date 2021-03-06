import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, jsonify, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Enrollment, Event, EventCategory, EventType, Location, Participant 
from schemes import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

admin = Admin(app)
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Location, db.session))
admin.add_view(ModelView(Enrollment, db.session))

@app.route('/locations/', methods=['GET'])
def locations_list():
    locations_schema = LocationSchema(many=True)
    return jsonify(locations_schema.dump(Location.query.all()))

@app.route('/events/', methods=['GET'])
def events_list():
    eventtype = request.args.get('eventtype')
    eventtype = db.session.query(EventType).filter_by(code=eventtype).one_or_none()
    location = request.args.get('location')
    location = db.session.query(Location).filter_by(code=location).one_or_none()
    events_schema = EventSchema(many=True)
    events = db.session.query(Event)
    if eventtype and location: 
        events = events.filter(
            Event.location == location, Event.type_event == eventtype)
    elif eventtype:
        events = events.filter(
            Event.type_event == eventtype).all()
    elif location:
        events = events.filter(Event.location == location)
    return jsonify(events_schema.dump(events))

@app.route('/enrollments/<int:event_id>', methods=['DELETE', 'POST'])
def enrollments_processing(event_id):
    user_id = session.get('user_id', None)
    today = datetime.datetime.today()
    date=today.strftime("%Y-%m-%d-%H:%M")
    if user_id == None:
        return {'error': 'User authorization failed'}, 400
    enrollments = db.session.query(Enrollment)
    event = db.session.query(Event).get(event_id)
    user = db.session.query(Participant).get(user_id)
    enrollment_with_user = enrollments.filter_by(
            event=event, participant=user).one_or_none()
    if request.method == 'POST':
        enrollments = enrollments.filter_by(event=event).all()
        if enrollment_with_user:
            return {"error":"The user is already registered"}, 400
        if len(enrollments) < event.seats:
            new_enrollment_schema = EnrollmentSchema()
            new_enrollment = Enrollment(
                datetime=date,
                event = event,
                participant=user
                )
            db.session.add(new_enrollment)
            db.session.commit()
            try:
                db.session.commit()
            except:
                return jsonify(), 500
            return jsonify(new_enrollment_schema.dump(new_enrollment)), 201, \
              {'Location': f'/enrollments/{new_enrollment.id}'}
        else:
            return {"error":"Not enough seats"}, 400
    elif request.method == 'DELETE':
        if enrollment_with_user:
            db.session.delete(enrollment_with_user)
            try:
                db.session.commit()
            except:
                return jsonify(), 500
            return  204
        else:
            return jsonify(), 204

@app.route('/register/', methods=['POST'])
def register_user():
    data = request.json
    user = db.session.query(Participant).filter_by(
        email=data.get('email')).one_or_none()
    if user:
        return jsonify({'error':'Already exists'})
    new_user_schema = ParticipantSchema()
    new_user = Participant(
        name=data.get('name'),
        email=data.get('email'),
        picture=data.get('picture'),
        location=data.get('location'),
        about=data.get('about') 
    )
    new_user.password = data.get('password')
    db.session.add(new_user)
    try:
        db.session.commit()
    except:
        return jsonify(), 500
    return jsonify(new_user_schema.dump(new_user)), 201, {'Location': f'/login/{new_user.id}'}

@app.route('/auth/', methods=['POST'])
def auth_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user_schema = ParticipantSchema()
    user = db.session.query(Participant).filter_by(
        email=email).one_or_none()
    if user and user.password_valid(password):
        session['user_id'] = user.id
        return jsonify(user_schema.dump(user)), 200
    else:
        return {'error': 'Wrong password'}, 400

@app.route('/logout/', methods=['POST'])
def logout_user():
    session.clear()
    return jsonify(), 200

@app.route('/profile/', methods=['GET'])
def get_profile():
    user_id = session.get('user_id', None)
    if user_id:
        user = db.session.query(Participant).get(user_id)
        user_schema = ParticipantSchema()
    return jsonify(user_schema.dump(user)), 200

@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'

if __name__ == '__main__':
    app.run()
    