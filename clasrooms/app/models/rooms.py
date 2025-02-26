from mongoengine import Document,EmbeddedDocument,StringField,IntField,DateTimeField,EnumField,ListField,EmbeddedDocumentField
from datetime import datetime
from enum import Enum

class Activity(Enum):
    MEETING = "meeting"
    LECTURE = "lecture"
    WORKSHOP = "workshop"
    PROJECT = "project"
    OTHER = "other"

class Room(EmbeddedDocument):
    name = StringField(required = True)
    capacity = IntField(required = True)

class Schedule(Document):
    rooms = EmbeddedDocumentField(Room)
    start = DateTimeField(required = True)
    end = DateTimeField(required = True)
    group_name = StringField(required = True)
    activity = EnumField(Activity,required=True)

def to_dict(self):
    return {
        "rooms":{
            "name": self.rooms.name,
            "capacity": self.rooms.capacity
        },
        "start": self.start,
        "end": self.end,
        "group_name": self.group_name,
        "activity": self.activity.value
    }