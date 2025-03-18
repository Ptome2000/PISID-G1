import paho.mqtt.client as mqtt

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqttc.connect("broker.mqtt-dashboard.com", 1883, 60)

mqttc.publish("pisid_g1_player", '{"player": 1}', 2)

