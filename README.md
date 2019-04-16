# Push events from RabbitMQ to Azure Event Hubs

A fun collaboration between [Sethu Raman](https://github.com/rsethur/) and __Donovan White__.

__Work in progress -beware!__

__Step 1:__ Setup Rabbit MQ - docker setup is quick. Below one liner should work. However [official documentation](https://hub.docker.com/_/rabbitmq) is available for reference 
```
docker run -d -p 5672:5672 -h rabbit_host --name rmq rabbitmq:3.7.14
```

__Step 2:__ Setup Event Hubs: Follow instructions in the `EventHubsSetup.script`

__Step 3:__ Setup python environment (conda/virtual env) - and` pip install pika azure-eventhub`

__Step 3:__ Update the `config.json` with both Rabbit MQ & Event Hub parameters

__Step 4:__ Pump messages into Rabbit MQ by running `SendMsgsToRabbitMQ.py`

__Step 5:__ Push messages from Rabbit MQ to Azure Event Hub by running `PushFromRabbitToEH.py`

__Step 6:__ You could check the messages in Azure Event Hub by running `EventHubTestRecv.py`
