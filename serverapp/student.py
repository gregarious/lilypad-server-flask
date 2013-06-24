from flask.ext.restful import Resource, fields, marshal_with, reqparse, abort

from mongokit import Document
from bson.objectid import ObjectId

from datetime import datetime, date

from serverapp import db, connection

class Student(Document):
    __collection__ = 'students'
    structure = {
        'first_name': unicode,
        'last_name': unicode,
        'email': unicode,

        # note that embedded doc fields for doc arrays aren't
        # actually mandated by MongoKit -- all it sees is the []
        'goals': [{
            'label': unicode,
            'description': unicode,
            'started_at': datetime,
            'ended_at': datetime
        }],

        'activity_ratings': [{
            'point_value': int,
            'points_available': int,
            'label': unicode,
            'recorded_at': datetime,
            'category': {
                'label': unicode
            }
        }],

        'bonuses': [{
            'recorded_at': datetime,
            'point_value': int,
            'label': unicode
        }]
    }

    required_fields = ['first_name', 'last_name']

    use_dot_notation = True

    def __repr__(self):
        return '<Student: %s %s>' % (self.first_name, self.last_name)

connection.register([Student])

class StudentResource(Resource):
    def get(self, _id):
        student = db.Student.find_one({'_id': ObjectId(_id)})
        if student:
            return student
        else:
            abort(404)

    def delete(self, _id):
        if db.Student.find_one({'_id': ObjectId(_id)}):
            db.Student.collection.remove({'_id': ObjectId(_id)})
        else:
            abort(404)

    # def put(self, _id):
    #     if ok:
    #       return 200
    #     else:
    #       abort(404)

class StudentCollection(Resource):
    def get(self):
        return list(db.Student.find())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=unicode)
        parser.add_argument('last_name', type=unicode)
        args = parser.parse_args()

        student = db.Student()
        student['first_name'] = args['first_name']
        student['last_name'] = args['last_name']
        student.save()
        return student, 201
