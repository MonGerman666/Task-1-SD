import redis
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clau per emmagatzemar els textos filtrats (utilitzem una llista Redis)
FILTERED_LIST_KEY = 'filtered_texts'
KNOWN_INSULTS = ["insult1", "insult2"]

r = redis.Redis(host='localhost', port=6379, db=0)

def filter_text(text):
    filtered = text
    for insult in KNOWN_INSULTS:
        filtered = filtered.replace(insult, "CENSORED")
    r.rpush(FILTERED_LIST_KEY, filtered)
    logging.info("Text filtrat: %s", filtered)
    return filtered

def get_filtered_texts():
    texts = r.lrange(FILTERED_LIST_KEY, 0, -1)
    return [t.decode('utf-8') for t in texts]

def main():
    logging.info("Redis InsultFilter Service en execució. Esperant comandes...")
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
