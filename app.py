from flask import Flask,jsonify, make_response, request
from flask_json_schema import JsonSchema, JsonValidationError
from controller import Controller
from flask_cors import CORS
from schema import MOVIE_REQUEST_SCHEMA
controller = Controller()



app = Flask(__name__)
schema = JsonSchema(app)
cors = CORS(app)

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return make_response(jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]}),400)

@app.route('/',methods=['GET'])
def ping():
        return "Ping Recommeder Movie App .."


@app.route('/api/v1/movies/recommeder',methods=['POST'])
@schema.validate(MOVIE_REQUEST_SCHEMA)
def recommerder_movie():
    request_body = request.get_json()
    response = controller.recommender_movies(request_body)
    return jsonify(response)

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Resource Not Found'), 404)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080)