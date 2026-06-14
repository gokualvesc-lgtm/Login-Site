import sqlite3, os
from dotenv import load_dotenv
from flask import Flask, request, render_template, session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastrar/submited", methods=["POST"])
def cadastrar_submited():
    nome = request.form["nome"].strip()
    senha = request.form["senha"].strip()
    if not nome or not senha:
        return render_template("cadastro.html", message="Nome e senha são obrigatórios!")
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))

    conn.commit()
    conn.close()

    return render_template("login.html", message="Cadastro realizado com sucesso! Faça login.")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/submited", methods=["POST"])
def login_submited():
    nome = request.form["nome"].strip()
    senha = request.form["senha"].strip()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    result = cursor.fetchone()
    conn.close()

    if result:
        session["user_id"] = result[0]
        session["nome"] = result[1]
        return render_template("home.html", nome=session["nome"], id=session["user_id"])

    return render_template("login.html", message="Nome ou senha incorretos!")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/submited", methods=["POST"])
def admin_submited():
    nome = request.form["nome"].strip()
    senha = request.form["senha"].strip()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ? AND admin = 1", (nome, senha))
    result = cursor.fetchone()
    conn.close()

    if result:
        session["user_id"] = result[0]
        session["nome"] = result[1]
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return render_template("admin_home.html", nome=session["nome"], id=session["user_id"], usuarios=usuarios)

    return render_template("admin.html", message="Nome ou senha incorretos!")

app.run(debug=True)