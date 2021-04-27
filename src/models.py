from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False) #Por que psw=False?
    favorites_person = db.relationship("Favorites_person", backref=db.backref("User", cascade="all,delete"))
    favorites_planet = db.relationship("Favorites_planet", backref=db.backref("User", cascade="all,delete"))
    #children_favorites_planet = db.relationship('favorites_planet')
    #is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model): #Las clases deben ir con ENTIDADES.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable = False)
    population = db.Column(db.Integer)
    gravity = db.Column(db.String(40))
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    created =db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    url = db.Column(db.String(100))
    
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "created": self.created,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "url": self.url,

            # do not serialize the password, its a security breach
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable = False)
    birth_year = db.Column(db.Date, nullable = False)
    created = db.Column(db.String(50))
    homeworld = db.Column(db.String(50))
    eye_color = db.Column(db.String(10))
    gender = db.Column(db.String(15))
    hair_color = db.Column(db.String(20))
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(20))
    url = db.Column(db.String(100))
    #children_favorites = db.relationship("favorites_person")

    def __repr__(self):
        return '<Person %r>' % self.name


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "created": self.created,
            "homeworld": self.homeworld,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "skin_color": self.skin_color,
            "url": self.url
            # do not serialize the password, its a security breach
        }

class Favorites_person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_person = db.Column(db.Integer,db.ForeignKey('person.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id')) 
    person = db.relationship("Person", backref=db.backref("Favorites_person", cascade="all,delete")) 

    def __repr__(self):
        return '<Favorites_Person %r>' % self.name

    def serialize(self):
        return {
            "id": self.id, #DUDA:Que otra informacion podria retornarse?
            "id_person": self.id_person,
            "id_user": self.id_user,
            "content": self.person.serialize()#Esto es para llamar el metodo serialize del modelo person. P.ej: Marte o Luke Skywalker.Aqui se va a almacenar la info de serialize.
        }   

class Favorites_planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_planet = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship("Planet", backref=db.backref("Favorites_planet", cascade="all,delete")) 
    #lazy='subquery'

    def __repr__(self):
        return '<Favorites_Planet %r>' % self.name
   
    def serialize(self):
        return {
            "id": self.id,
           "id_user": self.id_user,
           "id_planet" : self.id_planet,
           "content": self.planet.serialize()

        }



