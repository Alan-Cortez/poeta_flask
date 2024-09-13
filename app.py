from flask import Flask

from flask import render_template
from flask import request

import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/evento", methods=["GET"])
def evento():
    pusher_client = pusher.Pusher(
        app_id='1767934',
        key='ffa9ea426828188c22c1',
        secret='628348e447718a9eec1f',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger("conexion", "evento", request.args)
