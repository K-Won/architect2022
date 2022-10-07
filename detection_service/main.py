
import os
import sys
'''
root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
print(root)

add_path_list = ['3rd_party_services', 'config', 'data_processing', 'data_sample', 'data_source', 'server', 'utils']

for add_path in add_path_list:
    if not root in sys.path:
        sys.path.append(root)

    if not add_path in sys.path:
        sys.path.append(os.path.join(root, add_path))
'''

import json
import argparse
import random
import pika



def get_msg():
    with open("./cls.data", 'r') as f:
        data = f.readlines()
    index = random.randint(0, 19)
    msg = json.dumps({
        "label_result": data[index]
    })
    return msg


class DataPublisher:
    def __init__(self, ip, port):
        self.credentials = pika.PlainCredentials('rabbit', 'rabbit')
        self.topic_name = "CLASSIFICATION_LABELING"
        self.ip = ip
        self.port = port
        self.queue_name = 'park'
        self.channel, self.connection, self.routing_key, = self.connect()

    def connect(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.ip, port=self.port, credentials=self.credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.topic_name, exchange_type='topic')

        return channel, connection, self.queue_name

    def send_msg(self, msg):
        try:
            self.channel.basic_publish(exchange=self.topic_name, routing_key=self.routing_key, body=msg)

        except Exception as e:
            print('', e)
            self.channel, self.connection, self.routing_key, = self.connect()
            self.send_msg(msg)

    def disconnect(self):
        print('disconnect')
        self.connection.close()
import time
if __name__ == '__main__':
    print('Classification Labeling Service')
    parser = argparse.ArgumentParser(description="[Data Source] Main")
    parser.add_argument('--mq_ip', '-ip', default='rabbitmq', type=str, help='rabbit mq ip')
    parser.add_argument('--mq_port', '-port', default='5672', type=str, help='rabbit mq port')
    args = parser.parse_args()
    data_publisher = DataPublisher(args.mq_ip, args.mq_port)
    i = 0
    while True:
        time.sleep(10)
        i += 1
        msg = get_msg()
        data_publisher.send_msg()
        print("{} : {}".format(i, get_msg()))
