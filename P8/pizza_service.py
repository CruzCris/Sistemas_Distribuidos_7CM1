from flask import Flask, request, jsonify
import threading
import time
import uuid

app = Flask(__name__)
estufas = threading.Semaphore(2) # Recursos dedicados a pizza
pedidos = {}

@app.route('/cocinar', methods=['POST'])
def cocinar():
    id_p = str(uuid.uuid4())[:8]
    platillo = request.json.get('platillo')
    
    def proceso():
        pedidos[id_p] = "En fila (Pizzería)"
        with estufas:
            pedidos[id_p] = "En el Horno"
            time.sleep(8)
            pedidos[id_p] = "Listo"

    threading.Thread(target=proceso).start()
    return jsonify({"id_pedido": id_p})

@app.route('/status/<id_p>', methods=['GET'])
def status(id_p):
    return jsonify({"estatus": pedidos.get(id_p, "No encontrado")})

if __name__ == '__main__':
    app.run(port=5001)