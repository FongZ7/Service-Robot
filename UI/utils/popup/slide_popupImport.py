import customtkinter as ctk
from tkinter import Frame, Canvas
from PIL import Image
import json

class SlidePopupImport(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # คำนวณขนาด popup จากหน้าจอ parent (80% ของความกว้าง, max 380)
        parent.update_idletasks()
        screen_w = parent.winfo_width() or 480
        screen_h = parent.winfo_height() or 320

        self.popup_w = 550
        self.popup_h = 440

        self.configure(
            fg_color="#035E5A",
            corner_radius=25,
            width=self.popup_w,
            height=self.popup_h
        )

        self.grid_propagate(False)

        try:
            self.close_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\barcode_import_page\close.png"), size=(30,30))
        except:
            self.close_img = None

        # ปรับฟอนต์และปุ่มตามสัดส่วนหน้าจอ
        scale = self.popup_w / 400
        btn_w   = max(80,  int(120 * scale))
        btn_h   = max(28,  int(40  * scale))
        btn_r   = int(20 * scale)
        f_text  = max(9,   int(14  * scale))
        f_head  = max(12,  int(16  * scale))
        f_inst  = max(8,   int(11  * scale))
        f_btn   = max(10,  int(13  * scale))

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
        self.text_style        = {'text_color': "#FFFFFF", 'font': ("Noto Sans Thai", 18)}
        self.header_style      = {'text_color': "#FFFFFF", 'font': ("Noto Sans Thai", 24, "bold")}
        self.instruction_style = {'text_color': "#FFFFFF", 'font': ("Noto Sans Thai", 15)}

        self.patientData = {}

        self.x_pos     = 0.5
        self.start_pos = 2.0
        self.end_pos   = 1.0
        self.place(relx=self.x_pos, rely=self.start_pos, anchor="s")

        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        px = 50
        py = 8
        wrap_val = 350

        # หัวข้อ
        ctk.CTkLabel(self, text='ข้อมูลผู้ป่วย', **self.header_style).grid(
            row=0, column=0, columnspan=2, padx=(px, px), pady=(25, 15), sticky="w"
        )

        # ชื่อผู้ป่วย
        ctk.CTkLabel(self, text='ชื่อผู้ป่วย :', **self.text_style).grid(
            row=1, column=0, padx=(px, 10), pady=py, sticky="w"
        )
        self.patientName_lb = ctk.CTkLabel(self, text="-", **self.text_style)
        self.patientName_lb.grid(row=1, column=1, padx=(10, px), pady=py, sticky="w")

        # HN
        ctk.CTkLabel(self, text='HN :', **self.text_style).grid(
            row=2, column=0, padx=(px, 10), pady=py, sticky="w"
        )
        self.patientHN_lb = ctk.CTkLabel(self, text="-", **self.text_style)
        self.patientHN_lb.grid(row=2, column=1, padx=(10, px), pady=py, sticky="w")

        # ชื่อยา
        ctk.CTkLabel(self, text='ชื่อยา :', **self.text_style).grid(
            row=3, column=0, padx=(px, 10), pady=py, sticky="w"
        )
        self.patientDrugs_lb = ctk.CTkLabel(self, text="-", **self.text_style)
        self.patientDrugs_lb.grid(row=3, column=1, padx=(10, px), pady=py, sticky="w")

        # รายละเอียด
        ctk.CTkLabel(self, text='รายละเอียด :', **self.text_style).grid(
            row=4, column=0, padx=(px, 10), pady=py, sticky="w"
        )
        self.patientDetail_lb = ctk.CTkLabel(
            self, text="-", **self.text_style, wraplength=wrap_val, justify="left"
        )
        self.patientDetail_lb.grid(row=4, column=1, padx=(10, px), pady=py, sticky="w")

        # instruction
        self.instruction_lb = ctk.CTkLabel(
            self,
            text='กรุณาตรวจสอบข้อมูลผู้ป่วยเพิ่มยาให้ครบถ้วนและกด "ยืนยัน" เมื่อเพิ่มยาเสร็จเรียบร้อยแล้ว',
            **self.instruction_style,
            wraplength=self.popup_w - 60,
            justify="center"
        )
        self.instruction_lb.grid(row=5, column=0, columnspan=2, padx=px, pady=(15, 10))

        # ปุ่ม
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=6, column=0, columnspan=2, pady=(10, 20), sticky="ew")

        self.btn_inner_frame = ctk.CTkFrame(self.btn_frame, fg_color="transparent")
        self.btn_inner_frame.pack(expand=True)

        self.confirm_btn = ctk.CTkButton(self.btn_inner_frame, **self.button_style, text="ยืนยัน")
        self.confirm_btn.pack(side="left", padx=10)

        self.add_btn = ctk.CTkButton(self.btn_inner_frame, **self.button_style, text="เพิ่มยา")
        self.add_btn.pack(side="left", padx=10)

    def slide_up(self):
        self.lift()
        if self.start_pos > self.end_pos:
            self.start_pos -= 0.08
            self.place(relx=self.x_pos, rely=self.start_pos, anchor="s")
            self.after(10, self.slide_up)
        else:
            self.place(relx=self.x_pos, rely=self.end_pos, anchor="s")

    def slide_down(self):
        if self.start_pos < 2.0:
            self.start_pos += 0.08
            self.place(relx=self.x_pos, rely=self.start_pos, anchor="s")
            self.after(10, self.slide_down)

    def reset_pos(self):
        self.start_pos = 2.0
        self.place(relx=self.x_pos, rely=self.start_pos, anchor="s")

    def config_popupDetail(self, data):
        self.patientData = data
        name   = self.patientData.get('name', '-')
        hn     = self.patientData.get('hn', '-')
        drug   = self.patientData.get('drug', '-')
        detail = str(self.patientData.get('detail', '-'))

        if len(detail) > 30:
            detail = detail[:30] + "..."

        self.patientName_lb.configure(text=name)
        self.patientHN_lb.configure(text=hn)
        self.patientDrugs_lb.configure(text=drug)
        self.patientDetail_lb.configure(text=detail)