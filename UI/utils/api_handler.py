import requests
from pprint import pprint
from datetime import datetime

USE_MOCK = True  

MOCK_DATABASE = {
    "slot1": {},
    "slot2": {}
}

MOCK_DRUG_LOG = [
    {
        "time": "02-07-2026 11:12:21",
        "name": "นาง จันเพ็ง ผุกแสน",
        "drug": "Dophamine",
        "detail": "drip",
        "status": "นำเข้าสำเร็จ"
    }
]

base_url = "http://127.0.0.1:5000/"

def get_api_data(location):
    if USE_MOCK:
        if location == "slot":
            return MOCK_DATABASE
        elif location == "drug_log":
            return MOCK_DRUG_LOG
        return {}
    # -----------------------------------------------

    url = f"{base_url}/{location}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"API: Error fetching data for {location}: {e}")
        return None

def post_api_data(location, payload):
    if USE_MOCK:
        print(f"API (MOCK): Posting to '{location}' with data: {payload}")
        
        if location == 'qr_scan':
            slot_id = payload.get('slot_id') 
            
            if slot_id:
                key = f"slot{slot_id}" 
                
                # Retrieve existing slot data or initialize a blank one
                existing = MOCK_DATABASE.get(key, {})
                if not isinstance(existing, dict):
                    existing = {}
                
                # Get lists of drugs and details
                drugs = existing.get("drugs")
                if not isinstance(drugs, list):
                    drugs = []
                details = existing.get("detail")
                if not isinstance(details, list):
                    details = []
                
                # Append the new drug and detail
                new_drug = payload.get('drug', '-')
                new_detail = payload.get('detail', '-')
                
                drugs.append(new_drug)
                details.append(new_detail)
                
                # Parse patient name
                full_name = payload.get('name', 'นาง จันเพ็ง ผุกแสน')
                first_name = ''
                last_name = ''
                if full_name:
                    parts = full_name.split()
                    first_name = parts[0] if parts else ''
                    last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
                
                MOCK_DATABASE[key] = {
                    "name": {"first": first_name, "last": last_name},
                    "hn": payload.get('hn', '46608226'),
                    "drugs": drugs,
                    "detail": details,
                    "status": "occupied",
                    "IsReturn": payload.get("is_return", False),
                    "WhyReturn": payload.get("why_return", None),
                    "location": payload.get("location", "LM49"),
                    "bed_number": payload.get("bed_number", "XX")
                }
                
                # Add to MOCK_DRUG_LOG as well
                current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                MOCK_DRUG_LOG.append({
                    "time": current_time,
                    "name": full_name,
                    "drug": new_drug,
                    "detail": new_detail,
                    "status": "นำเข้าสำเร็จ"
                })
                
                print(f"API (MOCK): Saved data to {key} successfully!")
                return {"success": True, "data": MOCK_DATABASE[key]}
            else:
                return {"success": False, "error": "No slot_id provided"}

        elif location == 'gate':
             return {"success": True, "message": "Gate command received (Mock)"}

        return {"success": True, "data": payload}
    # -----------------------------------------------

    url = f"{base_url}/{location}"
    try:
        response = requests.post(url, json=payload, timeout=10)  # Add a timeout
        response.raise_for_status()  # Raise an exception for HTTP error responses
        return {"success": True, "data": response.json()}
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (like 500, 404)
        return {"success": False, "error": f"HTTPError: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        # Handle non-HTTP exceptions (e.g., timeout, connection error)
        return {"success": False, "error": str(e)}

def slot_detail():
    slot = get_api_data("slot")
    return slot