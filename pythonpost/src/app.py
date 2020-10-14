from flask import Flask, jsonify

from conexion import tareas

app = Flask(__name__)


@app.route('/')
def inicio():
    return jsonify({'mensaje': 'Bienvenido al API'})

app.register_blueprint(tareas)

if __name__ == '__main__':
    app.run(debug=True)