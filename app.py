from flask import Flask
from flask import render_template
from flask import request
import pusher
import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
     con.close()
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
     con.close()
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
     con.close()
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/buscar")
def buscar():
  return "Hola";

@app.route("/evento", methods=["GET"])
def evento():
     if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    args = request.args
  
    sql = "INSERT INTO sensor_log (Temperatura, Humedad, Fecha_Hora) VALUES (%s, %s, %s)"
    val = (args["temperatura"], args["humedad"], datetime.datetime.now())
    cursor.execute(sql, val)
    
    con.commit()
    con.close()
    pusher_client = pusher.Pusher(
        app_id='1767934',
        key='ffa9ea426828188c22c1',
        secret='628348e447718a9eec1f',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger("conexion", "evento", request.args)
