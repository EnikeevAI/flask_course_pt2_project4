import csv
from flask_sqlalchemy import SQLAlchemy
from models import db, Enrollment, Event, EventCategory, EventType, Location, Participant 


location_csv = "data/meetup_locations.csv"
event_categories_csv = "data/meetup_categories.csv"
event_types_csv = "data/meetup_types.csv"

def db_add_objects_with_code_title(csv_file_path, db_model):
    with open(csv_file_path, "r") as f:
        rows = csv.reader(f)
        for row in rows:
            if row[0] != 'code':
                code = row[0]
                title = row[1]
                object_db = db_model(title=title, code=code)
                db.session.add(object_db)

def db_add_event():
    with open("data/meetup_events.csv", "r") as f:
        events = csv.reader(f)
        for event in events:
            if event[0] != 'title':
                event_title = event[0]
                event_description = event[1]
                event_date = event[2]
                event_time = event[3]
                event_category = db.session.query(
                    EventCategory).filter_by(code=event[4]).first()
                event_type = db.session.query(
                    EventType).filter_by(code=event[5]).first()
                event_location = db.session.query(
                    Location).filter_by(code=event[6]).first()
                event_address = event[7]
                event_seats = event[8]
                event_db = Event(
                    title = event_title,
                    description = event_description,
                    date = event_date,
                    time = event_time,
                    address = event_address,
                    seats = event_seats,
                    category = event_category,
                    type_event = event_type,
                    location = event_location
                )
                db.session.add(event_db)

if __name__ == '__main__':
    db_add_objects_with_code_title(location_csv, Location)
    db_add_objects_with_code_title(event_categories_csv, EventCategory)
    db_add_objects_with_code_title(event_types_csv, EventType)
    db_add_event()
    db.session.commit()