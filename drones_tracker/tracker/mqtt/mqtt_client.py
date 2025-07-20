import paho.mqtt.client as mqtt
from django.conf import settings
from .mqtt_call_backs import *


def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
    client.connect(
        host=settings.MQTT_SERVER,
        port=settings.MQTT_PORT,
        keepalive=settings.MQTT_KEEPALIVE
    )
    client.loop_start()
