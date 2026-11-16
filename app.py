
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from forms import ContactoForm

# Configuración inicial
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///proyecto.db"

# Inicializar extensiones
bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)


# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)


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


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
