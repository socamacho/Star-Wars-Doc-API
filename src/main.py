"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Person
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#----------ENDPOINTS------------------------------------------>


@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets_array = Planet.query.all()
    response_planets = list(map(lambda planet: planet.serialize(), planets_array))

    return jsonify(response_planets),200



@app.route('/persons', methods=['GET'])
def get_all_persons():

    persons_array = Person.query.all()
    response_persons = list(map(lambda person: person.serialize(), persons_array))

    return jsonify(response_persons),200


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_id(id):
    get_planet_info = Planet.query.get(id) 
    if get_planet_info is None:
        raise APIException ("Planet not found", status_code=404)
    response_planet_id = get_planet_info.serialize() #Pq tiene la instancia de planet, por eso puedo acceder a los metodos del modelo Planet.
    return jsonify(response_planet_id),200

@app.route('/persons/<int:id>', methods=['GET'])
def get_person_id(id):
    get_person_info = Person.query.get(id)
    if get_person_info is None:
        raise APIException ("Character not found", status_code=404)
    response_person_id = get_person_info.serialize()
    return jsonify(response_person_id),200





"""@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200"""

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
