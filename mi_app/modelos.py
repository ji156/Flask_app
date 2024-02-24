from . import db  
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin


# clase Usuario
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    clave_hash = db.Column(db.String(512))  # Aumentar la longitud de la columna

    def __init__(self, username, clave):
        self.username = username
        self.set_clave(clave)

    def set_clave(self, clave):
        self.clave_hash = generate_password_hash(clave)

    def check_pass(self, clave):
        return check_password_hash(self.clave_hash, clave)
    
    def is_active(self):
        return True
    
    def get_id(self):
        return self.id

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    resumen = db.Column(db.String(256))

    def __init__(self, title, resumen):
        self.title = title
        self.resumen = resumen


# clase FormRegistro
class FormRegistro(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    clave = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar_clave = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrar')


# clase FormLogin
class FormLogin(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    clave = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')


# clase FormNoticia
class FormNoticia(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    resumen = StringField('Resumen', validators=[DataRequired()])
    submit = SubmitField('Crear noticia')
