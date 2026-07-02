import customtkinter as ctk
from PIL import Image
from datetime import datetime
from utils.mqtt_handler import MQTTClient  
from utils.topbar_handler import IconHandler  

class Topbar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(width=1280, height=80, corner_radius=0, fg_color="#FFFFFF")
        self.grid_propagate(False)

        print("page: Top bar > init!")

        self.percent_battery = None
        self.icon_handler = IconHandler()
        self.charge_status = "false"
        self.closeApp_stacking= 3
        

        try:
            self.mqtt = MQTTClient()
            try:
                self.mqtt.client.on_message = self.on_message
            except Exception:
                pass
            self.pages = None
            try:
                if getattr(self.mqtt, 'enabled', True):
                    self.mqtt.connect()
                    self.mqtt.start()
            except Exception:
                pass
        except Exception:
            self.mqtt = None
            self.pages = None

        self.robot_status = 100
        self.prv_robot_status = 100
        self.home_flag = False
        self.speaker_level = 0
        self.robot_mapping_status = {
            "0" : "Free State", "1" : "Running State", "2" : "Arrived State",
            "3" : "clear all state", "4" : "Received State", "5" : "Init Map Success",
            "6":  "not Ready init Map First", "8":  "going to charge", "9":  "will discharge",
            "10": "free motor", "11" : "unlock motor", "12" : "resume",
            "98":  "Cannot move", "99" : "Emergency Button State"
        }

        self.load_images()
        self.create_widgets()
        self.update_labels()

    def load_images(self):
        try:
            self.udontani_logo = ctk.CTkImage(
                light_image=Image.open(r"C:\\Service_Robot\\UI\\assets\\main_page\\artron_logo.png"), 
                size=(160, 45)) 
            self.speaker_full_img = ctk.CTkImage(
                light_image=Image.open(r"C:\\Service_Robot\\UI\\assets\\top_bar\\speaker\\speaker_full.png"), size=(30, 30))
            self.speaker_medium_img = ctk.CTkImage(
                light_image=Image.open(r"C:\\Service_Robot\\UI\\assets\\top_bar\\speaker\\speaker_medium.png"), size=(30, 30))
            self.speaker_low_img = ctk.CTkImage(
                light_image=Image.open(r"C:\\Service_Robot\\UI\\assets\\top_bar\\speaker\\speaker_low.png"), size=(30, 30))
            self.battery_img = ctk.CTkImage(
                light_image=Image.open(r"C:\\Service_Robot\\UI\\assets\\top_bar\\battery\\batt100.png"), size=(45, 22))
        except FileNotFoundError as e:
            print(f"Error loading image on topbar: {e}")

    def create_widgets(self):

        date_style = {'font': ("Noto Sans Thai", 18), 'text_color': '#035E5A'}
        date_style_bold = {'font': ("Noto Sans Thai", 18, "bold"), 'text_color': '#035E5A'}
        btn_font = ("Noto Sans Thai", 16, "bold")

        # 1. LOGO (ซ้ายสุด)
        self.logo = ctk.CTkButton(
            master=self,
            text="",
            image=self.udontani_logo,
            hover=False,
            corner_radius=0,
            fg_color="transparent",
            width=160,
            command=self._on_LogoClick
        )
        self.logo.place(relx=0.01, rely=0.5, anchor="w")

        # 2. Date & Time Group (ใช้ Frame จัดกลุ่มกึ่งกลางหน้าจอ 50%)
        self.date_time_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.date_time_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.date_text = ctk.CTkLabel(self.date_time_frame, text="Date :", **date_style_bold)
        self.date_text.pack(side="left", padx=(0, 5))

        self.date = ctk.CTkLabel(self.date_time_frame, text="11-11-2022", **date_style)
        self.date.pack(side="left", padx=(0, 25))

        self.time_text = ctk.CTkLabel(self.date_time_frame, text="Time :", **date_style_bold)
        self.time_text.pack(side="left", padx=(0, 5))

        self.time = ctk.CTkLabel(self.date_time_frame, text="15:11:22", **date_style)
        self.time.pack(side="left")

        # 3. Right Group (Discharge / Home / Speaker / Battery) - ใช้ Frame จัดกลุ่มเพื่อความเสถียรและไม่ซ้อนทับกัน
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.place(relx=0.98, rely=0.5, anchor="e")

        self.chargeAction_btn = ctk.CTkButton(
            self.right_frame, 
            text="Discharge Robot", 
            font=btn_font,
            fg_color="#035E5A",
            width=150,  
            height=35, 
            corner_radius=10,
            command=self.on_discharge
        )
        self.chargeAction_btn.pack(side="left", padx=6)

        self.home_btn = ctk.CTkButton(
            self.right_frame, 
            text="Home",
            font=btn_font,
            fg_color="#035E5A",
            width=90, 
            height=35,
            corner_radius=10,
            command=self._on_home
        )
        self.home_btn.pack(side="left", padx=6)

        # System Icons (Speaker / Battery)
        self.speaker_btn = ctk.CTkButton(
            self.right_frame, 
            text="", 
            bg_color="transparent",
            command=self._on_speaker_click,
            image=self.speaker_full_img,
            width=35, height=35,
            fg_color="transparent",
            hover=False
        )
        self.speaker_btn.pack(side="left", padx=6)

        # Battery Group
        self.battery_ico = ctk.CTkLabel(self.right_frame, image=self.battery_img, text="")
        self.battery_ico.pack(side="left", padx=(6, 4))

        self.battery_lb = ctk.CTkLabel(self.right_frame, text="100%", font=("Noto Sans Thai", 16, "bold"), text_color='#035E5A')
        self.battery_lb.pack(side="left", padx=(0, 6))

        # 5. Window Controls
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0, height=18)
        self.control_frame.place(relx=1.0, rely=0.0, anchor='ne')
        
        # Dragging logic
        self._drag_data = {"x": 0, "y": 0}
        self.bind("<Button-1>", self._start_move)
        self.bind("<B1-Motion>", self._do_move)
        self.logo.bind("<Button-1>", self._start_move)
        self.logo.bind("<B1-Motion>", self._do_move)

    def update_labels(self):
        self.update_datetime()
        self.update_battery_icon()
        self.after(1000, self.update_labels)

    def update_datetime(self):
        """Update the date and time labels."""
        self.date.configure(text=datetime.now().strftime("%d-%m-%Y"))
        self.time.configure(text=datetime.now().strftime("%H:%M:%S"))

    def update_battery_icon(self):
        """Update the battery icon based on the current battery percentage from mqtt."""
        if self.percent_battery is not None:
            icon = self.icon_handler.get_icon(percentage=self.percent_battery, is_charge=self.charge_status)
            self.battery_ico.configure(image=icon)
            self.battery_lb.configure(text = str(self.percent_battery)+"%")

    def on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages."""
        if msg.topic == self.mqtt.topics["battery_status"]:
            try:
                self.percent_battery = int(msg.payload.decode())
                self.update_battery_icon()
            except ValueError:
                print("Invalid battery status received.")

        if msg.topic == self.mqtt.topics["status"]:
            try:
                self.prv_robot_status = self.robot_status
                self.robot_status = int(msg.payload.decode())
                try:
                    print(f"robot status > {self.robot_status} : {self.robot_mapping_status[str(self.robot_status)]}")
                    self.after_dischargeEvent()
                    self._home_event()
                except KeyError:
                    print(f"Invalid Key, this key is not in mapping > {str(self.robot_status)}")
            except ValueError:
                print("Invalid status received.")

        if msg.topic == self.mqtt.topics["charge"]:
            try:
                self.robot_charge_status = msg.payload.decode()
                try:
                    if self.robot_charge_status == "true":
                        self.charge_status = "true"
                        # ถ้าปุ่ม chargeAction_btn ถูก comment ไว้ บรรทัดนี้จะ Error
                        self.chargeAction_btn.configure(text="Discharge", command = self.on_discharge)
                        self.update_battery_icon()
                    else:
                        self.chargeAction_btn.configure(text="Charge", command = self.on_going_charge)
                except KeyError:
                    print(f"Invalid Key, this key is not in mapping > {str(self.robot_charge_status)}")
            except ValueError:
                print("Invalid status received.")

    def on_discharge(self):
        self.home_btn.configure(state = "disabled")
        self.chargeAction_btn.configure(state = "disabled")
        self.mqtt.publish("robot/status", 11)
        self.mqtt.publish("robot/poi", 9)
        self.charge_status = "false"
        self.update_battery_icon()

        self.pages["main_page"].pack_forget()
        self.pages['ongoing_page'].pack(pady = 50)
        self.pages['ongoing_page'].start_animation()

    def on_going_charge(self):
        self.home_btn.configure(state = "disabled")
        self.chargeAction_btn.configure(state = "disabled")
        self.mqtt.publish("robot/poi", 8)
        self.pages["main_page"].pack_forget()
        self.pages['ongoing_page'].pack(pady = 50)
        self.pages['ongoing_page'].start_animation()

    def after_dischargeEvent(self):
        if self.prv_robot_status == 9 and self.robot_status == 0:
            print("Robot leaved charger station")
            print("Robot will go to poi 1 (Stanby location)")
            self.mqtt.publish("robot/poi", 1)

    def _on_home(self):
        print("Topbar > Home clicked")
        self.mqtt.publish("robot/status", 3)
        self.home_flag = True
        self.pages["main_page"].pack_forget()
        self.pages['ongoing_page'].pack(pady = 50)
        self.pages['ongoing_page'].start_animation()
    
    def _home_event(self):
        if self.robot_status == 0 and self.home_flag:
            print("> Robot Going Home POI")
            self.home_flag = False
            self.mqtt.publish("robot/poi", 1)
            self.home_btn.configure(state = "disabled")
            self.chargeAction_btn.configure(state = "disabled")

    def _on_LogoClick(self):
        print("page: Topbar > Artron Button Clicked.")
        self.closeApp_stacking -= 1
        if self.closeApp_stacking == 0:
            if self.mqtt: self.mqtt.stop() 
            # if self.pages and 'barcode_page' in self.pages: 
            #     self.pages['barcode_page'].qr_scanner.disconnect()
            self.parent.master.destroy()
    
    def _on_speaker_click(self):
        self.speaker_level += 1
        if self.speaker_level > 2:
            self.speaker_level = 0

        if self.speaker_level == 0:
            print("Top bar > speaker Low")
            self.speaker_btn.configure(image = self.speaker_low_img)
        elif self.speaker_level == 1:
            print("Top bar > speaker Medium")
            self.speaker_btn.configure(image = self.speaker_medium_img)
        else:
            print("Top bar > speaker Full")
            self.speaker_btn.configure(image = self.speaker_full_img)

    def _on_close(self):
        root = self.winfo_toplevel()
        if self.mqtt: self.mqtt.stop()
        root.destroy()

    def _start_move(self, event):
        root = self.winfo_toplevel()
        self._drag_data['x'] = event.x_root - root.winfo_x()
        self._drag_data['y'] = event.y_root - root.winfo_y()

    def _do_move(self, event):
        root = self.winfo_toplevel()
        root.geometry(f"+{event.x_root - self._drag_data['x']}+{event.y_root - self._drag_data['y']}")