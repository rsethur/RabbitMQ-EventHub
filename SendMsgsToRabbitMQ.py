import pika
import json

# Code to send simple JSON messages to a Work Queue of RabbitMQ
def main():
    #load config
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    # Setup connection
    credentials = pika.PlainCredentials(config["RMQ_USER_NAME"], config["RMQ_PASSWORD"])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config["RMQ_HOST"], port=config["RMQ_PORT"],
                                                                   virtual_host=config["RMQ_VIRTUALHOST"], credentials=credentials))
    channel = connection.channel()

    # Setup Work Queue
    channel.queue_declare(queue=config["RMQ_QUEUE_NAME"], durable=True)

    # Send messages to the queue
    for i in range(5):
        msg = {"itemId": i, "itemName":"drone"+str(i)}
        json_msg_str = json.dumps(msg)
        channel.basic_publish(
            exchange=config["RMQ_EXCHANGE"],
            routing_key=config["RMQ_ROUTING_KEY"],
            body=json_msg_str,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
    print("Sent")
    connection.close()

if __name__ == '__main__':
    main()