import redis
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connexió a Redis
r = redis.Redis(host='localhost', port=6379, db=0)
INSULT_SET_KEY = 'insults_set'

def add_insult(insult):
    return bool(r.sadd(INSULT_SET_KEY, insult))

def get_insults():
    insults = r.smembers(INSULT_SET_KEY)
    return [i.decode('utf-8') for i in insults]

def main():
    res1 = add_insult("insult1")
    res2 = add_insult("insult2")
    res3 = add_insult("insult1")  # Ja existeix
    logging.info("Resultats d'afegir insults: %s, %s, %s", res1, res2, res3)
    insults = get_insults()
    logging.info("Llista d'insults: %s", insults)

if __name__ == '__main__':
    main()
