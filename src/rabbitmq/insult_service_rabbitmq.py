import pika
import threading
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mantenim els insults en memòria (aquesta és una implementació simple)
INSULTS = set()

def add_insult(insult):
    if insult not in INSULTS:
        INSULTS.add(insult)
        logging.info("S'ha afegit l'insult: %s", insult)
        return True
    else:
        logging.info("L'insult ja existeix: %s", insult)
        return False

def get_insults():
    return list(INSULTS)

class InsultServiceRPC:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpc_queue')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)

    def on_request(self, ch, method, props, body):
        message = body.decode('utf-8')
        logging.info("Rebut request: %s", message)
        if message.startswith("add_insult:"):
            insult = message.split(":", 1)[1]
            response = str(add_insult(insult))
        elif message == "get_insults":
            response = ",".join(get_insults())
        else:
            response = "Unknown command"
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id = props.correlation_id),
            body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        logging.info("RabbitMQ InsultService RPC Server esperant peticions RPC...")
        self.channel.start_consuming()

def broadcaster():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='broadcast', exchange_type='fanout')
    while True:
        if INSULTS:
            insult = random.choice(list(INSULTS))
            channel.basic_publish(exchange='broadcast', routing_key='', body=insult)
            logging.info("[BROADCASTER] Difonent insult: %s", insult)
        time.sleep(5)

def main():
    # Llança el broadcaster en un fil separat
    t = threading.Thread(target=broadcaster, daemon=True)
    t.start()
    rpc = InsultServiceRPC()
    rpc.start()

if __name__ == '__main__':
    main()
