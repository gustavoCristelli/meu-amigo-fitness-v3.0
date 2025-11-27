#models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    peso_atual = db.Column(db.Float)
    altura = db.Column(db.Float)
    sexo = db.Column(db.String(10))
    nivel_atividade = db.Column(db.Integer)

class RegistroDiario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    calorias_consumidas = db.Column(db.Float)
    calorias_gastas = db.Column(db.Float)
