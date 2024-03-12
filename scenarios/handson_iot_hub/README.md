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
