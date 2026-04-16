import requests
import time

def simulacion_mesero():
    url_base = "http://localhost:5000"
    
    # 1. Enviar el pedido
    payload = {"platillo": "Pizza Especial ESCOM", "mesero": "Oziel"}
    print("[MESERO] Enviando comanda vía Web Service...")
    
    r_post = requests.post(f"{url_base}/pedido", json=payload)
    id_pedido = r_post.json()['id_pedido']
    print(f"[MENSAJE] Tu ID de seguimiento es: {id_pedido}\n")

    # 2. Consultar el estatus periódicamente (Polling)
    while True:
        r_get = requests.get(f"{url_base}/estatus/{id_pedido}")
        status = r_get.json()['estatus']
        
        print(f"[CONSULTA] Estatus del pedido {id_pedido}: {status}")
        
        if status == "Listo":
            print("\n[MESERO] ¡El pedido está listo!.")
            break
        
        time.sleep(3) # Esperar antes de volver a preguntar

if __name__ == "__main__":
    simulacion_mesero()