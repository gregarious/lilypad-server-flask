from flask.ext.restful import Api
from serverapp import app

from student import StudentCollection, StudentResource
from student import ActivityCollection, BonusCollection, GoalCollection

@app.route('/')
def index():
    return 'Welcome home!'

api = Api(app)

api.add_resource(StudentCollection, '/students/')
api.add_resource(StudentResource, '/students/<string:_id>')

api.add_resource(ActivityCollection, '/students/<string:student_id>/activities/')
api.add_resource(BonusCollection, '/students/<string:student_id>/bonuses/')
api.add_resource(GoalCollection, '/students/<string:student_id>/goals/')
