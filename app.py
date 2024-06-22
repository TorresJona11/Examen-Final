from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin1@localhost:3306/lista'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basedatos = SQLAlchemy(app)
ma = Marshmallow(app)

class Tarea(basedatos.Model):
    id = basedatos.Column(basedatos.Integer, primary_key=True)
    descripcion = basedatos.Column(basedatos.String(255), nullable=False)
    fecha_vencimiento = basedatos.Column(basedatos.Date, nullable=False)

    def __init__(self, descripcion, fecha_vencimiento):
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento

basedatos.create_all()

class TareaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        sqla_session = basedatos.session

tarea_schema = TareaSchema()
tareas_schema = TareaSchema(many=True)
