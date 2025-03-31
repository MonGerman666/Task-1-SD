from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

# Llista per emmagatzemar els textos filtrats
FILTERED_TEXTS = []

# Llista d'insults coneguts a filtrar (pots afegir-ne més si cal)
KNOWN_INSULTS = ["insult1", "insult2"]

class RequestHandler(SimpleXMLRPCRequestHandler):
    # Accepta peticions a /RPC2 i a la ruta arrel /
    rpc_paths = ('/RPC2', '/')

def filter_text(text: str) -> str:
    """
    Rep un text i substitueix totes les ocurrències dels insults per "CENSORED".
    El text filtrat s'afegeix a la llista FILTERED_TEXTS.
    Retorna el text filtrat.
    """
    filtered = text
    for insult in KNOWN_INSULTS:
        filtered = filtered.replace(insult, "CENSORED")
    FILTERED_TEXTS.append(filtered)
    return filtered

def get_filtered_texts() -> list:
    """
    Retorna la llista de textos filtrats.
    """
    return FILTERED_TEXTS

def main():
    # Arrenca el servidor XMLRPC a localhost, port 8001
    server = SimpleXMLRPCServer(("localhost", 8001),
                                requestHandler=RequestHandler,
                                allow_none=True)
    server.register_function(filter_text, "filter_text")
    server.register_function(get_filtered_texts, "get_filtered_texts")
    
    print("XMLRPC InsultFilter Service en execució al port 8001...")
    server.serve_forever()

if __name__ == "__main__":
    main()
