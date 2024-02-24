# importamos app desde mi_app
from mi_app import app

# Esto es para que se ejecute el servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
