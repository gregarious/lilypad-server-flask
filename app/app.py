from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    resp = 'Secret key: %s<br/>\nShhhh!' % app.config['SECRET_KEY']
    return resp

if __name__ == '__main__':
    app.config.from_object('config.default')
    app.config.from_envvar('LILYPAD_DEPLOY_SETTINGS')
    app.run()
