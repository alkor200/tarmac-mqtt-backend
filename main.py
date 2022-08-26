from light import Light
from mqtt_light_manager import MQTTLightManager

# relais = [26, 16, 20, 21, 5, 6, 19, 13, 18, 17, 27, 23, 22]  # , 24, 25, 12]
relais = []

if __name__ == '__main__':
    manager = MQTTLightManager

    light_list = []
    i = 0
    for pin in relais:
        light_list.append(
            Light(number=i, pin=pin)
        )
        i += 1

    light_manager = MQTTLightManager(light_list)

    light_manager.run()