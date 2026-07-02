import customtkinter as ctk
from tkinter import Button
from PIL import Image, ImageTk
from utils.table_handler import Table
from utils.button_handler import MyButton
from utils.api_handler import post_api_data, get_api_data

class CheckDrugPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master = parent)
        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF")
        self.slot_id = None
        self.pages= None
        self.open_slot_key = {'status': 1}
        self.load_images()
        self.create_widgets()

    def load_images(self):
        try:
            pil_back = Image.open(r"C:\Service_Robot\UI\assets\check_drug_page\back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)
            
            self.add_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\check_drug_page\add.png"), size=(24,24))
            # Scale Template to 920x470
            self.template_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\check_drug_page\template.png"), size=(920,470))
        except:
            self.back_img = None
            self.add_img = None
            self.template_img = None
    
    def create_widgets(self):
        self.back_btn = Button(
            master=self, text="", image=self.back_img, borderwidth=0,
            background="#FFFFFF", highlightthickness=0, activebackground="#FFFFFF",
            command=lambda: self.back())
        self.back_btn.place(relx=0.00, rely=0.06)

        self.title = ctk.CTkLabel(self, text="ยาที่นำเข้าทั้งหมด", font=("Noto Sans Thai", 24, "bold"), text_color="#035E5A", bg_color="transparent")
        self.title.place(relx=0.10, rely=0.065)

        self.addDrugBtn = ctk.CTkButton(self, text="เพิ่มยา", font=("Noto Sans Thai", 18, "bold"), 
                                        corner_radius=10, width=120, height=40,
                                        bg_color="#FFFFFF", fg_color="#035E5A", text_color="#FFFFFF",
                                        image=self.add_img, compound="left", hover=False,
                                        command=self._on_addDrugBtn_click)
        self.addDrugBtn.place(relx=0.82, rely=0.03)

        self.shadow = ctk.CTkLabel(master=self, image=self.template_img, text=None)
        self.shadow.place(relx=0.5, rely=0.48, anchor="center")

        self.table_frame = Table(master=self, 
                                 width=900, height=450, 
                                 bg_color="#FFFFFF", 
                                 fg_color="#FFFFFF")
        
        self.table_frame.place(relx=0.5, rely=0.48, anchor="center")
    
        self.confirmbtn = MyButton(self)
        self.confirmbtn.configbtn(text="ยืนยัน", command=self._on_confirmBtn_click, x=0.5, y=0.90) 
        
        self.confirmbtn.configure(width=200, height=50, font=("Noto Sans Thai", 18, "bold"), corner_radius=25)
        self.confirmbtn.place(relx=0.5, rely=0.90, anchor="center")


    def _on_addDrugBtn_click(self):
        post_api_data('qr_scan', {
            "qr_number": "900000178291111", 
            "name": "นาง จันเพ็ง ผุกแสน", 
            "drug": "Dophamine", 
            "detail": "drip", 
            "hn": "46608226", 
            "is_return": False,
            "slot_id": self.slot_id
        })
        self.update_table()

    def _on_confirmBtn_click(self):
        self.pack_forget()
        self.pages['import_page'].pack(fill='both', expand=True)
        self.pages['import_page'].on_display()
        post_api_data('gate', self.open_slot_key)

    def update_table(self):
        self.data = get_api_data('slot')
        self.plot_data = self.data[f"slot{self.slot_id}"]
        self.table_frame.update_table(self.plot_data)

    def on_display(self):
        self.after(100, lambda: self.update())

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)

    def back(self):
        print("CheckDrugPage: Back clicked")
        self.pack_forget()
        
        if self.pages and 'barcode_page' in self.pages:
            target_page = self.pages['barcode_page']
            target_page.slot_id = self.slot_id 
            
            target_page.pack(fill='both', expand=True)
            target_page.on_display()
            target_page.start_animation() 
        else:
            print("Error: barcode_page not found in pages")

