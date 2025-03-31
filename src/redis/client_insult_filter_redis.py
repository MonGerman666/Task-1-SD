import redis
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

r = redis.Redis(host='localhost', port=6379, db=0)
FILTERED_LIST_KEY = 'filtered_texts'
KNOWN_INSULTS = ["insult1", "insult2"]

def filter_text(text):
    for insult in KNOWN_INSULTS:
        text = text.replace(insult, "CENSORED")
    r.rpush(FILTERED_LIST_KEY, text)
    return text

def get_filtered_texts():
    texts = r.lrange(FILTERED_LIST_KEY, 0, -1)
    return [t.decode('utf-8') for t in texts]

def main():
    text1 = "Aquest text conté insult1 i més coses."
    text2 = "Aquest text està net."
    text3 = "Aquest text té insult2 i insult1."
    res1 = filter_text(text1)
    res2 = filter_text(text2)
    res3 = filter_text(text3)
    print("Textos filtrats:", res1, res2, res3)
    texts = get_filtered_texts()
    print("Tots els textos filtrats:", texts)

if __name__ == '__main__':
    main()
