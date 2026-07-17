from flask import Flask, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Función para obtener datos limpios de la base de datos
def fetch_genomic_data():
    conn = sqlite3.connect('database/primates_data.db')
    # Usamos dict_factory para que los resultados sean más fáciles de procesar en el frontend
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Consulta SQL limpia: excluimos registros sin nombre científico
    query = """
        SELECT * FROM genomas 
        WHERE scientific_name IS NOT NULL 
        AND scientific_name != 'None' 
        AND scientific_name != ''
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    # Convertimos los resultados a una lista de diccionarios
    return [dict(row) for row in rows]

# Ruta principal: sirve la página web
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# Ruta de la API: el frontend pedirá los datos a esta dirección
@app.route('/api/genomas')
def get_genomas():
    data = fetch_genomic_data()
    return jsonify(data)

if __name__ == '__main__':
    # Asegúrate de crear la carpeta 'database' y poner tu archivo .db ahí
    app.run(debug=True, port=5000)
