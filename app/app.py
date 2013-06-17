from flask import Flask
from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with, Api

from mongokit import Connection, Document
from bson.objectid import ObjectId

app = Flask(__name__)

app.config.from_object('config.default')
app.config.from_envvar('LILYPAD_DEPLOY_SETTINGS')

connection = Connection(
    app.config.get('MONGODB_HOST', 'localhost'),
    app.config.get('MONDODB_PORT', 27017))

db = connection[app.config.get('MONGODB_DATABASE')]

parser = reqparse.RequestParser()

class Student(Document):
    __collection__ = 'students'
    structure = {
        'first_name': unicode,
        'last_name': unicode
    }
    required_fields = ['first_name', 'last_name']
    use_dot_notation = True

    def __repr__(self):
        return '<Student: %r %r>' % (self.first_name, self.last_name)

connection.register([Student])

student_resource_fields = {
    '_id':  fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
}

class StudentResource(Resource):
    @marshal_with(student_resource_fields)
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
    @marshal_with(student_resource_fields)
    def get(self):
        return list(db.Student.find())

    @marshal_with(student_resource_fields)
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

@app.route('/')
def index():
    return 'Welcome home!'

api = Api(app)

api.add_resource(StudentCollection, '/students/')
api.add_resource(StudentResource, '/students/<string:_id>')

if __name__ == '__main__':
    app.run()
