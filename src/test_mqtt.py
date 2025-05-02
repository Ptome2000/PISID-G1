import paho.mqtt.client as mqtt

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("pisid_mazesound_1")
    for i in range(500):
        res = mqttc.publish("pisid_mazesound_1", '{Player:1, Hour:"2024-07-04 16:29:21.281898", Sound:19.0}')
        print(f'enviado {i} {res}')

    # client.subscribe("pisid_g1_movimento_1")
    # for i in range(500):
    #     res = mqttc.publish("pisid_g1_movimento_1", '{"Player": 1, "Marsami": 47, "RoomOrigin": 4, "RoomDestiny": 5, "Status": 1}')
    #     print(f'enviado {i} {res}')

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("broker.emqx.io", 1883, 60)

mqttc.loop_forever()



