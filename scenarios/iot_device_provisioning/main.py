import os
import time
import uuid

import typer
from azure.iot.device import IoTHubDeviceClient, Message, ProvisioningDeviceClient
from dotenv import load_dotenv

app = typer.Typer()


@app.command()
def run():
    # https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/provision_symmetric_key.py
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=os.getenv("PROVISIONING_HOST"),
        registration_id=os.getenv("PROVISIONING_REGISTRATION_ID"),
        id_scope=os.getenv("PROVISIONING_IDSCOPE"),
        symmetric_key=os.getenv("PROVISIONING_SYMMETRIC_KEY"),
    )
    registration_result = provisioning_device_client.register()

    # The result can be directly printed to view the important details.
    print(registration_result)

    # Individual attributes can be seen as well
    print("The status was :-")
    print(registration_result.status)
    print("The etag is :-")
    print(registration_result.registration_state.etag)

    if registration_result.status == "assigned":
        print("Will send telemetry from the provisioned device")
        # Create device client from the above result
        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=os.getenv("PROVISIONING_SYMMETRIC_KEY"),
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
        )

        # Connect the client.
        device_client.connect()

        for i in range(1, 6):
            print("sending message #" + str(i))
            device_client.send_message("test payload message " + str(i))
            time.sleep(1)

        for i in range(6, 11):
            print("sending message #" + str(i))
            msg = Message("test wind speed " + str(i))
            msg.message_id = uuid.uuid4()
            device_client.send_message(msg)
            time.sleep(1)

            # finally, disconnect
            device_client.disconnect()
    else:
        print("Can not send telemetry from the provisioned device")


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
