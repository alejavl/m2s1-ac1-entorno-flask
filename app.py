
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from forms import ContactoForm

# Configuración inicial
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///proyecto.db"

# Inicializar extensiones
bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)

# Configurar Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Modelo de usuario
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)


# Cargar usuario para Flask-Login
@login_manager.user_loader
def cargar_usuario(usuario_id):
    return db.session.get(Usuario, int(usuario_id))


# Crear las tablas de la base de datos
with app.app_context():
    db.create_all()


# Página de inicio
@app.route("/")
def index():
    return render_template("index.html")


# Página Acerca de
@app.route("/about")
def about():
    return render_template("about.html", proyecto="Mi primera app Flask")


# Formulario de contacto y registro de usuarios
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    form = ContactoForm()

    if form.validate_on_submit():
        existente = Usuario.query.filter_by(
            correo=form.correo.data
        ).first()

        if existente:
            flash("Ese correo ya está registrado. Prueba con otro.", "warning")
        else:
            nuevo = Usuario(
                nombre=form.nombre.data,
                correo=form.correo.data
            )

            db.session.add(nuevo)
            db.session.commit()

            flash(
                f"¡Registro guardado con éxito, {nuevo.nombre}!",
                "success"
            )

        return redirect(url_for("contacto"))

    return render_template("contacto.html", form=form)


# Página para mostrar los usuarios registrados
@app.route("/usuarios")
def usuarios():
    lista = Usuario.query.order_by(Usuario.id).all()
    return render_template("usuarios.html", usuarios=lista)


# Inicio de sesión con correo
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip()

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario:
            login_user(usuario)
            flash("Has iniciado sesión correctamente.", "success")
            return redirect(url_for("perfil"))

        flash("No existe un usuario con ese correo.", "warning")

    return render_template("login.html")


# Perfil protegido
@app.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html", usuario=current_user)


# Cerrar sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("index"))


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
