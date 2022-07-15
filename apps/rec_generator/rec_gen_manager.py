import os
import pika

USER = os.getenv("RECS_MQ_USER", default="user")
PWD = os.getenv("RECS_MQ_PWD", default="pwd")
HOST = os.getenv("RECS_MQ_HOST", default="recommender-mq-rabbitmq.default.svc.cluster.local")
PORT = int(os.getenv("RECS_MQ_PORT", default="5672"))
TOPIC = os.getenv("RECS_NEW_UA_TOPIC", default='user_activity_available')

class IngestManager:
    """
    """
    def __init__(self, mq_user:str, mq_pwd:str, mq_host:str, mq_port:int) -> None:
        # Message Queue Config
        credentials = pika.PlainCredentials(mq_user, mq_pwd)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(mq_host, mq_port, '/', credentials))

    def consumer_callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body, flush=True)
    
    def run(self):
        """
        """
        channel = self.connection.channel()
        channel.queue_declare(queue=TOPIC)
        channel.basic_consume(queue=TOPIC, auto_ack=True, on_message_callback=self.consumer_callback)
        print("Waiting for messages", flush=True)
        channel.start_consuming()



if __name__ == "__main__":
    m = IngestManager(USER, PWD, HOST, PORT)
    m.run()