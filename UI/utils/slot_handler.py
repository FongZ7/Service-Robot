import customtkinter as ctk
from PIL import Image

class TheSlot(ctk.CTkButton):
    def __init__(self, master, slot_id, branch, slotData):
        super().__init__(master)
        self.load_image()
        self.slotID = slot_id
        self.branch = branch
        self.master = master
        self.slotData = slotData

        self.Isblank = True
        self.IsrequestAPIfail = False
        self.config_parameter()

        # Enlarge Slot to 380x260 for 1280x800 screen
        self.configure(
            width=380,
            height=260,
            corner_radius=15,
            fg_color="#F4F4F4",
            hover=False,
            text = " " + "\n",
            font=("Noto Sans Thai", 18),
            anchor="CENTER",
            image=self.blank_img,
            command= lambda: print(f"User Click {slot_id} as blankSlot"),
        )

        # Enlarge bed number button
        self.bedNo_btn = ctk.CTkButton(
            master=self,
            width=380,
            height=55,
            hover=False,
            corner_radius=10,
            text="ช่องว่าง", 
            text_color="#FFFFFF", 
            fg_color="#035E5A",
            font=("Noto Sans Thai", 18, "bold"),
            anchor="center",
            command= lambda: print(f"User Click {slot_id} as blankSlot"),
        ) 
        self.bedNo_btn.place(x=0, y=0) 

    def load_image(self):
        # Enlarge image size for 1280x800 display
        self.blank_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\slot_page\blank_box.png"), size=(120, 140))
        
        self.male_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\slot_page\male.png"), size=(36, 36))
        self.female_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\slot_page\female.png"), size=(36, 36))
        self.maleReturn_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\slot_page\male_return.png"), size=(70, 36))
        self.femaleReturn_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\slot_page\female_return.png"), size=(70, 36))
        self.error_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\slot_page\error.png"), size=(24, 160))
    
    def set_slot(self):
        self.config_parameter()
        if (not self.firstName) and (not self.lastName):
            self.Isblank = True
            self._set_blank_slot()
        else:
            self.Isblank = False
            self._set_fill_slot()

    def _set_blank_slot(self):
        self.configure(
            width=380,
            height=260,
            corner_radius=15,
            fg_color="#F4F4F4",
            hover_color = "#67A7A4",
            text = " " + "\n",
            compound = "left",
            anchor="CENTER",
            image=self.blank_img,
        )
        self.bedNo_btn.configure(
            width=380,
            height=55,
            corner_radius=10,
            text="ช่องว่าง", 
            text_color="#FFFFFF", 
            hover_color = "#67A7A4",
            fg_color="#035E5A",
            font=("Noto Sans Thai", 18, "bold"),
        ) 

    def _set_fill_slot(self):
        self.configure(
            width=380,
            height=260,
            corner_radius=15,
            fg_color="#F4F4F4",
            hover=True,
            hover_color = "#67A7A4",
            text = " "+ "\n" + str(self.firstName) + " " + str(self.lastName) + "\n" + "HN: " + str(self.HN) + "\n" + "มียา " + str(len(self.drugs)) + " ชนิด", 
            font = ("Noto Sans Thai", 18),
            text_color="#000000",
            image= self._fillSlot_setimg(),
            anchor = 'CENTER',
            compound="bottom",
        )

        self.bedNo_btn.configure(
            width=380,
            height=55,
            text="เตียง " + str(self.bedNo), 
            text_color="#FFFFFF", 
            fg_color= self._fillSlot_setbedStyle(),
            hover_color = "#67A7A4",
            font=("Noto Sans Thai", 20, "bold"),
            anchor="center",
        ) 

    # ... (ส่วน _fillSlot_setimg, _fillSlot_setbedStyle, config_parameter เหมือนเดิม) ...
    def _fillSlot_setimg(self):
        if self.gender == "male" and not self.IsReturn:
            return self.male_img
        elif self.gender == "male" and self.IsReturn:
            return self.maleReturn_img
        elif self.gender == "female" and not self.IsReturn:
            return self.female_img
        elif self.gender == "female" and self.IsReturn:
            return self.femaleReturn_img
    
    def _fillSlot_setbedStyle(self):
        self.fg_color_map = {
            "LM42": "#C6000C", 
            "LM26": "#0E17DF", 
            "LM48": "#FF63AE", 
            "LM49": "#04A5FF", 
            "LM11": "#18E60D", 
        }
        self.fg_color = self.fg_color_map.get(self.location, "#000000")
        return self.fg_color

    def config_parameter(self):
        try:
            sd = self.slotData or {}
            if isinstance(sd, list) and len(sd) > 0 and isinstance(sd[0], dict):
                sd = sd[0]

            def _get(*keys, default=None):
                for k in keys:
                    if isinstance(sd, dict) and k in sd:
                        return sd[k]
                return default

            name_val = _get('name', 'Name', default={})
            first = ''
            last = ''
            if isinstance(name_val, dict):
                first = name_val.get('first') or name_val.get('name') or ''
                last = name_val.get('last') or name_val.get('surname') or ''
            elif isinstance(name_val, str):
                parts = name_val.split()
                first = parts[0] if parts else ''
                last = ' '.join(parts[1:]) if len(parts) > 1 else ''

            self.firstName = first
            self.lastName = last

            self.HN = _get('hn', 'HN', default=None)
            self.gender = _get('gender', default=None)
            self.bedNo = _get('bed_number', 'bedNumber', 'bedNo', default=None)

            drugs = _get('drugs', 'drug_name', default=[])
            if drugs is None:
                drugs = []
            self.drugs = drugs

            self.timestamp = _get('timestamp', 'timeStamp', default=None)
            self.location = _get('location', 'Location', default=None)
            self.IsReturn = _get('IsReturn', default=False)
            self.whyReturn = _get('WhyReturn', default=None)

        except Exception as e:
            print(f"handler: slot handler > An error occurred while parsing slotData: {e}")
            self.firstName = ""
            self.lastName = ""
            self.HN = None
            self.gender = None
            self.bedNo = None
            self.drugs = []
            self.timestamp = None
            self.location = None
            self.IsReturn = False
            self.whyReturn = None