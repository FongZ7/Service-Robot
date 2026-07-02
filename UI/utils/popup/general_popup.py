import customtkinter as ctk
from tkinter import Frame, Canvas
from PIL import Image, ImageTk
import os

class GeneralPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="#FFFFFF", bg_color="#FFFFFF", corner_radius=10)
        self.wm_overrideredirect(True)

        # Enlarge Popup to 500x300 for 1280x800 display
        popup_width = 500
        popup_height = 300

        # 2. คำนวณหาจุดกึ่งกลางหน้าต่างหลัก (Parent) อย่างแม่นยำ
        try:
            root = parent.winfo_toplevel()
            root.update_idletasks() # อัปเดตเพื่อให้ได้ค่าตำแหน่งล่าสุดจริง
            
            # หาตำแหน่งและขนาดของหน้าต่างหลัก
            root_w = root.winfo_width()
            root_h = root.winfo_height()
            root_x = root.winfo_rootx()
            root_y = root.winfo_rooty()

            x_pos = root_x + (root_w - popup_width) // 2
            y_pos = root_y + (root_h - popup_height) // 2

        except:
            # ค่าเริ่มต้นกรณีหาตำแหน่งไม่ได้
            x_pos = (1280 - popup_width) // 2
            y_pos = (800 - popup_height) // 2

        # สูตรคำนวณกึ่งกลาง: (ตำแหน่ง X แม่ + ครึ่งหนึ่งของความกว้างแม่) - ครึ่งหนึ่งของความกว้าง Popup


        self.geometry(f"{popup_width}x{popup_height}+{x_pos}+{y_pos}") 
        self.resizable(False, False)
        
        self.load_images()
        self.create_widgets()
        
        self.lift()
        self.wm_transient(parent)

    def load_images(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(current_dir))
        image_dir = os.path.join(base_dir, "assets", "popup")

        try:
            # Enlarge popup images
            img_w, img_h = 460, 75 
            
            self.used_patient_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_dir, "added.png")), size=(img_w, img_h))
            self.already_added_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_dir, "used.png")), size=(img_w, img_h))
            self.no_used_patient_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_dir, "noused.png")), size=(img_w, img_h))

            self.not_found_patient_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_dir, "patientNotFound.png")), size=(img_w, img_h))
            self.problem_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_dir, "problem.png")), size=(img_w, img_h))
            self.api_error_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_dir, "api_error.png")), size=(img_w, img_h))
        except FileNotFoundError as e:
            print(f"Error loading images: {e}")
            pass

    def create_widgets(self):
        # Header Frame
        self.header_frame = Frame(self, background="#FFFFFF")
        self.header_frame.pack(pady=10)

        # Content Frame
        self.content_frame = ctk.CTkFrame(self, bg_color="#FFFFFF", fg_color="#F4F4F4", corner_radius=15)
        self.content_frame.pack(pady=5, fill='x', padx=25) # ลด padding ด้านข้าง

        # Header Image
        header_img = self.already_added_img if hasattr(self, 'already_added_img') else None
        
        self.header_image = ctk.CTkLabel(self.header_frame, 
                    image=header_img,
                    text="Popup" if header_img is None else "",
                    fg_color="#FFFFFF",
                    bg_color="transparent"
                     )
        self.header_image.pack(padx=5, pady=5) # ลด padding

        # Message Label
        self.user_msg = ctk.CTkLabel(self.content_frame, 
                     text="กรุณาตรวจสอบข้อมูล", 
                     text_color="#035E5A",
                     font=('Prompt', 20, 'bold'), # ลดขนาดฟอนต์ลงเหลือ 14
                     )
        self.user_msg.pack(padx=15, pady=12) # ลด padding
        
        # Button Frame
        self.button_frame = Frame(self, background="#FFFFFF")
        self.button_frame.pack(pady=12)

        # Enlarge buttons
        btn_width = 160
        btn_height = 45
        btn_font = ('Prompt', 16, 'bold')

        self.returnMainBtn = ctk.CTkButton(self.button_frame,
                                           text="กลับหน้าหลัก",
                                           text_color="#FFFFFF",
                                           bg_color="#FFFFFF",
                                           fg_color="#035E5A",
                                           hover=False,
                                           corner_radius=22,
                                           width=btn_width,
                                           height=btn_height,
                                           font=btn_font,
                                           command=self.on_ReturnClick
                                           )
        
        self.rescanBtn = ctk.CTkButton(self.button_frame,
                                           text="ลองใหม่",
                                           text_color="#FFFFFF",
                                           bg_color="#FFFFFF",
                                           fg_color="#035E5A",
                                           hover=False,
                                           corner_radius=22,
                                           width=btn_width,
                                           height=btn_height,
                                           font=btn_font,
                                           command=self.on_RescanClick
                                           )

        self.returnMainBtn.pack(side='left', padx=5)    
        self.rescanBtn.pack(side='right', padx=5)  
    
    def on_ReturnClick(self):
        print("page: popup > Goto Main page clicked")
        self.destroy()
        
    def on_RescanClick(self):
        print("page: popup > Rescan clicked")
        self.destroy()

    def on_confirmClick(self):
        print("page: popup > Confirm clicked")
        self.destroy()

    def set_used_popup(self):
        self.rescanBtn.pack_forget()
        if hasattr(self, 'used_patient_img'): self.header_image.configure(image=self.used_patient_img)
        self.user_msg.configure(text="กรุณาเลือกช่องว่าง")
        self.returnMainBtn.configure(text="ตกลง", command=self.on_confirmClick)
        self.returnMainBtn.pack_forget()
        self.returnMainBtn.pack(anchor="center")

    def set_problem_slot_popup(self):
        self.rescanBtn.pack_forget()
        if hasattr(self, 'problem_img'): self.header_image.configure(image=self.problem_img)
        self.user_msg.configure(text="นำยาออกเรียบร้อย")
        self.returnMainBtn.configure(text="ตกลง", command=self.on_confirmClick)
        self.returnMainBtn.pack_forget()
        self.returnMainBtn.pack(anchor="center")

    def set_cant_used_popup(self):
        self.rescanBtn.pack_forget()
        if hasattr(self, 'no_used_patient_img'): self.header_image.configure(image=self.no_used_patient_img)
        self.user_msg.configure(text="เลือกช่องที่มีอยู่")
        self.returnMainBtn.configure(text="ตกลง", command=self.on_confirmClick)
        self.returnMainBtn.pack_forget()
        self.returnMainBtn.pack(anchor="center")

    def set_api_error_popup(self):
        if hasattr(self, 'api_error_img'): self.header_image.configure(image=self.api_error_img)
        self.returnMainBtn.pack_forget()
        self.user_msg.configure(text="เช็ค QR-Code")
       
    def scan_fail_popup(self):
        pass