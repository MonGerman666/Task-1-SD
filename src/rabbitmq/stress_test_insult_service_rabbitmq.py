import pika
import uuid
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InsultServiceRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode()

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=self.corr_id),
                                   body=message)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def send_insult(i):
    rpc_client = InsultServiceRpcClient()
    insult = f"insult_{i}"
    result = rpc_client.call(f"add_insult:{insult}")
    return insult, result

def main():
    num_requests = 100
    logging.info("Iniciant test d'estrès amb %d peticions...", num_requests)
    start = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_insult, i) for i in range(num_requests)]
        for future in as_completed(futures):
            insult, result = future.result()
            logging.info("Resultat per %s: %s", insult, result)

    end = time.time()
    logging.info("Temps total del test d'estrès: %.2f segons", end - start)
    logging.info("Temps mitjà per petició: %.2f segons", (end - start) / num_requests)

if __name__ == '__main__':
    main()
