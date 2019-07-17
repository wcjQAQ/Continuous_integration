from flask import Flask
from flask_restful import Resource, Api
from api.tomcat import UpdateTomcat
from api.show import showtag,showproject
from flask_cors import CORS
app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello_world():
    return 'Hello World!'
CORS(app, supports_credentials=True)
api.add_resource(UpdateTomcat, '/api/update/tomcat')
api.add_resource(showtag, '/api/showtag/<project>/<module>')
api.add_resource(showproject, '/api/showmodule/<project>')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
