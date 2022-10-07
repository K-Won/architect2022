import os
import sys
import argparse
from multiprocessing import Process, Pool
import multiprocessing
from queue_handler import QueueHandler
root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
print(root)

add_path_list = ['3rd_party_services', 'config', 'data_processing', 'data_sample', 'data_source', 'server', 'utils']
# topic_name: CIFAR10_DATA_SOURCE, CANCER_DATA_SOURCE

for add_path in add_path_list:
    if not root in sys.path:
        sys.path.append(root)

    if not add_path in sys.path:
        sys.path.append(os.path.join(root, add_path))

from data_consumer import DataConsumer
from redis_cli import RedisCli
from data_publisher import DataPublisher

import json

import time
import requests

def send_dlq(config, data):

    error_config = config
    if 'CIFAR10' in config['rabbit_config']['topic'] :
        error_config['rabbit_config']['topic'] = 'CIFAR10_DLQ'
    else:
        error_config['rabbit_config']['topic'] = 'CANCER_DLQ'
    data_publisher = DataPublisher(config['rabbit_config'])
    msg = json.dumps({
        "data": data
    })

    print('[ERROR]Send Dead Letter Queue([{}]) for that reason redis db is not working'.format(error_config['rabbit_config']['topic']))
    data_publisher.send_msg(msg)

def worker(item, config):

    redis_client = RedisCli(config['rabbit_config'])
    data = item['label_result']
    result = redis_client.insert(data)
    if result == False:
        send_dlq(config, data)
    else:
        # DB 저장
        print("{} - [SUB]CLASSIFICATION_LABELING - {}".format(multiprocessing.current_process(), data))
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="[Data Processing] Main")
    parser.add_argument('--mq_ip', '-ip', default='70.70.10.39', type=str, help='rabbit mq ip')
    parser.add_argument('--mq_port', '-port', default='5672', type=str, help='rabbit mq port')
    parser.add_argument('--service_ip', '-sip', default='http://70.70.202.133', type=str, help='prediction server ip')
    parser.add_argument('--config_file', '-cf', default='data_processing_config.json', type=str, help='config file path')
    args = parser.parse_args()
    thread_num = args.thread_num
    with open(os.path.join(args.config_file), 'r') as cf:
        config = json.load(cf)
    config['rabbit_config']['ip'] = args.mq_ip
    config['rabbit_config']['port'] = args.mq_port
    config['rabbit_config']['sip'] = args.service_ip
    config['rabbit_config']['sport'] = args.service_port
    config['rabbit_config']['topic'] = 'CLASSIFICATION_LABELING'

    #print("Config " + str(config))
    p = Pool(thread_num)
    consumer = DataConsumer(config['rabbit_config'])
    consumer.start()
    que = QueueHandler()
    while True:
        que_size = que.current_size()
        if que_size > 0:
            item = json.loads(que.get())
            p.apply(worker, args=(item, config, ))

