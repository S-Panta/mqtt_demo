## Client
-Clients can both publish messages to topics and subscribe to receive messages on specific topics
## Designing a Broker
- An intermediary entity that enables MQTT clients to communicate.

Topic based filtering
MQTT is lighter than the HTTP 1.1 protocol. Seriously what does it even mean?

One can either open socket port and then get request for health checking. But mosquitto already have their internalized health checking. `$SYS` reveals the internal information of broker