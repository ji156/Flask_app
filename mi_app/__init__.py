from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import time

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_super_secreta')  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'postgresql://user:password@postgres:5432/mydatabase')

# Configurar la base de datos SQLAlchemy
db = SQLAlchemy(app)

# Inicializar Flask-Migrate para las migraciones de la base de datos
migrate = Migrate(app, db)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Función user_loader para cargar un usuario basado en su ID
from .modelos import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Importar las vistas y registrar el blueprint 
from .vistas import news_bp
app.register_blueprint(news_bp)

def wait_for_db():
    max_retries = 10
    retries = 0
    with app.app_context():
        while retries < max_retries:
            try:
                db.engine.connect()
                print("Conexión exitosa a la base de datos.")
                return
            except Exception as e:
                print(f"Error al conectar con la base de datos: {e}")
                retries += 1
                print(f"Reintentando en 5 segundos... Intento {retries}/{max_retries}")
                time.sleep(5)
        print("No se pudo conectar a la base de datos después de varios intentos. Saliendo...")
        exit(1)

wait_for_db()
