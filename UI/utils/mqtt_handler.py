import logging
import time
import os

class MQTTClient:
    def __init__(self, broker='10.20.40.51', port=1883):
        self.broker = broker
        self.port = port

        self.topics = {
            "battery_status": "robot/battery",
            "current_poi": "robot/current_poi",
            "robot_poi": "robot/poi",

            # "emergency": "robot/emergency",
            "charge": "robot/charge",
            "status": "robot/status",
        }

        self.client = mqtt.Client()

        # Assign callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("MQTTClient")

        #value
        self.percent_battery = None


    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info("Connected to broker successfully!")
            # Subscribe to all topics
            for topic_name, topic in self.topics.items():
                self.client.subscribe(topic)
                self.logger.info(f"Subscribed to topic: {topic}")
        else:
            self.logger.error(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            message = msg.payload.decode()
            self.logger.info(f"Message received on topic {msg.topic}: {message}")
        except UnicodeDecodeError:
            self.logger.error(f"Failed to decode message on topic {msg.topic}: {msg.payload}")




    def on_publish(self, client, userdata, mid):
        self.logger.info(f"MQTT Message published")

    def connect(self):
        """Connect to the MQTT broker."""
        try:
            self.logger.info(f"Connecting to broker {self.broker} on port {self.port}...")
            self.client.connect(self.broker, self.port, keepalive=60)
        except Exception as e:
            self.logger.error(f"Failed to connect to broker: {e}")

    def publish(self, topic, message):
        """Publish a message to a specific topic."""
        if topic in self.topics.values():
            self.client.publish(topic, message)
            self.logger.info(f"Published message: '{message}' to topic: '{topic}'")
        else:
            self.logger.warning(f"Topic '{topic}' is not in the predefined list.")

    def start(self):
        """Start the MQTT client loop."""
        self.client.loop_start()

    def stop(self):
        """Stop the MQTT client loop and disconnect."""
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info("Disconnected from broker.")
