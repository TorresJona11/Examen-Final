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

@app.route('/tareas', methods=['GET'])
def obtener_todas_las_tareas():
    try:
        tareas = Tarea.query.all()
        resultado = tareas_schema.dump(tareas)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al obtener los datos', 'error': str(e)}), 500

@app.route('/tareas/<int:id>', methods=['GET'])
def obtener_tarea_id(id):
    try:
        tarea = Tarea.query.get(id)
        if not tarea:
            return jsonify({'mensaje': 'Tarea no encontrada'}), 404
        return tarea_schema.jsonify(tarea), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al obtener la tarea', 'error': str(e)}), 500

@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    try:
        descripcion = request.json['descripcion']
        fecha_vencimiento_str = request.json['fecha_vencimiento']
        
        fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%d-%m-%Y').date()
        
        nueva_tarea = Tarea(descripcion=descripcion, fecha_vencimiento=fecha_vencimiento)
        basedatos.session.add(nueva_tarea)
        basedatos.session.commit()
        return tarea_schema.jsonify(nueva_tarea), 201
    except ValueError:
        basedatos.session.rollback()
        return jsonify({'mensaje': 'Formato de fecha incorrecto. Debe ser DD-MM-YYYY.'}), 400
    except Exception as e:
        basedatos.session.rollback()
        return jsonify({'mensaje': 'Error al agregar la tarea', 'error': str(e)}), 500
