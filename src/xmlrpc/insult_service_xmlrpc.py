import threading
import time
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

# Conjunt per emmagatzemar els insults (evitem duplicats)
INSULTS = set()

class RequestHandler(SimpleXMLRPCRequestHandler):
    # Permet peticions a /RPC2 i a la ruta arrel /
    rpc_paths = ('/RPC2', '/')

def add_insult(insult: str) -> bool:
    """
    Afegeix un insult si no hi és.
    Retorna True si s'ha afegit, False si ja existeix.
    """
    if insult not in INSULTS:
        INSULTS.add(insult)
        return True
    return False

def get_insults() -> list:
    """
    Retorna la llista d'insults.
    """
    return list(INSULTS)

def start_broadcaster():
    """
    Broadcaster que cada 5 segons imprimeix un insult aleatori si n'hi ha.
    """
    while True:
        if INSULTS:
            import random
            insult_aleatori = random.choice(list(INSULTS))
            print(f"[BROADCASTER] Difonent insult: {insult_aleatori}")
        time.sleep(5)

def main():
    # Arrenca el servidor XMLRPC a localhost, port 8000
    server = SimpleXMLRPCServer(("localhost", 8000),
                                requestHandler=RequestHandler,
                                allow_none=True)
    server.register_function(add_insult, "add_insult")
    server.register_function(get_insults, "get_insults")
    
    # Llança el broadcaster en un fil separat
    broadcaster_thread = threading.Thread(target=start_broadcaster, daemon=True)
    broadcaster_thread.start()
    
    print("Servidor XMLRPC InsultService en execució al port 8000...")
    server.serve_forever()

if __name__ == "__main__":
    main()
