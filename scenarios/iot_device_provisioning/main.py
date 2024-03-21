import os
import uuid
from typing import Union

import typer
from azure.iot.device import (
    IoTHubDeviceClient,
    Message,
    ProvisioningDeviceClient,
    RegistrationResult,
)
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential

app = typer.Typer()


class ProvisioningDeviceClientWrapper:
    def __init__(self) -> None:
        self._provisioning_device_client = (
            ProvisioningDeviceClient.create_from_symmetric_key(
                provisioning_host=os.getenv("PROVISIONING_HOST"),
                registration_id=os.getenv("PROVISIONING_REGISTRATION_ID"),
                id_scope=os.getenv("PROVISIONING_IDSCOPE"),
                symmetric_key=os.getenv("PROVISIONING_SYMMETRIC_KEY"),
            )
        )

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def register_device(self) -> RegistrationResult:
        print("Registering device with Provisioning Service")
        registration_result = self._provisioning_device_client.register()
        if registration_result.status != "assigned":
            raise Exception("Device registration status is not assigned")
        return registration_result


class IotHubDeviceClientWrapper:
    def __init__(self, hostname: str, device_id: str) -> None:
        self._iot_hub_device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=os.getenv("PROVISIONING_SYMMETRIC_KEY"),
            hostname=hostname,
            device_id=device_id,
        )

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def connect(self):
        print("Connecting to IoT Hub")
        self._iot_hub_device_client.connect()

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def send_message(self, message: Union[Message, str]):
        print("Sending message to IoT Hub")
        self._iot_hub_device_client.send_message(message)

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def disconnect(self):
        print("Disconnecting from IoT Hub")
        self._iot_hub_device_client.disconnect()


@app.command()
def run():
    # https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/provision_symmetric_key.py
    provisioning_device_client = ProvisioningDeviceClientWrapper()
    registration_result = provisioning_device_client.register_device()

    # The result can be directly printed to view the important details.
    print(registration_result)

    # Individual attributes can be seen as well
    print("The status was :-")
    print(registration_result.status)
    print("The etag is :-")
    print(registration_result.registration_state.etag)

    print("Will send telemetry from the provisioned device")
    # Create device client from the above result
    device_client = IotHubDeviceClientWrapper(
        hostname=registration_result.registration_state.assigned_hub,
        device_id=registration_result.registration_state.device_id,
    )

    # Connect the client.
    device_client.connect()

    for i in range(1, 6):
        print(f"sending message #{str(i)}")
        device_client.send_message(f"test payload message {str(i)}")

    for i in range(6, 11):
        print(f"sending message #{str(i)}")
        msg = Message(
            data=f"test wind speed {str(i)}",
            message_id=uuid.uuid4(),
        )
        device_client.send_message(msg)

    # finally, disconnect
    device_client.disconnect()


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
