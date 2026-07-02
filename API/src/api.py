from flask import request, jsonify  # 1. ต้อง import request และ jsonify มาใช้งาน
from action import Action
import time
import os

action = Action()   

class API:

    def __init__(self, app,  mqtt): 

        self.data = {
            "message": "Service Robot API is running",
        }

        # --- Route Definitions ---

        @app.route('/slot', methods=['GET'])
        def slot():
            response = action.slot()
            return response

        # Read Locker Status
        @app.route('/locker_status', methods=['GET'])
        def locker_status():
            response = action.locker_status()

            return response

        # Get drug log
        @app.route('/drug_log', methods=['POST', 'GET'])
        def drug_log():
            response = action.get_drug_log()

            return response 
        
        # Select Insert or Takeout (QR Scan)
        @app.route('/qr_scan', methods=['POST'])
        def qr_scan():
            new_data = request.get_json()
            print(new_data)
            response = action.recieved_qr_data(new_data, mqtt) 
            return jsonify({'message': response})
        
        # Select Insert or Takeout (In/Out)
        @app.route('/in_out', methods=['POST'])
        def in_out(): 
            new_data = request.get_json()
            print(str(new_data))
            action.in_out(new_data)
            return jsonify({'message': 'Received message'}) 
        
        # Select Slot
        @app.route('/select_slot', methods=['POST'])
        def select_slot():
            new_data = request.get_json()
            print(str(new_data))
            action.select_slot(new_data)
            return jsonify({'slot No': new_data["slot"]}) 


        @app.route('/confirm_takeout', methods=['POST'])
        def confirm_takeout():
            new_data = request.get_json()
            print(str(new_data))
            action.confirm_takeout(str(new_data["slot"]))

            return jsonify({'message': 'Received message'})

        @app.route('/insert_location', methods=['POST'])
        def insert_location():
            new_data = request.get_json()
            print(new_data)
            action.insert_location(new_data)

            return jsonify({'message': 'Data insert successfully'})
        
        # Open/Close Gate
        @app.route('/gate', methods=['POST'])
        def gate():
            new_data = request.get_json()
            print(new_data["status"])
            response = action.gate(new_data["status"])

            while response == "error":
                response = action.gate(new_data["status"])

            return jsonify({'message': 'Received message'})
        
        # start send 
        @app.route('/start', methods=['POST'])
        def start():
            new_data = request.get_json()
            print(f"start status: {new_data}")
            response, send_status = action.start(new_data["status"])
            
            mqtt.publish("robot/poi", response)
            mqtt.publish("api/send_status", send_status)
            print(f"Go to poi {response}")

            return jsonify({'message': 'Received message'})
        
        # Pause and Resume
        @app.route('/pause', methods=['POST'])
        def pause():
            new_data = request.get_json()
            print(f"pause status: {new_data}")
            print(new_data["status"])
            if new_data["status"] == "pause":
                mqtt.publish("robot/status", 12) 
            
            elif new_data["status"] == "resume":
                mqtt.publish("robot/status", 11) 
                # time.sleep(1)
                mqtt.publish("robot/status", 3) 
                time.sleep(13)
                print(f"Robot status: {robot_status}")
                
                if(robot_status == 0):
                    # read robot startus for check
                    file_name = "going_to_poi.txt"
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        going_to = int(file.read())
                        file.close() 
                    print(f"Robot going to: {going_to}")
                    mqtt.publish("robot/poi", going_to)


            return jsonify(new_data)