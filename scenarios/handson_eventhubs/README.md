# Hands-on Event Hubs

## Deploy Azure resources

Go to [ks6088ts-labs/baseline-environment-on-azure-bicep: event-grid-mqtt scenario](https://github.com/ks6088ts-labs/baseline-environment-on-azure-bicep/blob/main/infra/scenarios/event-grid-mqtt/README.md) and follow the instructions.

Note: Turn on Event Hubs by setting `eventHubEnabled` to `true` in bicep parameter file.

```bicep
// Turn on Event Hubs
param eventHubEnabled = true
```

To receive messages from Event Hubs, you need to create a consumer group in the Event Hubs namespace.
Details are described in the [Send events to or receive events from event hubs by using Python](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-send?tabs=connection-string%2Croles-azure-portal).

## How to run

### Set environment variables

- Copy [settings.env.sample](./settings.env.sample) to `settings.env` and set your values.
- Run `poetry install` to install dependencies.

## Send messages

```shell
# Send messages from command line
poetry run python main.py send
```

On the other hand, you can send messages from Azure Event Grid.
Use MQTTX app to send messages to the Event Hubs.
Details are described in the [Connecting the clients to the EG Namespace using MQTTX app](https://learn.microsoft.com/en-us/azure/event-grid/mqtt-publish-and-subscribe-portal#connecting-the-clients-to-the-eg-namespace-using-mqttx-app)

## Receive messages

```shell
# Receive messages
❯ poetry run python main.py receive

Receiving message from Event Hubs
Received the event: "#0 event" from the partition with ID: "0"
Received the event: "#1 event" from the partition with ID: "0"
Received the event: "#2 event" from the partition with ID: "0"
Received the event: "[{"id":"446b6dff-77c2-4473-87e0-ae8112c36698","source":"thmi45djdbmxaegn","type":"MQTT.EventPublished","data_base64":"ewogICJtc2ciOiAiaGVsbG8gd29ybGQiCn0=","time":"2024-03-27T08:59:44.661+00:00","specversion":"1.0","datacontenttype":"application/octet-stream","subject":"contosotopics/topic1"}]" from the partition with ID: "0"
```
