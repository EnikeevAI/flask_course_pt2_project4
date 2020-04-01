from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, jsonify, render_template, request
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
    data = request.json
    eventtype = request.args.get('eventtype')
    print(data)
    eventtype = db.session.query(EventType).filter_by(code=eventtype).one_or_none()
    location = request.args.get('location')
    location = db.session.query(Location).filter_by(code=location).one_or_none()
    events_schema = EventSchema(many=True)
    events = db.session.query(Event)
    print(eventtype, location)
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
    return jsonify({"status":"success"})

@app.route('/register/', methods=['POST'])
def register_user():
    return jsonify({"status":"ok","id":1})

@app.route('/auth/', methods=['POST'])
def auth_user():
    return jsonify({"status":"success","key":111111111})

@app.route('/profile/', methods=['GET'])
def get_profile():
    return jsonify({"id":1,"picture":"","city":"nsk","about":"", 'enrollments':[]})

@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'

if __name__ == '__main__':
    app.run()