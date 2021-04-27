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
    get_planet_info = Planet.query.get(id) #REPASAR SQL. Planet.query.get(id) lo que hace es que me trae la info del planeta por id.
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


#---------------------------GET users by ID------------------------->


@app.route('/users', methods=['GET'])
def get_all_users():

    users_array = User.query.all()
    response_users = list(map(lambda user: user.serialize(), users_array))

    return jsonify(response_users),200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites_by_IDuser(user_id):
    print(request.method)#NOTA: El parametro debe llamarse EXACTAMENTE igual que la ruta.
    favorites_person_array = Favorites_person.query.filter_by(id_user=user_id) #DUDA id_user=user_id, origen de los datos? R/id_user de la linea 96 en models.py igualado al parametro de la ruta actual (user_id).
    favorites_planet_array = Favorites_planet.query.filter_by(id_user=user_id) #NOTA: Favorites_person.query.filter_by/planet devuelven array.
    
    response_favorites_person = list(map(lambda fav_person: fav_person.serialize(), favorites_person_array)) #NOTA: Al ser dos arrays de diccionarios los puedo sumar.
    response_favorites_planet = list(map(lambda fav_planet: fav_planet.serialize(), favorites_planet_array)) #NOTA: El operador "+" en arrays los suma, unicamente si son arrays del mismo tipo.
    response_favorites_total = response_favorites_person + response_favorites_planet #NOTA: Se esta concatenando la info que ya tenia con la nueva.

    return jsonify(response_favorites_total),200

#------------------------POST FAVORITES by USER ID----------------------->


@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def create_favorites_by_IDuser(user_id):
    print(request.method)
    modelo_favorites = request.json.get("modelo_favorites", None)#Traigo el valor de la propiedad modelo_favorites que esta en el body del request.
    id_modelo = request.json.get("id_modelo", None)#Extrae la info del id_modelo ya sea planet o character.
    #id_user = request.json.get("id_user", None)#El ID user asignado al planet o person.


    if modelo_favorites == "person" : #DUDA: Logica del codigo...si la info de clase es igual a la de person, almacenelo y creelo?
        storage_fav_person = Favorites_person(id_person=id_modelo, id_user=user_id)# IZQ.Nombre de la propiedad y a la DERECHA, la variable. En favorites_person estoy creando una instancia (objeto) con las propiedades id_person y id_user.
        db.session.add(storage_fav_person) #NOTA: Codigo linea 106 y 107 son para insertar nuevos datos a la base de datos.
        db.session.commit()#db.session es una imagen viviente de lo que hay en la base de datos. Commit hace que los datos esten enel disco duro.

        return  jsonify(storage_fav_person.serialize()),200 #DUDA: Devuelvo la info almacenada? Si. 

    elif modelo_favorites == "planet":
        storage_fav_planet = Favorites_planet(id_planet=id_modelo,id_user=user_id)
        db.session.add(storage_fav_planet) 
        db.session.commit()

        return jsonify(storage_fav_planet.serialize()),200
    return "Bad request:Modelo favorites does not exist",400

#--------------------DELETE FAVORITES by USER ID--------------------->

@app.route('/favorite/<string:modelo>/<int:favorite_id>', methods=['DELETE']) #DUDAS: el get no es como el delete? debo condicionarlo de alguna manera?
def delete_favorites_by_ID(modelo,favorite_id):
    print(modelo)
    if modelo == "person":
        info_person_favorite_id = Favorites_person.query.get(favorite_id)#Get me trae un objeto (instancia de favorites_person)
        if info_person_favorite_id is None:
            return "Not found: Person does not exist",404
        else:
            db.session.delete(info_person_favorite_id)
            db.session.commit()
        return "Person was successfully deleted",204
    elif modelo == "planet":
        info_planet_favorite_id = Favorites_planet.query.get(favorite_id)
        if info_planet_favorite_id is None:
            return "Not found: Planet does not exist",404
        else: 
            db.session.delete(info_planet_favorite_id)
            db.session.commit() 
        return "Planet was successfully deleted",204
    return "Bad request: We cannot handle this model",400 #NOTA: Si no existe el planet o character, sale este mensaje.



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
