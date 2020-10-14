from flask import Blueprint, request, jsonify

from conexion import db, ma, Task, task_Squema, tasks_Squema

tareas = Blueprint('task', __name__)


@tareas.route('/task', methods=['POST'])
def crearTask():

    title = request.json['title']
    descripcion = request.json['descripcion']

    newTask = Task(title, descripcion)
    db.session.add(newTask)
    db.session.commit()

    return task_Squema.jsonify(newTask)

@tareas.route('/task')
def obtenerTasks():
    tasks = Task.query.all()
    resultado = tasks_Squema.dump(tasks)
    return jsonify(resultado)

@tareas.route('/task/<id>')
def obtenerTaskPorId(id):
    task = Task.query.get(id)
    return task_Squema.jsonify(task)

@tareas.route('/task/<id>', methods=['PUT'])
def editarTask(id):
    task = Task.query.get(id)
    
    title = request.json['title']
    descripcion = request.json['descripcion']

    task.title = title
    task.descripcion = descripcion

    db.session.commit()

    return task_Squema.jsonify(task)

@tareas.route('/task/<id>', methods=['DELETE'])
def eliminarTarea(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_Squema.jsonify(task) 

