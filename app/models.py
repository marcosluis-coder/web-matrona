from . import db
from flask_login import UserMixin

class Usuari(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    contrasenya = db.Column(db.String(200))
    rol = db.Column(db.String(20), default="pacient")

    citas = db.relationship("Cita", backref="usuari")

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    estat = db.Column(db.String(20), default="pendent")
    usuari_id = db.Column(db.Integer, db.ForeignKey("usuari.id"))

