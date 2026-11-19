import os
import sqlite3
from cs50 import SQL
from flask import Flask, jsonify, request, render_template, redirect, session
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash


app =  Flask(__name__)

app.config["SECRET_KEY"] = "clave_secreta_super_segura_gym"

if not os.path.exists("gym.db"):
    with sqlite3.connect("gym.db") as conn:
        with open("schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())

db = SQL("sqlite:///gym.db")

# -----------------------------------
# RUTAS DE AUTENTICACIÓN
# -----------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validaciones básicas
        if not usuario or not password or not confirmation:
            return "Faltan campos por llenar", 400
        if password != confirmation:
            return "Las contraseñas no coinciden", 400
        
        # Encriptamos la contraseña por seguridad
        hash_password = generate_password_hash(password)

        try:
            # Guardamos el usuario en la BD (si ya existe, saltará un error por el UNIQUE)
            id_nuevo = db.execute(
                "INSERT INTO usuarios (usuario, hash) VALUES (?, ?)", usuario, hash_password
            )
        except:
            return "El nombre de usuario ya está registrado", 400
        
        # Iniciamos sesión automáticamente al registrarse
        session["user_id"] = id_nuevo
        return redirect("/")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Limpiamos cualquier sesión previa
    session.clear()

    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        if not usuario or not password:
            return "Faltan campos por llenar", 400
        
        # Buscamos al usuario en la BD

        filas = db.execute("SELECT * FROM usuarios WHERE usuario = ?", usuario)

        # Verificamos si existe el usuario y si la contraseña coincide con el hash
        if len(filas) != 1 or not check_password_hash(filas[0]["hash"], password):
            return "Usuario o contraseña incorrectos", 400
        
        # Guardamos el ID del usuario en la sesión del navegador
        session["user_id"] = filas[0]["id"]
        return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -----------------------------------
# RUTAS DEL TRACKER (PROTEGIDAS POR SESIÓN)
# -----------------------------------

@app.route("/")
def index():
    # Si no ha iniciado sesión, lo mandamos al login
    if "user_id" not in session:
        return redirect("/login")
    
    user_id = session["user_id"]

    # Traemos solo los entrenamientos DEL USUARIO ACTUAL

    registros = db.execute(
        "SELECT * FROM entrenamientos WHERE usuario_id = ? ORDER BY fecha DESC, id DESC", user_id
    )

    records = db.execute("""
        SELECT ejercicio, MAX(peso) as max_peso
        FROM entrenamientos
        WHERE usuario_id = ?
        GROUP by ejercicio
    """, user_id)

    volumen_total = db.execute("SELECT COALESCE(SUM(peso * repeticiones), 0) AS total FROM entrenamientos WHERE usuario_id = ?", user_id)[0]["total"]

    return render_template(
        "index.html",
        entrenamientos=registros,
        records=records,
        volumen_total=volumen_total
    )


@app.route("/registrar", methods=["POST"])
def registrar():
    if "user_id" not in session:
        return redirect("/login")
    
    ejercicio = request.form.get("ejercicio")
    peso = request.form.get("peso")
    repeticiones = request.form.get("repeticiones")
    fecha_input = request.form.get("fecha")

    if not ejercicio or not peso or not repeticiones:
        return "Faltan campos por llenar", 400
    
    if not fecha_input:
        fecha_input = date.today().isoformat()

    # Insertamos asociando la serie al user_id en sesion
    db.execute("INSERT INTO entrenamientos (usuario_id, ejercicio, peso, repeticiones, fecha) VALUES (?, ?, ?, ?, ?)", 
        session["user_id"],
        ejercicio,
        peso,
        repeticiones,
        fecha_input)
    
    return redirect("/")

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if "user_id" not in session:
        return redirect("/login")
    
    registro_id = request.form.get("id")

    if not registro_id:
        return "Falta el ID del registro", 400
    
    # Aseguramos que solo pueda borrar sus propios registros
    db.execute("DELETE FROM entrenamientos WHERE id = ? and usuario_id = ?",
    registro_id,
    session["user_id"])

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)