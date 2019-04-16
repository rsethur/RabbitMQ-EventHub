# Code for printing messages from EventHub
# Based on : https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-receive

import json
import time
from azure.eventhub import EventHubClient, Receiver, Offset

def main():
    total = 0
    last_sn = -1
    last_offset = "-1"

    #load config
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    client = EventHubClient(config["EH_ADDRESS"], debug=False, username=config["EH_USER"], password=config["EH_KEY"])
    try:
        receiver = client.add_receiver(config["EH_CONSUMER_GROUP"], config["EH_PARTITION"], prefetch=5000, offset=Offset(config["EH_OFFSET"]))
        client.run()
        start_time = time.time()
        for event_data in receiver.receive():
            last_offset = event_data.offset
            last_sn = event_data.sequence_number
            #print("Received: {}, {}".format(last_offset, last_sn))
            print(event_data.body_as_str(encoding='UTF-8'))
            total += 1

        end_time = time.time()
        client.stop()
        run_time = end_time - start_time
        print("Received {} messages in {} seconds".format(total, run_time))

    except KeyboardInterrupt:
        pass
    finally:
        client.stop()

if __name__ == '__main__':
    main()