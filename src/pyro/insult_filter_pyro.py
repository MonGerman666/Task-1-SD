import Pyro4, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@Pyro4.expose
class InsultFilter(object):
    def __init__(self):
        self.filtered_texts = []
        self.known_insults = ["insult1", "insult2"]
    
    def filter_text(self, text):
        """
        Rep un text, substitueix els insults per "CENSORED" i emmagatzema el text filtrat.
        Retorna el text filtrat.
        """
        filtered = text
        for insult in self.known_insults:
            filtered = filtered.replace(insult, "CENSORED")
        self.filtered_texts.append(filtered)
        logging.info("Text filtrat: %s", filtered)
        return filtered
    
    def get_filtered_texts(self):
        """Retorna la llista completa de textos filtrats."""
        return self.filtered_texts

def main():
    service = InsultFilter()
    daemon = Pyro4.Daemon(host="localhost")
    ns = None
    try:
        ns = Pyro4.locateNS()
    except Exception as e:
        logging.error("Name server no trobat: %s", e)
    uri = daemon.register(service)
    if ns:
        ns.register("insult.filter", uri)
    logging.info("Pyro InsultFilter està llest. URI: %s", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
