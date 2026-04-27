from flask import Flask, request, jsonify, send_from_directory
import threading
import time
import uuid
import os

app = Flask(__name__, static_folder='public')

pedidos_status = {}
estufas_semaforo = threading.Semaphore(3)

# --- Rutas para servir la PWA ---
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('public', path)

# --- Endpoints de la API (Igual que Práctica 6) ---
@app.route('/pedido', methods=['POST'])
def recibir_pedido():
    datos = request.json
    id_pedido = str(uuid.uuid4())[:8]
    platillo = datos.get('platillo')
    
    def proceso_cocina():
        pedidos_status[id_pedido] = "En espera"
        with estufas_semaforo:
            pedidos_status[id_pedido] = "Cocinando"
            time.sleep(10)
            pedidos_status[id_pedido] = "Listo"

    threading.Thread(target=proceso_cocina).start()
    return jsonify({"id_pedido": id_pedido}), 202

@app.route('/estatus/<id_pedido>', methods=['GET'])
def consultar_estatus(id_pedido):
    return jsonify({"estatus": pedidos_status.get(id_pedido, "No encontrado")})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0') # host='0.0.0.0' para verlo desde el celular