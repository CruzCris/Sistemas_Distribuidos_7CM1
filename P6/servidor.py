from flask import Flask, request, jsonify
import threading
import time
import uuid

app = Flask(__name__)

# Diccionario para guardar el estatus de los pedidos
# Estructura: { id_pedido: "En espera" | "Cocinando" | "Listo" }
pedidos_status = {}
estufas_semaforo = threading.Semaphore(3)

def proceso_coccion(id_pedido, platillo):
    """Tarea que corre en segundo plano para no bloquear el servicio web"""
    pedidos_status[id_pedido] = "En espera de estufa"
    
    with estufas_semaforo:
        pedidos_status[id_pedido] = "Cocinando"
        print(f"[API] Cocinando pedido {id_pedido}: {platillo}")
        time.sleep(15)  # Simulamos un tiempo largo para poder consultar el estatus
        pedidos_status[id_pedido] = "Listo"
        print(f"[API] Pedido {id_pedido} terminado.")

@app.route('/pedido', methods=['POST'])
def recibir_pedido():
    datos = request.json
    platillo = datos.get('platillo')
    
    # Generamos un ID único para el pedido
    id_pedido = str(uuid.uuid4())[:8]
    
    # Iniciamos la cocción en un hilo aparte (Asíncrono)
    hilo_cocina = threading.Thread(target=proceso_coccion, args=(id_pedido, platillo))
    hilo_cocina.start()
    
    return jsonify({
        "id_pedido": id_pedido,
        "status": "Recibido",
        "mensaje": "Tu pedido ha sido enviado a la cocina. Consulta su estatus con el ID."
    }), 202  # 202 significa "Accepted" (Aceptado para procesamiento)

@app.route('/estatus/<id_pedido>', methods=['GET'])
def consultar_estatus(id_pedido):
    status = pedidos_status.get(id_pedido, "No encontrado")
    return jsonify({
        "id_pedido": id_pedido,
        "estatus": status
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)