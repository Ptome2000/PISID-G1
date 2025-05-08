import sys
import time
import threading
import paho.mqtt.client as mqtt

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("pisid_g1_ruido_1")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# Individual functions for sending messages
def send_message_1():
    message = '{"Player":1, "Hour":"2025-01-01 16:29:21.281898", "Sound":20}'  # +90%
    mqttc.publish("pisid_g1_ruido_1", message)
    print(f"Sent: {message}")

def send_message_2():
    message = '{"Player":1, "Hour":"2025-01-01 16:29:22.281898", "Sound":19.4}'  # -90%
    mqttc.publish("pisid_g1_ruido_1", message)
    print(f"Sent: {message}")

def send_message_3():
    message = '{"Player":1, "Hour":"2025-01-01 16:00:23.281898", "Sound":19.0}'  # Normal sound (should not trigger)
    mqttc.publish("pisid_g1_ruido_1", message)
    print(f"Sent: {message}")

def send_message_4():
    message = '{"Player":1, "Hour":"2025-01-01 16:00:36.281898", "Sound":19.0}'  # Normal sound (should trigger)
    mqttc.publish("pisid_g1_ruido_1", message)
    print(f"Sent: {message}")

def send_message_5():
    message = '{"Player":1, "Hour":"2025-01-01 16:29:22.281898", "Sound":27}'  # Above max, GAME OVER
    mqttc.publish("pisid_g1_ruido_1", message)
    print(f"Sent: {message}")

# Main function to orchestrate message sending
def send_mqtt_messages():
    send_message_1()
    time.sleep(1)  # Simulate delay between messages
    send_message_2()
    time.sleep(1)
    send_message_3()
    time.sleep(35)  # Simulate 30 seconds delay
    send_message_4()
    send_message_5()

# Set up MQTT callbacks
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect to the MQTT broker
mqttc.connect("broker.emqx.io", 1883, 60)

# Start the message-sending thread
message_thread = threading.Thread(target=send_mqtt_messages)
message_thread.start()

# Start the MQTT loop
mqttc.loop_forever()