import os
import time

import typer
from azure.core.exceptions import AzureError
from azure.iot.device import IoTHubDeviceClient, IoTHubModuleClient, MethodResponse
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import QuerySpecification, Twin, TwinProperties
from azure.storage.blob import BlobClient
from dotenv import load_dotenv

app = typer.Typer()


@app.command()
def device_twin_update_tags():
    try:
        iothub_registry_manager = IoTHubRegistryManager(
            os.getenv("IOT_HUB_CONNECTION_STRING")
        )

        twin = iothub_registry_manager.get_twin(os.getenv("DEVICE_ID"))
        twin_patch = Twin(
            tags={"location": {"region": "US", "plant": "Redmond43"}},
            properties=TwinProperties(desired={"power_level": 1}),
        )
        twin = iothub_registry_manager.update_twin(
            os.getenv("DEVICE_ID"), twin_patch, twin.etag
        )
        print("Tags updated for device: {}".format(twin.device_id))

    except Exception as ex:
        print("Unexpected error {0}".format(ex))
        return
    except KeyboardInterrupt:
        print("IoT Hub Device Twin service sample stopped")


@app.command()
def device_twin_query_iot_hub():
    try:
        iothub_registry_manager = IoTHubRegistryManager(
            os.getenv("IOT_HUB_CONNECTION_STRING")
        )
        query_spec = QuerySpecification(
            query="SELECT * FROM devices WHERE tags.location.plant = 'Redmond43'"
        )
        query_result = iothub_registry_manager.query_iot_hub(query_spec, None, 100)
        print(
            "Devices in Redmond43 plant: {}".format(
                ", ".join([twin.device_id for twin in query_result.items])
            )
        )

        print()

        query_spec = QuerySpecification(
            query="SELECT * FROM devices WHERE tags.location.plant = 'Redmond43' AND properties.reported.connectivity = 'cellular'"
        )
        query_result = iothub_registry_manager.query_iot_hub(query_spec, None, 100)
        print(
            "Devices in Redmond43 plant using cellular network: {}".format(
                ", ".join([twin.device_id for twin in query_result.items])
            )
        )

    except Exception as ex:
        print("Unexpected error {0}".format(ex))
        return
    except KeyboardInterrupt:
        print("IoT Hub Device Twin service sample stopped")


@app.command()
def device_twin_update_reported_properties():
    print("Starting the Python IoT Hub Device Twin device sample...")
    # Instantiate client
    client = IoTHubModuleClient.create_from_connection_string(
        os.getenv("IOT_HUB_DEVICE_CONNECTION_STRING")
    )

    # Define behavior for receiving twin desired property patches
    def twin_patch_handler(twin_patch):
        print("Twin patch received:")
        print(twin_patch)

    try:
        # Set handlers on the client
        client.on_twin_desired_properties_patch_received = twin_patch_handler
    except Exception as ex:
        # Clean up in the event of failure
        print(ex)
        client.shutdown()

    print("IoTHubModuleClient waiting for commands, press Ctrl-C to exit")

    try:
        # Update reported properties with cellular information
        print("Sending data as reported property...")
        reported_patch = {"connectivity": "cellular"}
        client.patch_twin_reported_properties(reported_patch)
        print("Reported properties updated")

        # Wait for program exit
        while True:
            time.sleep(1000000)
    except KeyboardInterrupt:
        print("IoT Hub Device Twin device sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()


@app.command()
def direct_method():
    # https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/receive_direct_method.py

    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = os.getenv("IOT_HUB_DEVICE_CONNECTION_STRING")
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    device_client.connect()

    # Define behavior for handling methods
    def method_request_handler(method_request):
        # Determine how to respond to the method request based on the method name
        if method_request.name == "method1":
            print(method_request.payload)
            payload = {"result": True, "data": "some data"}  # set response payload
            status = 200  # set return status code
            print("executed method1")
        elif method_request.name == "method2":
            payload = {"result": True, "data": 1234}  # set response payload
            status = 200  # set return status code
            print("executed method2")
        else:
            payload = {
                "result": False,
                "data": "unknown method",
            }  # set response payload
            status = 400  # set return status code
            print("executed unknown method: " + method_request.name)

        # Send the response
        method_response = MethodResponse.create_from_method_request(
            method_request, status, payload
        )
        device_client.send_method_response(method_response)

    # Set the method request handler on the client
    device_client.on_method_request_received = method_request_handler

    # Wait for user to indicate they are done listening for messages
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break

    # finally, shut down the client
    device_client.shutdown()


def store_blob(blob_info, file_name):
    try:
        sas_url = f"https://{blob_info['hostName']}/{blob_info['containerName']}/{blob_info['blobName']}{blob_info['sasToken']}"
        print(
            f"Uploading file: {file_name} to Azure Storage as blob: {blob_info['blobName']} in container {blob_info['containerName']}"
        )

        # Upload the specified file
        with BlobClient.from_blob_url(sas_url) as blob_client:
            with open(file_name, "rb") as f:
                result = blob_client.upload_blob(f, overwrite=True)
                return (True, result)

    except FileNotFoundError as ex:
        # catch file not found and add an HTTP status code to return in notification to IoT Hub
        ex.status_code = 404
        return (False, ex)

    except AzureError as ex:
        # catch Azure errors that might result from the upload operation
        return (False, ex)


@app.command()
def file_upload(path_to_file="./.gitignore"):
    device_client = IoTHubDeviceClient.create_from_connection_string(
        os.getenv("IOT_HUB_DEVICE_CONNECTION_STRING")
    )

    try:
        print("IoT Hub file upload sample, press Ctrl-C to exit")
        # Connect the client
        device_client.connect()

        # Get the storage info for the blob
        blob_name = os.path.basename(path_to_file)
        storage_info = device_client.get_storage_info_for_blob(blob_name)

        # Upload to blob
        success, result = store_blob(storage_info, path_to_file)

        if success:
            print("Upload succeeded. Result is: \n")
            print(result)
            print()

            device_client.notify_blob_upload_status(
                storage_info["correlationId"], True, 200, "OK: {}".format(path_to_file)
            )

        else:
            # If the upload was not successful, the result is the exception object
            print("Upload failed. Exception is: \n")
            print(result)
            print()

            device_client.notify_blob_upload_status(
                storage_info["correlationId"], False, result.status_code, str(result)
            )
    except KeyboardInterrupt:
        print("IoTHubDeviceClient sample stopped")
    finally:
        # Graceful exit
        device_client.shutdown()


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
