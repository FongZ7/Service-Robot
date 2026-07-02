from paho.mqtt import client as mqtt
import os

# 1. Mockup Config (จำลองตัวแปร config ขึ้นมา เพราะในโค้ดเดิมไม่มี)
config = {
    'MQTT': {
        'broker': '10.20.40.51',
        'port': 1883,
        'client_id': 'ServiceRobot_Client'
    }
}

mq = config['MQTT']
broker = mq['broker'] 
port = int(mq['port'])
client_id = mq['client_id']

class MQTTClient:
    def __init__(self):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, self.client_id)
        except AttributeError:
            self.client = mqtt.Client(self.client_id)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            result = "Connected successfully"
            print(result)

        else:
            result = f"Connect failed with code {rc}"
            print(result)


    def on_message(self, client, userdata, message):
        payload_str = message.payload.decode()
        result = f"Received message '{payload_str}' on topic '{message.topic}' with QoS {message.qos}"
        print(result)

        if message.topic == "robot/status":
            if payload_str == "2": 
                print("Status is 2: Robot is active") # 4. เติม Logic ที่หายไป


    def on_disconnect(self, client, userdata, rc):
        result = "Disconnected"
        print(result)

    def connect(self):
        if not self.broker:
            result = "Broker address is not set."
            print(result)
            return

        result = f"Connecting to broker at {self.broker}:{self.port}"
        print(result)
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
        except Exception as e:
            print(f"Connection Error: {e}")

    def disconnect(self):
        self.client.disconnect()

    def subscribe(self, topic, qos=0):
        self.client.subscribe(topic, qos)

    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)

    def publish(self, topic, payload, qos=0, retain=False):
        self.client.publish(topic, payload, qos, retain)

    def loop_forever(self):
        self.client.loop_forever()

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()