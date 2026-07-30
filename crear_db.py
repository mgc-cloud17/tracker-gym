from cs50 import SQL

# 1. Nos conectamos usando la herramienta de CS50
db = SQL("sqlite:///gym.db")

# 2. Tabla de Usuarios
db.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NO NULL UNIQUE,
    hash TEXT NO NULL
)
""")

# 3. Tabla de Entrenamientos conectada a Usuarios mediante 'usuario_id'
db.execute("""
CREATE TABLE IF NOT EXISTS entrenamientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    ejercicio TEXT NO NULL,
    peso REAL NOT NULL,
    repeticiones INTEGER NOT NULL,
    fecha DATE NO NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
""")

print("¡Base de datos actualizada con sistema de usuarios!")

