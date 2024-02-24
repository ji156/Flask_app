from flask import Blueprint, render_template, redirect, url_for, request
from .modelos import db
from .modelos import Usuario, Noticia, FormRegistro, FormLogin, FormNoticia
from flask_login import login_user, logout_user, current_user
import sqlalchemy


# Crear el blueprint 'news'
news_bp = Blueprint('news', __name__)

# Ruta redirige a /home
@news_bp.route('/')
def index():
    # Si el usuario ya está autenticado, redirige a /home
    if current_user.is_authenticated:
        return redirect(url_for('news.home'))
    # Si no esta autenticado, redirige a /login
    else:
        return redirect(url_for('news.login'))

# Rutas de gestión de usuarios
@news_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.home'))
    
    form = FormLogin()
    if form.validate_on_submit():
        username = form.username.data
        clave = form.clave.data
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.check_pass(clave):
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('news.home'))
    return render_template('login.html', form=form)

# Ruta de registro
@news_bp.route('/registro', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.home'))
    
    form = FormRegistro()
    if form.validate_on_submit():
        username = form.username.data
        clave = form.clave.data
        confirmar_clave = form.confirmar_clave.data
        if Usuario.query.filter_by(username=username).first():
            return render_template('registro.html', form=form, error='El nombre de usuario ya existe.')
        if clave != confirmar_clave:
            return render_template('registro.html', form=form, error='Las contraseñas no coinciden.')
        
        nuevo_usuario = Usuario(username=username, clave=clave)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('news.login'))
    return render_template('registro.html', form=form)

# Ruta de logout
@news_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()  # Cerrar sesión

    return redirect(url_for('news.login'))  # Redirigir al inicio de sesión


# Rutas de noticias
@news_bp.route('/home')
def home():
    noticias = Noticia.query.paginate(page=1, per_page=3)
    return render_template('home.html', noticias=noticias)

# Ruta de noticias
@news_bp.route('/news/<int:pag>')
def news(pag):
    # Obtener las noticias de la página 'pag' y mostrar 3 noticias por página
    noticias = Noticia.query.paginate(page=pag, per_page=3)
    return render_template('noticias.html', noticias=noticias)

# Ruta para crear noticias
@news_bp.route('/crear-noticia', methods=['GET', 'POST'])
def crear_noticia():
    if not current_user.is_authenticated:
        return redirect(url_for('news.login'))
    
    form = FormNoticia()
    if form.validate_on_submit():
        title = form.title.data
        resumen = form.resumen.data
        try:
            nueva_noticia = Noticia(title=title, resumen=resumen)
            db.session.add(nueva_noticia)
            db.session.commit()
            return redirect(url_for('news.news', pag=1))
        # mensaje de error si el título o el resumen superan el límite de caracteres
        except sqlalchemy.exc.DataError as e:
            db.session.rollback()  # Deshacer la transacción
            error_message = "Error: el límite de caracteres para el título o el resumen se ha superado."
            return render_template('crear_noticias.html', form=form, error=error_message)
    return render_template('crear_noticias.html', form=form)

