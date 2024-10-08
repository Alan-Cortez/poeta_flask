from flask import Flask, render_template, request, jsonify
import mysql.connector
import pusher

# Configuración de conexión MySQL
con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

# Configuración de Pusher
pusher_client = pusher.Pusher(
  app_id='1767934',
  key='ffa9ea426828188c22c1',
  secret='628348e447718a9eec1f',
  cluster='us2',
  ssl=True
)

# Ruta para renderizar la página principal
@app.route("/")
def index():
    return render_template("usuarios.html")

# Ruta para renderizar la página de usuarios
@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html")

# Crear usuario
@app.route("/usuarios/guardar", methods=["POST"])
def usuarios_guardar():
    usuario = request.form["txtUsuarioFA"]
    contrasena = request.form["txtContrasenaFA"]

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    # Insertar nuevo usuario
    sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
    cursor.execute(sql, (usuario, contrasena))
    con.commit()

    # Disparar evento Pusher para notificar la inserción
    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {"usuario": usuario})

    return jsonify({"status": "success", "message": "Usuario creado exitosamente"})

# Leer todos los usuarios
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuario DESC")
    registros = cursor.fetchall()

    return jsonify(registros)

# Actualizar usuario
@app.route("/usuarios/actualizar", methods=["POST"])
def usuarios_actualizar():
    id_usuario = request.form["id_usuario"]
    usuario = request.form["txtUsuarioFA"]
    contrasena = request.form["txtContrasenaFA"]

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    # Actualizar usuario
    sql = "UPDATE tst0_usuarios SET Nombre_Usuario=%s, Contrasena=%s WHERE Id_Usuario=%s"
    cursor.execute(sql, (usuario, contrasena, id_usuario))
    con.commit()

    # Disparar evento Pusher para notificar la actualización
    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {"usuario": usuario})

    return jsonify({"status": "success", "message": "Usuario actualizado exitosamente"})

# Eliminar usuario
@app.route("/usuarios/eliminar", methods=["POST"])
def usuarios_eliminar():
    id_usuario = request.form["id_usuario"]

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    # Eliminar usuario
    sql = "DELETE FROM tst0_usuarios WHERE Id_Usuario=%s"
    cursor.execute(sql, (id_usuario,))
    con.commit()

    # Disparar evento Pusher para notificar la eliminación
    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {"id_usuario": id_usuario})

    return jsonify({"status": "success", "message": "Usuario eliminado exitosamente"})

if __name__ == "__main__":
    app.run(debug=True)
