import asyncio
import os

import typer
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubConsumerClient, EventHubProducerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from dotenv import load_dotenv

app = typer.Typer()


async def send_async():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=os.getenv("EVENT_HUB_CONNECTION_STR"),
        eventhub_name=os.getenv("EVENT_HUB_NAME"),
    )
    async with producer:
        event_data_batch = await producer.create_batch()

        for i in range(3):
            event_data_batch.add(EventData(f"#{i} event"))

        await producer.send_batch(event_data_batch)


async def on_event(partition_context, event):
    print(
        'Received the event: "{}" from the partition with ID: "{}"'.format(
            event.body_as_str(encoding="UTF-8"), partition_context.partition_id
        )
    )
    await partition_context.update_checkpoint(event)


async def receive_async():
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        os.getenv("BLOB_STORAGE_CONNECTION_STRING"),
        os.getenv("BLOB_CONTAINER_NAME"),
    )

    client = EventHubConsumerClient.from_connection_string(
        os.getenv("EVENT_HUB_CONNECTION_STR"),
        consumer_group="$Default",
        eventhub_name=os.getenv("EVENT_HUB_NAME"),
        checkpoint_store=checkpoint_store,
    )
    async with client:
        await client.receive(on_event=on_event, starting_position="-1")


@app.command()
def send():
    print("Sending message to Event Hubs")
    asyncio.run(send_async())


@app.command()
def receive():
    print("Receiving message from Event Hubs")
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(receive_async())


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
