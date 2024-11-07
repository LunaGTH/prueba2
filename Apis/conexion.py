from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(
        host='localhost', 
        user='root',     
        password='',       
        db='alumnos'       
    )

# Obtener todos los alumnos (GET)
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM users')
    alumnos = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(alumnos)

# Obtener un alumno por ID (GET)
@app.route('/alumnos/<int:id_alum>', methods=['GET'])
def get_alumno(id_alum):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM users WHERE ID = %s', (id_alum,))
    alumno = cursor.fetchone()
    
    cursor.close()
    connection.close()

    if alumno:
        return jsonify(alumno)
    else:
        return jsonify({"Error": "No se encontró el alumno"}), 404

# Insertar un nuevo alumno (POST)
@app.route('/alumnos', methods=['POST'])
def add_alumno():
    new_alumno = request.json
    name = new_alumno['name']
    email = new_alumno['email']
    password = new_alumno['password']

    connection = get_db_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, password))
    connection.commit()
    
    new_alumno['id'] = cursor.lastrowid  # Obtener el ID del nuevo registro
    
    cursor.close()
    connection.close()
    
    return jsonify(new_alumno), 201

# Actualizar un alumno (PUT)
@app.route('/alumnos/<int:id_alum>', methods=['PUT'])
def update_alumno(id_alum):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    update_data = request.json
    name = update_data.get('name')
    email = update_data.get('email')
    password = update_data.get('password')
    
    cursor.execute(
        'UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s',
        (name, email, password, id_alum)
    )
    connection.commit()

    cursor.close()
    connection.close()
    
    if cursor.rowcount:
        return jsonify({"message": "Alumno actualizado correctamente"})
    else:
        return jsonify({"Error": "Alumno no encontrado"}), 404

# Eliminar un alumno (DELETE)
@app.route('/alumnos/<int:id_alum>', methods=['DELETE'])
def delete_alumno(id_alum):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('DELETE FROM users WHERE ID = %s', (id_alum,))
    connection.commit()

    cursor.close()
    connection.close()
    
    if cursor.rowcount:
        return jsonify({"message": "Alumno eliminado correctamente"})
    else:
        return jsonify({"Error": "Alumno no encontrado"}), 404
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)