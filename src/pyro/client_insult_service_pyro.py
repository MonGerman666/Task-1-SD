import Pyro4, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        ns = Pyro4.locateNS()
        uri = ns.lookup("insult.service")
    except Exception as e:
        logging.error("No s'ha pogut trobar el Name Server: %s", e)
        return
    service = Pyro4.Proxy(uri)
    
    # Prova d'afegir insults
    result1 = service.add_insult("insult1")
    result2 = service.add_insult("insult2")
    result3 = service.add_insult("insult1")  # Aquest ja existeix
    logging.info("Resultats d'afegir insults: %s, %s, %s", result1, result2, result3)
    
    insults = service.get_insults()
    logging.info("Llista d'insults: %s", insults)

if __name__ == "__main__":
    main()
