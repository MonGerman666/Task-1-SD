import pika
import uuid
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_rabbitmq(retries=5, delay=2):
    for attempt in range(1, retries + 1):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            logging.info("Connexió a RabbitMQ establerta en l'intent %d", attempt)
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            logging.error("Error de connexió a RabbitMQ en l'intent %d: %s", attempt, e)
            time.sleep(delay)
    raise Exception("No es pot connectar a RabbitMQ després de %d intents" % retries)

class InsultFilterRpcClient:
    def __init__(self):
        self.connection = connect_rabbitmq()
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode('utf-8')

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_filter_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def main():
    try:
        rpc_client = InsultFilterRpcClient()
    except Exception as e:
        logging.error("No s'ha pogut establir la connexió a RabbitMQ per InsultFilter: %s", e)
        return

    res1 = rpc_client.call("filter_text:Aquest text conté insult1 i altres coses.")
    res2 = rpc_client.call("filter_text:Aquest text està net.")
    res3 = rpc_client.call("filter_text:Aquest text té insult2 i insult1.")
    logging.info("Texts filtrats: %s, %s, %s", res1, res2, res3)
    all_filtered = rpc_client.call("get_filtered_texts")
    logging.info("Tots els textos filtrats: %s", all_filtered)

if __name__ == '__main__':
    main()
