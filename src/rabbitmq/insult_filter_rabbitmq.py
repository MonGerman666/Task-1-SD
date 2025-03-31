import pika
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FILTERED_TEXTS = []
KNOWN_INSULTS = ["insult1", "insult2"]

class InsultFilterRPC:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpc_filter_queue')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='rpc_filter_queue', on_message_callback=self.on_request)

    def on_request(self, ch, method, props, body):
        message = body.decode('utf-8')
        logging.info("Rebut filter request: %s", message)
        if message.startswith("filter_text:"):
            text = message.split(":", 1)[1]
            response = self.filter_text(text)
        elif message == "get_filtered_texts":
            response = "|".join(self.get_filtered_texts())
        else:
            response = "Unknown command"
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id = props.correlation_id),
            body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def filter_text(self, text):
        filtered = text
        for insult in KNOWN_INSULTS:
            filtered = filtered.replace(insult, "CENSORED")
        FILTERED_TEXTS.append(filtered)
        logging.info("Text filtrat: %s", filtered)
        return filtered

    def get_filtered_texts(self):
        return FILTERED_TEXTS

    def start(self):
        logging.info("RabbitMQ InsultFilter RPC Server esperant peticions RPC...")
        self.channel.start_consuming()

def main():
    rpc = InsultFilterRPC()
    rpc.start()

if __name__ == '__main__':
    main()
