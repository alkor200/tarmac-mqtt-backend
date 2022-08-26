import time
import paho.mqtt.client as mqtt

TOPIC = "motion_sensor"
BROKER_ADRESS = "127.0.0.1"
PORT = 1883


class MQTTLightManager():
    def __init__(self, light_list: list):
        self.lights = light_list
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT Broker: {BROKER_ADRESS}")
        self.mqtt_client.subscribe(TOPIC)

    def _on_message(self, client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print(f"received message: {msg}")
        try:
            light_id = int(msg)
            self._send_to_light(light_id)
        except ValueError:
            print("Message does not contain integer")

    def _send_to_light(self, light_id):
        print(f"Light {light_id} on")
        self.lights[light_id].turn_on()
        time.sleep(0.5)
        self.lights[light_id].turn_off()

    def run(self):
        self.mqtt_client.connect(BROKER_ADRESS, PORT)
        self.mqtt_client.loop_forever()
