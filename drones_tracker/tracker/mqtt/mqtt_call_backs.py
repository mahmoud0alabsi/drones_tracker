import json
from django.utils import timezone
from django.contrib.gis.geos import Point
from tracker.models import Drone, DroneLog


def store_drone(topic, payload):
    """
    Parse payload and create
    or update drone in (Drone) model
    """
    try:
        serial = topic.split('/')[2]
        height = payload['height']
        home_distance = payload['home_distance']
        horizontal_speed = payload['horizontal_speed']
        vertical_speed = payload['vertical_speed']
        latitude = payload['latitude']
        longitude = payload['longitude']

        drone, _ = Drone.objects.update_or_create(
            serial=serial,
            defaults={
                'height': height,
                'home_distance': home_distance,
                'horizontal_speed': horizontal_speed,
                'vertical_speed': vertical_speed,
                'location': Point(latitude, longitude),
                'last_seen': timezone.now()
            }
        )

        store_drone_log(drone, topic, payload)

    except Exception as e:
        print('Exception: ' + str(e))


def store_drone_log(drone, topic, payload):
    """
    Create new log record in (DroneLog) model
    """
    try:
        serial = topic.split('/')[2]
        log = DroneLog.objects.create(
            drone=drone,
            payload=payload,
            timestamp=timezone.now()
        )
        log.save()
    except Exception as e:
        print(e)


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('MQTT_BROKER: Connected successfully')
        mqtt_client.subscribe('thing/product/+/osd')
    else:
        print('MQTT_BROKER: Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    print(
        f'MQTT_ON_MESSAGE: Received message on topic: {msg.topic}.')
    try:
        if msg == 'offline':
            print('MQTT_ON_MESSAGE: publisher exit topic.')
            return
        payload = json.loads(msg.payload.decode())
        store_drone(msg.topic, payload)
        print('MQTT_ON_MESSAGE: Received message stored.')

    except json.JSONDecodeError as e:
        print(f"MQTT_ON_MESSAGE: Error decoding MQTT message, {e}")


def on_disconnect(client, userdata, rc):
    print("MQTT_BROKER: Disconnected from MQTT Broker")
