import json
import os
import pika
import logging
import time
import sys
import numpy as np
from basic_rec_utilities.schemas import UserActivity
from basic_rec_utilities.db import get_conn_str, interaction_to_rating
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

# App Config
USER = os.getenv("RECS_MQ_USER", default="user")
PWD = os.getenv("RECS_MQ_PWD", default="pwd")
HOST = os.getenv("RECS_MQ_HOST", default="recommender-mq-rabbitmq.default.svc.cluster.local")
PORT = int(os.getenv("RECS_MQ_PORT", default="5672"))
TOPIC = os.getenv("RECS_NEW_UA_TOPIC", default='user_activity_available')
DB_USER = os.getenv("RECS_DB_USER", default="activity_ingest_svc")
DB_PWD = os.getenv("RECS_DB_PWD")
DB_HOST = os.getenv("RECS_DB_HOST")

# Logger Config
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", default="INFO"))
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(console_handler)

class IngestManager:
    """
    """
    def __init__(self, mq_user:str, mq_pwd:str, mq_host:str, mq_port:int) -> None:
        # Message Queue Config
        mq_creds = pika.PlainCredentials(mq_user, mq_pwd)
        self.mq_conn = pika.BlockingConnection(pika.ConnectionParameters(mq_host, mq_port, '/', mq_creds))
        self.db_engine = create_engine(get_conn_str(DB_USER, DB_PWD, DB_HOST))
        self.db_factory = sessionmaker(bind=self.db_engine)
        md = MetaData()
        self.ratings_table = Table('movie_ratings', md, 
                            Column('user_id', Integer),
                            Column('movie_id', Integer),
                            Column('rating', Float),
                            Column('rating_timestamp', String))
        md.create_all(self.db_engine)

    def ingest_activity(self, ch, method, properties, body):
        logger.debug("[x] Received %r" % body)
        ua = UserActivity(json.loads(body.decode("utf-8")))
        logger.debug(f"Loaded Activity: {ua.to_json()}")
        for data in ua.activity:
            interaction, items = data["interaction"], data["items"]
            logger.info(f"User: {ua.user}, Interaction: {interaction}, Items: {items}")
            # Write to DB
            self._db_write_activity(ua.user, interaction, items)

    def _db_write_activity(self, user:int, interaction:str, items:list):
        values = [(user, id, interaction_to_rating(interaction), int(time.time())) for id in items]
        self.db_engine.execute(self.ratings_table.insert().values(values))


    
    def run(self):
        """
        """
        channel = self.mq_conn.channel()
        channel.queue_declare(queue=TOPIC)
        channel.basic_consume(queue=TOPIC, auto_ack=True, on_message_callback=self.ingest_activity)
        logger.info("Listening for messages")
        channel.start_consuming()



if __name__ == "__main__":
    m = IngestManager(USER, PWD, HOST, PORT)
    m.run()
