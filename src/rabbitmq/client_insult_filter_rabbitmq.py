import pika
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InsultFilterRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
    rpc_client = InsultFilterRpcClient()
    res1 = rpc_client.call("filter_text:Aquest text conté insult1 i més coses.")
    res2 = rpc_client.call("filter_text:Aquest text està net.")
    res3 = rpc_client.call("filter_text:Aquest text té insult2 i insult1.")
    logging.info("Texts filtrats: %s, %s, %s", res1, res2, res3)
    all_filtered = rpc_client.call("get_filtered_texts")
    logging.info("Tots els textos filtrats: %s", all_filtered)

if __name__ == '__main__':
    main()
