![](../fig/Smartenit_Main_Color_Positive.png?raw=true)

Making your world smarter and greener
# Python Serapi SDK

This repository is an **[Smartenit Inc.][smt-site]** workshop to get involved in the world of the IoT company services. Please enjoy it!
*Copyright Compacta International, Ltd 2017. All rights reserved*

## About this SDK
For simplicity, this SDK considers all requests asynchronous, so you will receive responses and reports asynchronously in a single callback. If you send a request which expects response, you will receive that message in that same callback.

## Getting messages
To process the messages coming from the coordinator using the Python SDK, set a handler for the received data as follow:
```python
import time
from serapi import serapi
def on_read(data):
  print("Data received!")
  print("Message name: ", data['serapi'])

api = serapi.SerApi("/dev/ttyUSB0")
api.setOnPacket(on_read)
api.send_request('SystemPing')
time.sleep(2)
```

``` text
Output:
Data received!
('Message name: ', 'SystemPingResponse')
```
The handler in this case is a python function but it could be a class method. Notice the sleep at the end of the script, it allows the program to run and receive the response before the script ends closing the port and the execution of the script.

### Supported incoming messages
| Message | Parameters |
| ------------- |:-------------:|
| SystemPingResponse | macFlags, services, firmwareVersion, profile, shortAddress, ieeeAddress |
| ReportAttributeMessage | mode, sourceAddress, sourceEndpoint, clusterId, commandId, manufacturerCode, attributes |
| ReadAttributesResponse | mode, sourceAddress, sourceEnpoint, clusterId, commandId, manufacturerCode, attributes |
| NetworkAddressResponse | ieeeAddress, shortAddress |

## Sending messages
The class method `send_request` serializes and sends to the coordinator the specified request with the given parameters. Each request has its own parameters, refer to [Serapi documentation](../ZBPCID_API.pdf)
For instance, to send a cluster command:
```python
from serapi import serapi

api = serapi.SerApi("/dev/ttyUSB0")
api.send_request('ClusterCommands', mode=0x12, destinationAddress=0x8627, destinationEndpoint=0x01, 
                 clusterId=0x0006, commandId=0x00)
```
The destination short address is 0x8627, the destination endpoint is 0x01, the clusterId is 0x0006 for OnOff and the commandId is 0x00 for Off command.

To receive messages from serapi refer to [Getting Messages](#getting-messages)

### Supported outcomming messages
| Message | Parameters (Required) | Parameters (optional)|
| ------------- |:-------------:|-------------:|
| SystemPing |  |  |
| ShortNetworkAddressRequest | ieeeAddress | startIndex|
| ClusterCommands | mode, destinationAddress, destinationEndpoint, culsterId, commandId | manufacturerCode |
| ReadAttributes | mode, destinationAddress, destinationEnpoint, clusterId, attributesList | manufacturerCode |

There are more that 20 outgoing requests and 30 incoming messages to be implemented in this SDK, are you interested in making a contribution? Follow the [Contribution guideline](#contributions-guidelines)

[smt-site]: http://smartenit.com/
