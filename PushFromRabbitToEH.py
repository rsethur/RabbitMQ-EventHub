import pika
import json
import time
from azure.eventhub import EventHubClient, Sender, EventData

# Code to get messages from RabbitMQ Queue and push it to Azure EventHub
class Worker(object):

    event_hub_sender = None
    config = None

    def __init__(self):
        #load config
        with open('config.json', 'r') as json_file:
            self.config = json.load(json_file)

        # Create Event Hubs client
        client = EventHubClient(self.config["EH_ADDRESS"], debug=False, username=self.config["EH_USER"], password=self.config["EH_KEY"])
        Worker.event_hub_sender = client.add_sender(partition="0")
        client.run()

    def rabbit_queue_callback(ch, method, properties, body):
        msg_str = body.decode()
        print(msg_str)
        #static variabe access (hack!) - fix this
        Worker.event_hub_sender.send(EventData(msg_str))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_rabbit_consumption(self):
        # Setup Rabbit connection & Queue
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.config["RMQ_HOST"]))
        channel = connection.channel()
        channel.queue_declare(queue=self.config["RMQ_QUEUE_NAME"], durable=True)
        channel.basic_qos(prefetch_count=1)
        # Setup Rabbit callback
        channel.basic_consume(queue=self.config["RMQ_QUEUE_NAME"], on_message_callback=Worker.rabbit_queue_callback)
        channel.start_consuming()

if __name__ == '__main__':
    worker = Worker()
    worker.start_rabbit_consumption()