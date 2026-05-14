from flask import Flask, request, jsonify, send_from_directory
import requests
import os

# Configuramos la carpeta 'public' para los archivos de la PWA
app = Flask(__name__, static_folder='public')

PIZZAS_URL = "http://localhost:5001"
GENERAL_URL = "http://localhost:5002"
mapping_servicios = {}

# --- RUTAS PARA SERVIR LA PWA DESDE EL GATEWAY ---
@app.route('/')
def index():
    # Esto busca el index.html dentro de la carpeta 'public'
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

# --- ENDPOINTS DE ENRUTAMIENTO ---
@app.route('/pedido', methods=['POST'])
def enrutar_pedido():
    datos = request.json
    platillo = datos.get('platillo')
    target_url = PIZZAS_URL if "Pizza" in platillo else GENERAL_URL
    
    try:
        response = requests.post(f"{target_url}/cocinar", json=datos)
        res_data = response.json()
        
        # CORRECCIÓN AQUÍ: Usar 'id_pedido' para coincidir con el microservicio
        id_generado = res_data.get('id_pedido')
        mapping_servicios[id_generado] = target_url
        
        return jsonify(res_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 503

@app.route('/estatus/<id_pedido>', methods=['GET'])
def consultar_estatus(id_pedido):
    target_url = mapping_servicios.get(id_pedido)
    if not target_url:
        return jsonify({"estatus": "No encontrado"}), 404
    
    response = requests.get(f"{target_url}/status/{id_pedido}")
    return response.json()

if __name__ == '__main__':
    # Usar 0.0.0.0 permite que el celular también entre al Gateway
    app.run(port=5000, host='0.0.0.0')