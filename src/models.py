from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

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
            "url": self.url,


            # do not serialize the password, its a security breach
        }
