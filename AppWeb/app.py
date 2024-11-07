# Realizar las importaciones de Flask
# modulos       Clase(constructor)
from flask import Flask, render_template
#from flask_mysqldb import MYSQL

# Creacion de objeto
app = Flask(__name__)
#Conexion a la base de datos
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='pass'
app.config['MYSQL_DB']='prueba'


#Crear una instancia de la clase

#mysql = MYSQL(app)

# Creacion de las rutas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return "Inicio de sesion"

# Corrección en la condición
if __name__ == '__main__':
    app.run(debug=True)