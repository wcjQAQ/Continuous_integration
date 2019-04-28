from flask import Flask
from flask_restful import Resource, Api
from api.tomcat import UpdateTomcat
from api.show import showtag
app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

api.add_resource(UpdateTomcat, '/api/update/tomcat')
api.add_resource(showtag, '/api/showtag/<project>/<module>')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
