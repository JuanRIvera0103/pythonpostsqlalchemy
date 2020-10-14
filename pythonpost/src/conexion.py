
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


conexion = Flask(__name__)

host = 'localhost'
user = 'postgres'
passw = '123456'
database = 'pythonpost'


conexion.config['SQLALCHEMY_DATABASE_URI'] = "postgres://" + user + ":"  + passw + "@" + host + "/" + database +""
conexion.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(conexion)
ma = Marshmallow(conexion)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    descripcion = db.Column(db.String(30))

    def __init__ (self, title, descripcion):
        self.title = title
        self.descripcion = descripcion

db.create_all()

class TaskSquema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'descripcion')

task_Squema = TaskSquema()
tasks_Squema = TaskSquema(many=True)

@conexion.route('/task', methods=['POST'])
def crearTask():

    title = request.json['title']
    descripcion = request.json['descripcion']

    newTask = Task(title, descripcion)
    db.session.add(newTask)
    db.session.commit()

    return task_Squema.jsonify(newTask)

@conexion.route('/task')
def obtenerTasks():
    tasks = Task.query.all()
    resultado = tasks_Squema.dump(tasks)
    return jsonify(resultado)

@conexion.route('/task/<id>')
def obtenerTaskPorId(id):
    task = Task.query.get(id)
    return task_Squema.jsonify(task)

@conexion.route('/task/<id>', methods=['PUT'])
def editarTask(id):
    task = Task.query.get(id)
    
    title = request.json['title']
    descripcion = request.json['descripcion']

    task.title = title
    task.descripcion = descripcion

    db.session.commit()

    return task_Squema.jsonify(task)

@conexion.route('/task/<id>', methods=['DELETE'])
def eliminarTarea(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_Squema.jsonify(task) 

if __name__ == "__main__":
    conexion.run(debug=True)