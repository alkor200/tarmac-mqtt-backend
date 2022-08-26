import time
import paho.mqtt.client as mqtt

from threading import Thread

TOPIC = "esp32/pirsensor"
BROKER_ADRESS = "192.168.0.2"
PORT = 1883


class MQTTLightManager():
    def __init__(self, light_list: list):
        self.lights = light_list
        self.on_time = 3
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT Broker: {BROKER_ADRESS}")
        print(f"listening on Topic: {TOPIC}")
        self.mqtt_client.subscribe(TOPIC)

    def _on_message(self, client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print(f"received message: {msg}")
        try:
            light_id = int(msg)
            light_thread = Thread(target=self._send_to_light, args=(light_id,))
            light_thread.start()
        except ValueError:
            print("Message does not contain integer")

    def _send_to_light(self, light_id):
        print(f"Light {light_id} on -> GPIO {self.lights[light_id].pin} HIGH")
        self.lights[light_id].turn_on()
        self.lights[light_id].on_since = time.time()

    def all_on(self):
        for light in self.lights:
            light.turn_on()

    def all_off(self):
        for light in self.lights:
            light.turn_off()

    def run(self):
        while True:
            try:
                self.mqtt_client.connect(BROKER_ADRESS, PORT)
                self.mqtt_client.loop_start()
                while True:
                    for light in self.lights:
                        now = time.time()
                        if light.on_since is not None:
                            if now - light.on_since > self.on_time:
                                light.turn_off()
                                light.on_since = None
            except ConnectionRefusedError:
                time.sleep(3)
