import sqlite3

conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

cursor.execute(
    "UPDATE usuarios SET admin = 1 WHERE nome = ?",
    ("Daniel",)
)

conn.commit()
conn.close()

print("Usuário promovido a admin!")