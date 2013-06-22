from flask.ext.restful import Api
from app import app

from student import StudentCollection, StudentResource

@app.route('/')
def index():
    return 'Welcome home!'

api = Api(app)

api.add_resource(StudentCollection, '/students/')
api.add_resource(StudentResource, '/students/<string:_id>')
