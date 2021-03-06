from db.base import TimedDAO

from models import Position, Mac, Location, Time


class PositionDAO(TimedDAO):
    def entity(self):
        return "position"

    def from_db_object(self, db_object):
        return Position(
            mac=Mac(db_object['mac']),
            location=Location(
                x=db_object['location']['x'],
                y=db_object['location']['y'],
                z=db_object['location']['z']
            ),
            created_at=Time(int(db_object['created_at'])),
            _id=db_object['_id']
        )

    def to_db_object(self, position):
        return {
            'mac': position.mac.mac,
            'location': {
                'x': position.location.x,
                'y': position.location.y,
                'z': position.location.z
            },
            'created_at': position.created_at.millis,
            '_id': position._id
        }

    def count_in_rectangle(self, top_left, size):
        x, y = top_left
        return self.count({"location.x": {"$gte": x, "$lte": x+size},
                           "location.y": {"$gte": y, "$lte": y+size}})
