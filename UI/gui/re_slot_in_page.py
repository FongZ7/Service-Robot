import customtkinter as ctk
from PIL import Image, ImageTk 
from tkinter import Frame, Button 
from utils.slot_handler import TheSlot
from utils.mockup_data import mockup_data
from utils.popup_handler import PopupDrugReturn
from utils.api_handler import get_api_data, post_api_data
from utils.popup.general_popup import GeneralPopup
from utils.popup.slot_on_problem import SlotOnProblemPopup

class ReSlotInPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        print("page: ReSlot page > init!")
        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF")
        
        self.branch = "in"
        self.pages = None
        self.slots = []

        self.slot_key = {"slot": 1}
        self.takeout_key = {"status": "takeout"}
        self.opengate_key = {"status": 1}
        self.closegate_key = {"status": 0}

        self.load_images()
        self.get_apidata()
        self.create_widgets()
        
    def load_images(self):
        try:        
            pil_back = Image.open("C:/Service_Robot/UI/assets/slot_page/back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)

            self.ward_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/slot_page/wardList.png"), size=(860, 110)) 
            
            self.popup_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/slot_page/popup.png"), size=(400, 158))
            self.notifytakeout_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/slot_page/notifyTakeout.png"), size=(300, 170))
        except Exception as e:
            print(f"Error loading images: {e}")
            self.back_img = None
            self.ward_img = None
    
    def create_widgets(self):

        self.back_btn = Button(
            master=self, 
            text="", 
            image=self.back_img, 
            borderwidth=0,
            background="#FFFFFF",
            highlightthickness=0,
            activebackground="#FFFFFF", 
            command=self.back
        )
        self.back_btn.place(relx=0.00, rely=0.06)

        self.title = ctk.CTkLabel(
            self, 
            text="ตรวจสอบการนำยาเข้า", 
            font=("Noto Sans Thai", 24, "bold"), 
            text_color="#035E5A",
            bg_color="transparent"
        )
        self.title.place(relx=0.10, rely=0.065) 

        self.freeSlot = ctk.CTkLabel(
            self,
            text=f"ช่องว่าง {self._count_blank_slots()} ช่อง",
            font=("Noto Sans Thai", 24, "bold"),
            text_color='#035E5A',
            bg_color="transparent"
        )      
        self.freeSlot.place(relx=0.95, rely=0.07, anchor="ne")


        self.slotFrame = Frame(self, background="#FFFFFF")
        self.slotFrame.place(relx=0.5, rely=0.47, anchor="center")

        self.row_1 = Frame(self.slotFrame, background="#FFFFFF")
        self.row_1.pack()

        for i in range(1, 3):
            slot_data = self.plot_data.get(f'slot{i}', {})
            slot = TheSlot(master=self.row_1, slot_id=i, branch=self.branch, slotData=slot_data)

            slot.pack(side='left', padx=40, pady=20)
            self.slots.append(slot)


        if self.ward_img:
            self.legend_label = ctk.CTkLabel(
                self, 
                text="", 
                image=self.ward_img,
                bg_color="transparent"
            )

            self.legend_label.place(relx=0.5, rely=0.98, anchor="s")

    def set_Slot(self):
        self.get_apidata()  
        self.freeSlot.configure(text=f"ช่องว่าง {self._count_blank_slots()} ช่อง")

        for i, slot in enumerate(self.slots, start=1):
            if f'slot{i}' in self.plot_data:
                slot.slotData = self.plot_data[f'slot{i}']
                slot.config_parameter()
                slot.set_slot()
                
                if slot.Isblank:
                    try:
                        slot.bedNo_btn.configure(state='disabled')
                        slot.configure(state='disabled')
                    except: pass
                else:
                    try:
                        slot.bedNo_btn.configure(command=lambda i=i: self.goto_reCheckDrugpage(slotID=i))
                        slot.configure(command=lambda i=i: self.goto_reCheckDrugpage(slotID=i))
                    except: pass
            
    def get_apidata(self):
        try:
            self.plot_data = get_api_data('slot')
            if self.plot_data is None:
                print("Warning: Received no data. Using dummy.")
                self.plot_data = {} 
                for i in range(1, 3):
                    self.plot_data[f'slot{i}'] = {
                        'bed_number': None, 'drugs': [], 'gender': None, 'hn': None,
                        'location': None, 'name': {'first': None, 'last': None},
                        'slot_id': i, 'timestamp': None
                    }     
        except Exception as e:
            print(f"Error in get_apidata: {e}")
            self.plot_data = {}

    def goto_reCheckDrugpage(self, slotID):
        print("page: reSlot page > goto reCheckDrug page")
        self.pack_forget()
        self.pages['recheckdrug_page'].slot_id = slotID
        self.pages['recheckdrug_page'].on_display()

    def notify_fill(self):
        self.used_popup = GeneralPopup(self.master)
        self.used_popup.set_used_popup()

    def notify_cant_fill(self):
        self.cant_used_popup = GeneralPopup(self.master)
        self.cant_used_popup.set_cant_used_popup()

    def _count_blank_slots(self):
        blank_slots = 0
        if not self.plot_data: return 0
        for i in range(1, 3):
            key = f'slot{i}'
            if key in self.plot_data:
                slot = self.plot_data[key]
                if (
                    slot.get('bed_number') is None and
                    not slot.get('drugs') and
                    slot.get('gender') is None and
                    slot.get('hn') is None
                ):
                    blank_slots += 1
        return blank_slots
    
    def on_display(self):
        self.pack(fill='both', expand=True)
        self.set_Slot()
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)
    
    def back(self):
        print("page: reSlot_in_page > back to main page")
        self.pack_forget()
        self.pages['main_page'].on_display()