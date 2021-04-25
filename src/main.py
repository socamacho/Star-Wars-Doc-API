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
from models import db, User, Planet, Person, Favorites_person, Favorites_planet
from sqlalchemy.orm import relationship
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
#----------ENDPOINTS STAR WARS------------------------------------------>


#-----------GET PLANETS and PEOPLE-------------------------------------->

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


#---------------------------GET, POST and DELETE users by ID------------------------->


@app.route('/users', methods=['GET'])
def get_all_users():

    users_array = User.query.all()
    response_users = list(map(lambda user: user.serialize(), users_array))

    return jsonify(response_users),200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites_by_IDuser(user_id):#NOTA: El parametro debe llamarse EXACTAMENTE igual que la ruta.
    favorites_person = Favorites_person.query.filter_by(id_user=user_id)
    favorites_planet = Favorites_planet.query.filter_by(id_user=user_id)
    
    response_favorites_person = list(map(lambda fav_person: fav_person.serialize(), favorites_person)) #NOTA: Al ser dos arrays de diccionarios los puedo sumar.
    response_favorites_planet = list(map(lambda fav_planet: fav_planet.serialize(), favorites_planet)) #NOTA: El operador "+" en arrays los suma, unicamente si son arrays del mismo tipo.
    response_favorites_total = response_favorites_person + response_favorites_planet

    return jsonify(response_favorites_total),200

@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def create_favorites_by_IDuser():
    clase = request.json.get("clase", None)
    id_clase = request.json.get("id_clase", None)
    id_user = request.json.get("id_user", None)


    if clase == "person" :
        storage_fav_person = Favorites_person(id_person=id_clase, id_user=id_user)
        db.session.add(storage_fav_person) #NOTA: Codigo linea 106 y 107 son para insertar neuvos datos a la base de datos.
        db.session.commit()

        return  jsonify(storage_fav_person.serialize()),200

    elif clase == "planet":
        storage_fav_planet = Favorites_planet(id_planet=id_clase,id_user=id_user)
        db.session.add(storage_fav_planet) 
        db.session.commit()

        return jsonify(storage_fav_planet.serialize()),200
    return "Bad request:Class does not exist",400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
