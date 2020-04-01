from marshmallow import Schema, fields


class EnrollmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    datetime = fields.String()

class EventSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description  = fields.String(required=True)
    date = fields.String(required=True)
    time = fields.String(required=True)
    address = fields.String()
    seats = fields.Integer()
    category = fields.Nested("EventCategorySchema")
    enrollment = fields.Nested("EnrollmentSchema")
    location = fields.Nested("LocationSchema")
    type_event = fields.Nested("EventTypeSchema")

class EventCategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    code  = fields.String()

class EventTypeSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    code  = fields.String()

class LocationSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    code  = fields.String()

class ParticipantSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    email  = fields.String()
    picture = fields.String()
    location = fields.String()
    about = fields.String()
    enrollments = fields.Nested("EnrollmentSchema")
    event = fields.Nested("EventSchema")

