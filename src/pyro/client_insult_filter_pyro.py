import Pyro4, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        ns = Pyro4.locateNS()
        uri = ns.lookup("insult.filter")
    except Exception as e:
        logging.error("No s'ha pogut trobar el Name Server: %s", e)
        return
    service = Pyro4.Proxy(uri)
    
    texts = [
        "Aquest text conté insult1 i altres coses.",
        "Aquest text està net sense cap insult.",
        "Aquí apareixen insult2 i insult1 en el mateix text."
    ]
    for text in texts:
        filtered = service.filter_text(text)
        logging.info("Original: '%s' -> Filtrat: '%s'", text, filtered)
    
    all_filtered = service.get_filtered_texts()
    logging.info("Tots els textos filtrats: %s", all_filtered)

if __name__ == "__main__":
    main()
