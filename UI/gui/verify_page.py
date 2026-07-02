import customtkinter as ctk
from tkinter import Frame, Button, PhotoImage
from datetime import datetime
import os
from PIL import Image, ImageTk
from tkinter import Frame, Button 

class VerifyPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        print("page: Verify page > init!")
        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF")
        self.branch = "in"
        self.pages = None
        self.font_styte = {'font': ("Noto Sans Thai", 22, "bold"), 'text_color': '#035E5A'}
        
        self.load_images()
        self.create_widgets()

    def load_images(self):
        try:
            pil_back = Image.open(r"C:\Service_Robot\UI\assets\verify_page\back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)
            self.user_icon = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\verify_page\photo_icons.png"), size=(250, 250))
        except Exception as e:
            print(f"Error loading images: {e}")
            self.back_img = None
            self.user_icon = None
            
    def create_widgets(self):
        # Back Button
        self.back_btn = Button(
            master=self,
            text="",
            image=self.back_img,
            borderwidth=0,
            background="#FFFFFF",
            highlightthickness=0,
            activebackground="#FFFFFF",
            command=lambda: self.backBtn_Onclick()
        )
        self.back_btn.place(relx=0.00, rely=0.04)

        # Centered Container Frame
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Icon Label
        self.icon_label = ctk.CTkLabel(self.container, text="", image=self.user_icon)
        self.icon_label.pack(anchor='center', pady=(0, 25))

        # Verify Button
        self.verify_btn = ctk.CTkButton(
            master=self.container, 
            text="ยืนยันตัวตน", 
            text_color="#FFFFFF",
            font=("Noto Sans Thai", 22, "bold"),
            fg_color="#035E5A",
            width=300,
            height=60,
            corner_radius=30,
            hover_color="#67A7A4",
            command=lambda: self.confirm_verify()
        )
        self.verify_btn.pack(pady=10)

        self.notify_text = ctk.CTkLabel(self.container, text="กรุณากดปุ่มเพื่อยืนยันการทำรายการ", **self.font_styte)
        self.notify_text.pack(pady=10)

    def confirm_verify(self):

        self.save_dummy_record()
        self.goto_slotpage()

    def save_dummy_record(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rec_location = "record_in" if self.branch == "in" else "record_out"
        base_path = f"C:/Users/FongZ/Documents/Robot_Udon_New-User-Interface/UI/{rec_location}"
        
        if not os.path.exists(base_path):
            try: os.makedirs(base_path)
            except: pass
            
        print(f"Verify Logged: {timestamp}")

    def set_branch(self, branch):
        self.branch = branch

    def goto_slotpage(self):
        print("page: Verify page > Goto slot page")
        self.pack_forget()
        try:
            self.pages['slot_page'].set_branch(self.branch)
            self.pages['slot_page'].pack(fill='both')
            self.pages['slot_page'].set_Slot()
            self.pages['slot_page'].on_display()
        except Exception as e:
            print(f"Error transition: {e}")

    def backBtn_Onclick(self):
        self.stop_camera()
        self.pack_forget()
        print("page: Verify page > Back to Main page")
        self.pages['main_page'].on_display()

    def stop_camera(self):
        pass 

    def on_display(self):
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)

    def _on_both_cam_fail(self):
        self.stop_camera()
        self.goto_slotpage()

    def _on_user_msg(self):
        if self.Iscam1_fail and not self.Iscam2_fail:
            self.notify_text.configure(text = "ไม่สามารถใช้งานกล้อง 1 ได้ \n ถ่ายรูปด้วยกล้อง 2", **self.font_styte) 
        elif not self.Iscam1_fail and self.Iscam2_fail:
            self.notify_text.configure(text = "ไม่สามารถอ่านกล้องใช้งานกล้อง 2 ได้ \n ถ่ายรูปด้วยกล้อง 1", **self.font_styte) 
        elif self.Iscam1_fail and self.Iscam2_fail: 
            self.notify_text.configure(text = "ไม่สามารถอ่านกล้องใช้งานกล้องได้ กรุณากดข้าม", **self.font_styte) 
            self.camcapture_btn.configure(command = self._on_both_cam_fail, text = "ข้าม")
        else:
            pass 