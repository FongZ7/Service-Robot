from flask import Flask, jsonify, request
from api import API
import os
import threading
from mqtt import MQTTClient

app = Flask(__name__)
mqtt = MQTTClient()

# แก้ไขบรรทัดนี้: ส่ง request เข้าไปใน API ด้วย
api = API(app, mqtt)

def run_mqtt():
    print("Starting MQTT...")
    mqtt.connect()
    mqtt.subscribe("robot/poi")
    mqtt.subscribe("robot/status")
    mqtt.loop_forever() 

if __name__ == '__main__':
    # 1. สร้าง Thread สำหรับ MQTT
    mqtt_thread = threading.Thread(target=run_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    # 2. รัน Flask API
    print("Starting Flask API on port 5000...")
    app.run(debug=False, host='0.0.0.0', port=5000)