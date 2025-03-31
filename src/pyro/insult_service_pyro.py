import Pyro4, threading, time, random, logging

# Configuració bàsica del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@Pyro4.expose
class InsultService(object):
    def __init__(self):
        self.insults = set()
    
    def add_insult(self, insult):
        """Afegeix un insult si no hi és. Retorna True si s'ha afegit, False si ja existeix."""
        if insult not in self.insults:
            self.insults.add(insult)
            logging.info("S'ha afegit l'insult: %s", insult)
            return True
        else:
            logging.info("L'insult ja existeix: %s", insult)
            return False
    
    def get_insults(self):
        """Retorna la llista d'insults."""
        return list(self.insults)

def start_broadcaster(service):
    """Broadcaster que cada 5 segons tria aleatòriament un insult i el mostra per logging."""
    while True:
        try:
            if service.insults:
                insult = random.choice(list(service.insults))
                logging.info("[BROADCASTER] Difonent insult: %s", insult)
            time.sleep(5)
        except Exception as e:
            logging.error("Error en el broadcaster: %s", e)
            time.sleep(5)

def main():
    service = InsultService()
    # Llança el broadcaster en un fil independent
    broadcaster_thread = threading.Thread(target=start_broadcaster, args=(service,), daemon=True)
    broadcaster_thread.start()
    
    # Crea el Pyro daemon
    daemon = Pyro4.Daemon(host="localhost")
    ns = None
    try:
        ns = Pyro4.locateNS()
    except Exception as e:
        logging.error("Name server no trobat: %s", e)
    
    uri = daemon.register(service)
    if ns:
        ns.register("insult.service", uri)
    logging.info("Pyro InsultService està llest. URI: %s", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
