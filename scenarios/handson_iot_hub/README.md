# Hands-on IoT Hub

## Receive direct method requests

- [samples/sync-samples/receive_direct_method.py](https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/receive_direct_method.py)
- [Get started with device management (Python)](https://learn.microsoft.com/en-us/azure/iot-hub/device-management-python)

```shell
DEVICE_ID="YOUR_DEVICE_ID"
HUB_NAME="YOUR_HUB_NAME"
RESOURCE_GROUP="YOUR_RESOURCE_GROUP"

# get the connection string for the device
az iot hub device-identity connection-string show \
    --device-id $DEVICE_ID \
    --hub-name $HUB_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

# invoke the method from the cloud
az iot hub invoke-device-method \
    --device-id $DEVICE_ID \
    --hub-name $HUB_NAME \
    --method-name "method1" \
    --method-payload "{'hello': 'world'}"
```

## Device Twin

- [Understand and use device twins in IoT Hub](https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-device-twins)
- [samples/sync-samples/receive_twin_desired_properties_patch.py](https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/receive_twin_desired_properties_patch.py)
- [Get started with device twins (Python)](https://learn.microsoft.com/en-us/azure/iot-hub/device-twins-python)

```shell
HUB_NAME="YOUR_HUB_NAME"
RESOURCE_GROUP="YOUR_RESOURCE_GROUP"

# get the connection string for IoT Hub
az iot hub connection-string show \
    --hub-name $HUB_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table
```

## File upload

- [Upload files from your device to the cloud with Azure IoT Hub (Python)](https://learn.microsoft.com/en-us/azure/iot-hub/file-upload-python)
