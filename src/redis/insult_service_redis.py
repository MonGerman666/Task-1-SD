import redis
import time
import threading
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clau per emmagatzemar els insults en un conjunt Redis
INSULT_SET_KEY = 'insults_set'
# Canal per publicar els missatges del broadcaster
BROADCAST_CHANNEL = 'insults_broadcast'

# Connexió a Redis (ajusta la configuració si cal)
r = redis.Redis(host='localhost', port=6379, db=0)

def add_insult(insult):
    """
    Afegeix un insult al conjunt si no existeix.
    Retorna True si s'ha afegit, False en cas contrari.
    """
    added = r.sadd(INSULT_SET_KEY, insult)
    if added:
        logging.info("S'ha afegit l'insult: %s", insult)
        return True
    else:
        logging.info("L'insult ja existeix: %s", insult)
        return False

def get_insults():
    """
    Retorna una llista amb tots els insults.
    """
    insults = r.smembers(INSULT_SET_KEY)
    return [i.decode('utf-8') for i in insults]

def broadcaster():
    """
    Cada 5 segons selecciona un insult aleatori i el publica al canal BROADCAST_CHANNEL.
    """
    while True:
        insults = get_insults()
        if insults:
            insult = random.choice(insults)
            r.publish(BROADCAST_CHANNEL, insult)
            logging.info("[BROADCASTER] Difonent insult: %s", insult)
        time.sleep(5)

def main():
    # Llança el broadcaster en un fil independent
    t = threading.Thread(target=broadcaster, daemon=True)
    t.start()
    logging.info("Redis InsultService en execució. Esperant comandes...")
    # Manté el procés actiu
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
