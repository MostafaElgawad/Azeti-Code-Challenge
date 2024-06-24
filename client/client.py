from threading import Event
from typing import Optional, Any

import paho.mqtt.client as mqtt

# Feel free to add more libraries (e.g.: The REST Client library)
import requests
from time import sleep
import json


mqtt_client: Optional[mqtt.Client] = None

mqtt_connection_event = Event()
secret_received_event = Event()

secret = -1


def send_secret_rest(secret_value: int):
    # Add the logic to send this secret value to the REST server.
    # We want to send a JSON structure to the endpoint `/secret_number`, using
    # a POST method.
    #
    # Assuming secret_value = 50, then the request will contain the following
    # body: {"value": 50}
    pass


def on_mqtt_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    mqtt_connection_event.set()


def on_mqtt_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    # Implement the logic to parse the received secret (we receive a json, but
    # we are interested just on the value) and send this value to the REST
    # server... or maybe the sending to REST should be done somewhere else...
    # do you have any idea why?
    message = json.loads(msg.payload)
    print("Message received-> " + msg.topic + " " + str(message.get('value')))
    secret_received_event.set()
    client.disconnect()


def connect_mqtt() -> mqtt.Client:
    client = mqtt.Client(
        clean_session=True,
        protocol=mqtt.MQTTv311
    )
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message
    client.loop_start()
    client.connect('mqtt-broker', 1883)
    return client

def get_server_status():
    url = 'http://server:80/ready'
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        if reponse.text == 'YES':
            return True
        else:
            raise ValueError('Server is Not Ready')
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request to {url} failed: {e}")
    
def wait_for_server_ready():
    # Implement code to wait until the server is ready, it's up to you how
    # to do that. Our advice: Check the server source code and check if there
    # is anything useful that can help.
    # Hint: If you prefer, feel free to delete this method, use an external
    # tool and incorporate it in the Dockerfile
    while True:
        try:
            get_server_status()
            print("Server is Ready")
            break
        except Exception as e:
            pass
        sleep(5)


def main():
    global mqtt_client

    wait_for_server_ready()

    mqtt_client = connect_mqtt()
    mqtt_connection_event.wait()

    # At this point, we have our MQTT connection established, now we need to:
    # 1. Subscribe to the MQTT topic: secret/number
    MQTT_TOPIC = 'secret/number'
    mqtt_client.subscribe(MQTT_TOPIC)
    # 2. Parse the received message and extract the secret number
    # 3. Send this number via REST to the server, using a POST method on the
    # resource `/secret_number`, with a JSON body like: {"value": 50}
    # 4. (Extra) Check the REST resource `/secret_correct` to ensure it was
    # properly set
    # 5. Terminate the script, only after at least a value was sent
    # Wait until a secret is received and processed
    secret_received_event.wait()


    try:
        mqtt_client.disconnect()
    except Exception:
        pass
    try:
        mqtt_client.loop_stop()
    except Exception:
        pass


if __name__ == '__main__':
    main()
