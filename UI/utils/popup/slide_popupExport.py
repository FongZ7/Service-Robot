import customtkinter as ctk
from tkinter import Frame, Canvas
from PIL import Image

class SlidePopupExport(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.popup_w = 550
        self.popup_h = 380

        self.configure(
            fg_color="#035E5A", 
            corner_radius=25,
            width=self.popup_w,
            height=self.popup_h
        ) 
        self.grid_propagate(False)

        self.close_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\barcode_import_page\back.png"), size=(30,30))

        self.button_style = {
            'width': 180, 
            'height': 45, 
            'corner_radius': 22, 
            'bg_color': '#035E5A', 
            'fg_color': '#FFFFFF', 
            'text_color': '#035E5A', 
            'font': ("Noto Sans Thai", 18, "bold"), 
            'hover_color': '#F0F0F0'
        }
        self.text_style = {'text_color': "#FFFFFF", 'font': ("Noto Sans Thai", 18)} 

        self.patientName = "วิลเลียม เชคสเปียร์"
        self.patienHN = "123456789"
        
        self.x_pos = 0.5
        self.start_pos = 1.5
        self.end_pos = 0.5 
        self.place(relx=self.x_pos, rely=self.start_pos, anchor="center")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        px = 50
        py = 8

        ctk.CTkLabel(self, text='ข้อมูลผู้ป่วย', text_color="#FFFFFF", font=("Noto Sans Thai", 24, "bold")).grid(
            row=0, column=0, columnspan=2, padx=(px, px), pady=(25, 15), sticky="w"
        )
        ctk.CTkLabel(self, text='ชื่อผู้ป่วย :', **self.text_style).grid(
            row=1, column=0, padx=(px, 10), pady=py, sticky="w"
        )
        ctk.CTkLabel(self, text='HN :', **self.text_style).grid(
            row=2, column=0, padx=(px, 10), pady=py, sticky="w"
        )
        ctk.CTkLabel(self, text='กรุณาตรวจสอบข้อมูลก่อนกด "ยืนยัน"', text_color="#FFFFFF", font=("Noto Sans Thai", 15), justify="center").grid(
            row=3, column=0, columnspan=2, padx=px, pady=(20, 10)
        )

        self.patientName_lb = ctk.CTkLabel(self, text=self.patientName, **self.text_style)
        self.patientName_lb.grid(row=1, column=1, padx=(10, px), pady=py, sticky="w")

        self.patientHN_lb = ctk.CTkLabel(self, text=self.patienHN, **self.text_style)
        self.patientHN_lb.grid(row=2, column=1, padx=(10, px), pady=py, sticky="w")
        
        self.confirm_btn = ctk.CTkButton(self,
                                         **self.button_style,
                                         text="ยืนยัน",
                                         )
        self.confirm_btn.grid(row=4, column=0, columnspan=2, padx=px, pady=(15, 25))
        
    def slide_up(self):
        self.lift()
        if self.start_pos > self.end_pos:
            self.start_pos -= 0.06  
            self.place(relx=self.x_pos, rely=self.start_pos, anchor="center")
            self.after(10, self.slide_up)
        else:
            self.place(relx=self.x_pos, rely=self.end_pos, anchor="center")

    def slide_down(self):
        if self.start_pos < 1.5:
            self.start_pos += 0.06
            self.place(relx=self.x_pos, rely=self.start_pos, anchor="center")
            self.after(10, self.slide_down)

    def reset_pos(self):
        self.start_pos = 1.5
        self.place(relx=self.x_pos, rely=self.start_pos, anchor="center")

    def config_popupDetail(self, data):
        self.patientData = data
        
        self.patientName = self.patientData['name']
        self.patienHN = self.patientData['hn']

        self.patientName_lb.configure(text=self.patientName)
        self.patientHN_lb.configure(text=self.patienHN)