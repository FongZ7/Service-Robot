
#slot page   // GET
slot = {
    "chnn1" : 1,
    "chnn2" : 0,
    "chnn3" : 0,
    "chnn4" : 0,
    "chnn5" : 0,
    "chnn6" : 0,
    "chnn7" : 0,
    "chnn8" : 0,
    # 0 = Unavilable slot   
    # 1 = Avilable slot   
}

#pop up detail  , #drug page // GET, "Slot" sort by List ID
patient = [
        #slot1
        [{"name": {"name": "วิลเลียม", "surname": "เชคสเปียร์"}, 
          "hn": 123456, 
          "gender": "male",
          "bedNumber": 101,
          "drug_name": ["Paracetamol", "Aspirin", "Antibiotic"],
          "timeStamp": "27/04/2024", 
          "Location": "งานจ่ายยาผู้ป่วยใน IPD", 
          "slotId": 1}],

        #slot2
        [{"name": {"name": "โยฮันน์ ", "surname": " เกอเธ่"}, 
          "hn": 789012, 
          "gender": "female",
          "bedNumber": 205,
          "drug_name": ["Insulin", "Painkiller", "Antibiotic"],
          "timeStamp": "27/04/2024", 
          "Location": "หอผู้ป่วยวิกฤติ", 
          "slotId": 2}],
        #slot3
        [{"name": {"name": "วิคเตอร์", "surname": "ฮูโก"}, 
          "hn": 345678, 
          "gender": "female",
          "bedNumber": 309,
          "drug_name": ["Antacid", "Antihistamine", "Vitamin"],
          "timeStamp": "27/04/2024", 
          "Location": "หอผู้ป่วยศัลยกรรมและรังสีรักษา", 
          "slotId": 3}],
        #slot4
        [{"name": {"name": "เลโอ", "surname": "ตอลสตอย"}, 
          "hn": 901234,
          "gender": "male", 
          "bedNumber": 413,
          "drug_name": ["Antibiotic", "Antiviral", "Painkiller", "Antifungal"],
          "timeStamp": "27/04/2024", 
          "Location": "งานโภชนศาสตร์", 
          "slotId": 4}],
        #slot5
        [{"name": {"name": "ฟีโอดอร์", "surname": "ดอสโตเยฟสกี้ "}, 
          "hn": 567890, 
          "gender": "female",
          "bedNumber": 517,
          "drug_name": ["Antibiotic", "Antifungal"],
          "timeStamp": "27/04/2024", 
          "Location": "หอผู้ป่วยอายุรกรรม", 
          "slotId": 5}],
        #slot6
        [{"name": {"name": "ฟรันซ์", "surname": "คาฟคา"}, 
          "hn": 234567, 
          "gender": "male",
          "bedNumber": 621,
          "drug_name": ["Antibiotic", "Antiviral", "Vitamin", "Antihistamine"],
          "timeStamp": "27/04/2024", 
          "Location": "งานจ่ายยาผู้ป่วยใน IPD", 
          "slotId": 6}],
        #slot7
        [{"name": {"name": "ชาลส์", "surname": "ดิกคินส์"}, 
          "hn": 890123,
          "gender": "female", 
          "bedNumber": 725,
          "drug_name": ["Antihistamine", "Antacid"],
          "timeStamp": "27/04/2024", 
          "Location": "หอผู้ป่วยไอโอดีนรังสี", 
          "slotId": 7}],
        #slot8
        [{"name": {"name": "เจน", "surname": "ออสเตน"}, 
          "hn": 456789, 
          "gender": "male",
          "bedNumber": 829,
          "drug_name": ["Antibiotic", "Antiviral"],
          "timeStamp": "27/04/2024", 
          "Location": "หอผู้ป่วยวิกฤติ",
          "slotId": 8}]
    
]


patients2 = {
    "slot1": [
        {
            "name": {
                "first": "วิลเลียม",
                "last": "เชคสเปียร์"
            },
            "hn": 123456,
            "gender": "male",
            "bed_number": 101,
            "drugs": ["Paracetamol", "Aspirin", "Antibiotic"],
            "timestamp": "27/04/2024",
            "location": "งานจ่ายยาผู้ป่วยใน IPD",
            "locationID" : 1,
            "slot_id": 1,
            "IsReturn": False,
            "WhyReturn": None,
            
        }
    ],
    "slot2": [
        {
            "name": {
                "first": "โยฮันน์",
                "last": "เกอเธ่"
            },
            "hn": 789012,
            "gender": "male",
            "bed_number": 205,
            "drugs": ["Insulin", "Painkiller", "Antibiotic"],
            "timestamp": "27/04/2024",
            "location": "หอผู้ป่วยวิกฤติ",
            "slot_id": 2,
            "IsReturn": False,
            "WhyReturn": None,
        }
    ],
    
    "slot3": [],
    "slot4": [
        {
            "name": {
                "first": "มารี",
                "last": "กูรี"
            },
            "hn": 901234,
            "gender": "female",
            "bed_number": 404,
            "drugs": ["Chemotherapy", "Painkiller"],
            "timestamp": "27/04/2024",
            "location": "หอผู้ป่วยวิกฤติ",
            "slot_id": 4,
            "IsReturn": True,
            "WhyReturn": "ยาไม่ถูกต้อง",
        }
    ],
    "slot5": [
        {
            "name": {
                "first": "อัลเบิร์ต",
                "last": "ไอน์สไตน์"
            },
            "hn": 567890,
            "gender": "male",
            "bed_number": 505,
            "drugs": ["Blood Pressure Medication", "Antibiotic"],
            "timestamp": "27/04/2024",
            "location": "หอผู้ป่วยอายุรกรรม",
            "slot_id": 5,
            "IsReturn": False,
            "WhyReturn": None,
        }
    ],
    "slot6": [
        {
            "name": {
                "first": "ไอแซก",
                "last": "นิวตัน"
            },
            "hn": 112233,
            "gender": "male",
            "bed_number": 606,
            "drugs": ["Painkiller", "Antibiotic"],
            "timestamp": "27/04/2024",
            "location": "หอผู้ป่วยศัลยกรรมและรังสีรักษา",
            "slot_id": 6,
            "IsReturn": True,
            "WhyReturn": "ยาไม่ถูกต้อง",
        }
    ],
    "slot7": [
        {
            "name": {
                "first": "เลโอนาร์โด",
                "last": "ดาวินชี"
            },
            "hn": 445566,
            "gender": "male",
            "bed_number": 707,
            "drugs": ["Diabetes Medication", "Antibiotic"],
            "timestamp": "27/04/2024",
            "location": "หอผู้ป่วยไอโอดีนรังสี",
            "slot_id": 7,
            "IsReturn": True,
            "WhyReturn": "ส่งผิดแผนก",
        }
    ],
    "slot8": [],
    "current_poi" : "POI",
}

barcode_scan = {
    "name": "นาย สมชาย ใจดี",
    "hn":11111111,
    "drug_name": "Paracetamol",
    "detail": "ยาลดไข้",
}


insert_table = [
    {
        "ลำดับ": 1,
        "รหัสยา": "A123456",
        "ชื่อยา": "Fluorouracil",
        "รายละเอียด": "ดูด Fluorouracil 1g/20 mL inj (ID-Fluorouracil) (x1) (858 mg/17.7 ml) + NSS 0.9% 1000ml IV dripin 22 hour Syringe (30) mL Day : 2 ขวดที่ 3 (ตัวอย่าง)"
    },
    {
        "ลำดับ": 2,
        "รหัสยา": "B789101",
        "ชื่อยา": "Ciprofloxacin",
        "รายละเอียด": "500 mg oral tablet, to be taken twice daily with water. Ensure hydration is maintained."
    },
    {
        "ลำดับ": 3,
        "รหัสยา": "C112131",
        "ชื่อยา": "Amoxicillin",
        "รายละเอียด": "250 mg/5 mL suspension, take 5 mL three times a day after meals for 7 days."
    }
]







#GET
top_bar_status_batt = {
    "status_batt" : 100,
        # % battery range 0-100
        # charge = 1000
        }
#PUT
top_bar_speaker_level =  {"status_speaker" : 100,
        #% 100,50,20,0
        # mute = 0
}

#GET
top_bar_wifi =  {"status_wifi" : 100,
        # disconnect = False
        # connected = true
}


#checkpoint

#GET
location =  {
    "location1" : "ห้องฉุกเฉิน",
    "location2" : "หอผู้ป่วยใน",  
    "location3" : "หอผู้ป่วยนอก",
    "location4" : "ห้อง ICU",
    # "location5" : "Radiology Department",
}


def mockup_data(selector):
    if selector == 0:
        return patients2
    if selector == 1:
        return barcode_scan
    if selector == 2:
        return insert_table
    # if selector == 2:
    #     return top_bar_detail
    

#UI   // PUT
Current_page = {
    "page" : "current page"
}





data = {
"slot1": {
"name": {
"first": "เสกสรร",
"last": "ราชสาร"
},
"hn": 46611548,
"gender": "male",
"bed_number": 9,
"drugs": [
"ID-Fluorouracil"
],
"timestamp": "27/11/2024",
"location": "S049",
"slot_id": 1,
"IsReturn": False,
"WhyReturn": None
},
"slot2": {
"name": {
"first": "สำราญ",
"last": "บานใจ"
},
"hn": 46611548,
"gender": "male",
"bed_number": 2,
"drugs": [
"ID-Fluorouracil"
],
"timestamp": "27/11/2024",
"location": "S049",
"slot_id": 2,
"IsReturn": False,
"WhyReturn": None
},
"slot3": {
"name": {
"first": "สุขใจ",
"last": "สบายดี"
},
"hn": 46611548,
"gender": "female",
"bed_number": 3,
"drugs": [
"ID-Fluorouracil"
],
"timestamp": "27/11/2024",
"location": "S049",
"slot_id": 3,
"IsReturn": False,
"WhyReturn": None
},
"slot4": {
"name": {
"first": None,
"last": None
},
"hn": None,
"gender": None,
"bed_number": None,
"drugs": [],
"drugs_detail": [],
"timestamp": None,
"location": None,
"slot_id": None,
"IsReturn": False,
"WhyReturn": None
},
"slot5": {
"name": {
"first": None,
"last": None
},
"hn": None,
"gender": None,
"bed_number": None,
"drugs": [],
"timestamp": None,
"location": None,
"slot_id": None,
"IsReturn": False,
"WhyReturn": None
},
"slot6": {
"name": {
"first": None,
"last": None
},
"hn": None,
"gender": None,
"bed_number": None,
"drugs": [],
"timestamp": None,
"location": None,
"slot_id": None,
"IsReturn": False,
"WhyReturn": None
},
"slot7": {
"name": {
"first": None,
"last": None
},
"hn": None,
"gender": None,
"bed_number": None,
"drugs": [],
"timestamp": None,
"location": None,
"slot_id": None,
"IsReturn": False,
"WhyReturn": None
},
"slot8": {
"name": {
"first": None,
"last": None
},
"hn": None,
"gender": None,
"bed_number": None,
"drugs": [],
"timestamp": None,
"location": None,
"slot_id": None,
"IsReturn": False,
"WhyReturn": None
}
}