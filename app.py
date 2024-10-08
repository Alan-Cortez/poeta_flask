from flask import Flask, request, jsonify
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Conectar a la base de datos
def conectar_bd():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="mi_base_datos",
        cursorclass=pymysql.cursors.DictCursor
    )

# Ruta para registrar un nuevo usuario
@app.route("/registrar", methods=["POST"])
def registrar_usuario():
    nombre = request.form["nombre"]
    password = request.form["password"]
    hash_password = generate_password_hash(password)  # Hasheando la contraseña

    conexion = conectar_bd()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios (nombre, password) VALUES (%s, %s)", (nombre, hash_password))
        conexion.commit()

    return "Usuario registrado", 201

# Ruta para iniciar sesión
@app.route("/login", methods=["POST"])
def login_usuario():
    nombre = request.form["nombreLogin"]
    password = request.form["passwordLogin"]

    conexion = conectar_bd()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT password FROM usuarios WHERE nombre=%s", (nombre,))
        usuario = cursor.fetchone()

    if usuario and check_password_hash(usuario["password"], password):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

# Ruta para obtener la lista de usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    conexion = conectar_bd()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombre, fecha_registro FROM usuarios")
        usuarios = cursor.fetchall()

    return jsonify(usuarios)

if __name__ == "__main__":
    app.run(debug=True)
