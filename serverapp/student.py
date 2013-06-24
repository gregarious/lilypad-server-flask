from flask.ext.restful import Resource, fields, marshal_with, reqparse, abort

from mongokit import Document
from bson.objectid import ObjectId

from datetime import datetime, date
from copy import copy

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

        'activities': [{
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


class GoalCollection(Resource):
    resource_fields = {
        'label': fields.String,
        'description': fields.String,
        'started_at': fields.DateTime,
        'ended_at': fields.DateTime
    }

    @marshal_with(resource_fields)
    def get(self, student_id):
        student = db.Student.find_one({'_id': ObjectId(student_id)})
        if student:
            return student.goals
        else:
            abort(404)


class ActivityCollection(Resource):
    resource_fields = {
        'point_value': fields.Integer,
        'points_available': fields.Integer,
        'label': fields.String,
        'recorded_at': fields.DateTime,
        'category': fields.Nested({
            'label': fields.String
        })
    }

    @marshal_with(resource_fields)
    def get(self, student_id):
        student = db.Student.find_one({'_id': ObjectId(student_id)})
        if student:
            return student.activities
        else:
            abort(404)


class BonusCollection(Resource):
    resource_fields = {
        'point_value': fields.Integer,
        'label': fields.String,
        'recorded_at': fields.DateTime,
    }

    @marshal_with(resource_fields)
    def get(self, student_id):
        student = db.Student.find_one({'_id': ObjectId(student_id)})
        if student:
            return student.bonuses
        else:
            abort(404)


class StudentResource(Resource):
    resource_fields = {
        '_id': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'goals': fields.List(fields.Nested(
            GoalCollection.resource_fields)),
        'activities': fields.List(fields.Nested(
            ActivityCollection.resource_fields)),
        'bonus': fields.List(fields.Nested(
            BonusCollection.resource_fields))
    }

    @marshal_with(resource_fields)
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
    resource_fields = StudentResource.resource_fields

    @marshal_with(resource_fields)
    def get(self):
        return list(db.Student.find())

    @marshal_with(resource_fields)
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
