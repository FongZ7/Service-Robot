from datetime import datetime
import json
import os
import time
from typing import Any, Dict


class Action:
    def __init__(self):
        # Try to reuse project's mock data when available
        try:
            from UI.utils.mockup_data import (
                data as slot_data,
                insert_table,
                barcode_scan,
                patients2,
                top_bar_status_batt,
            )
            self.slot_data = slot_data
            self.insert_table = insert_table
            self.barcode_scan = barcode_scan
            self.patients2 = patients2
            self.top_bar = top_bar_status_batt
        except Exception:
            # Fallback defaults
            self.slot_data = {
                f"slot{i+1}": {
                    "name": {"first": None, "last": None},
                    "hn": None,
                    "gender": None,
                    "bed_number": None,
                    "drugs": [],
                    "timestamp": None,
                    "location": None,
                    "slot_id": i + 1,
                    "IsReturn": False,
                    "WhyReturn": None,
                }
                for i in range(8)
            }
            self.insert_table = []
            self.barcode_scan = {"name": "Demo User", "hn": 111111, "drug_name": "Paracetamol", "detail": "demo"}
            self.patients2 = {}
            self.top_bar = {"status_batt": 100}

        # simple in-memory logs
        self.in_out_log = []
        self.select_log = []

    def get_drug_log(self):
        try:
            # ตัวอย่างการดึงข้อมูล (ถ้ามี Database ให้แก้ Query ตรงนี้)
            # cursor = self.db.cursor()
            # cursor.execute("SELECT * FROM history_log ORDER BY id DESC")
            # rows = cursor.fetchall()
            # return rows
            
            # --- ถ้ายังไม่มี DB ให้ Return ค่าว่าง หรือ Mock Data ไปก่อนเพื่อไม่ให้ Error ---
            print("Action: Getting drug log...")
            return [
                {
                    "timestamp": "10:30:00",
                    "date": "21/01/2026",
                    "action": "นำเข้า",
                    "slot": "1",
                    "patient": "ทดสอบ",
                    "drug": "Paracetamol",
                    "detail": "500 mg",
                    "status": "สำเร็จ"
                }
            ]
        except Exception as e:
            print(f"Error getting drug log: {e}")
            return []

    def slot(self) -> Dict[str, Any]:
        """Return current slot data as a dict. Suitable to be JSONified by Flask."""
        # Return a shallow copy to avoid accidental modification by callers
        print("Action.slot: returning slot data")
        return dict(self.slot_data)

    def locker_status(self) -> Dict[str, Any]:
        """Return a simple locker status summary based on slots."""
        status = {}
        for key, val in self.slot_data.items():
            # If slot has an hn or drugs, consider it occupied
            occupied = bool(val.get("hn") or (val.get("drugs") and len(val.get("drugs")).__int__() > 0))
            status[key] = "occupied" if occupied else "available"
        print("Action.locker_status: ", status)
        return {"locker_status": status}

    def drug_log(self, request_or_payload) -> Dict[str, Any]:
        """If passed a Flask `request`, handle GET/POST. If passed a dict, treat as payload to append.

        Returns a dictionary with success/data keys.
        """
        # If it's a request-like object
        try:
            # Flask request has get_json and method attributes
            if hasattr(request_or_payload, "method"):
                req = request_or_payload
                if req.method == "GET":
                    return {"success": True, "data": self.insert_table}
                payload = req.get_json(force=True)
            else:
                payload = request_or_payload
        except Exception as e:
            print("Action.drug_log parse error:", e)
            return {"success": False, "error": str(e)}

        entry = {
            "id": len(self.insert_table) + 1,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "entry": payload,
        }
        self.insert_table.append(entry)
        print("Action.drug_log: appended entry", entry)
        return {"success": True, "data": entry}

    def recieved_qr_data(self, new_data: Dict[str, Any], mqtt_client=None) -> str:
        """Process incoming QR data. Optionally publish via mqtt_client if provided.

        Returns a short status string.
        """
        print("Action.recieved_qr_data: received", new_data)
        try:
            # Example: publish to topic 'service_robot/qr'
            if mqtt_client is not None and hasattr(mqtt_client, "publish"):
                topic = os.environ.get("MQTT_QR_TOPIC", "service_robot/qr")
                payload = json.dumps(new_data, ensure_ascii=False)
                mqtt_client.publish(topic, payload)
                print(f"Published QR data to {topic}")
            # Return a simple success message
            return "OK"
        except Exception as e:
            print("Action.recieved_qr_data error:", e)
            return f"ERROR: {e}"

    def in_out(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Record an in/out event. Expects {'status': 'in'|'out', ...}.

        Returns a confirmation dict.
        """
        print("Action.in_out:", data)
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": data,
        }
        self.in_out_log.append(record)
        # Optionally update slot_data if slot is provided
        slot_no = data.get("slot")
        if slot_no:
            key = f"slot{slot_no}"
            if key in self.slot_data:
                if data.get("status") == "in":
                    # mark occupied with provided patient info
                    self.slot_data[key]["hn"] = data.get("hn")
                    self.slot_data[key]["drugs"] = data.get("drugs", [])
                else:
                    # clear slot
                    self.slot_data[key]["hn"] = None
                    self.slot_data[key]["drugs"] = []
        return {"success": True, "record": record}

    def select_slot(self, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle slot selection. Expects {'slot': n} and optional action fields.

        Returns a confirmation dict.
        """
        print("Action.select_slot: received", new_data)
        slot_no = new_data.get("slot")
        if not slot_no:
            return {"success": False, "error": "no slot provided"}

        key = f"slot{slot_no}"
        if key not in self.slot_data:
            return {"success": False, "error": "invalid slot"}

        # Record the selection
        rec = {"slot": slot_no, "meta": new_data}
        self.select_log.append(rec)

        # Optionally mark as selected in slot_data
        self.slot_data[key]["selected"] = True

        return {"success": True, "slot": slot_no}


    def gate(self, locker_state):
        print(f"Action: Gate command received (State: {locker_state}) - [MOCK SUCCESS]")
        # ส่งค่าคืนกลับไปว่า "success" เพื่อให้ api.py หลุดจาก loop while response == "error"
        return "success"


# Create a module-level instance that other modules can import as `action`
action = Action()



