import customtkinter as ctk
from tkinter import Button, PhotoImage, Frame
from PIL import Image, ImageTk
from utils.button_handler import MyButton
from utils.api_handler import post_api_data

class CloseDoorNotify(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF")
        self.pages = None
        self.open_slot_key = {'status': 1}
        self.close_slot_key = {'status': 0}
        print("page: Notify page > init!")
        self.load_images()
        self.create_widgets()

    def load_images(self):
        try:
            pil_back = Image.open("C:/Service_Robot/UI/assets/check_drug_page/back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)
            
            self.box_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/closedoornotify_page/icon_text.png"), size=(600, 260))
        except Exception as e:
            print(f"Error: {e}")
        
    def create_widgets(self):
        self.firstFrame = Frame(self, background=self.cget('fg_color'))
        self.firstFrame.pack(anchor='nw', fill='x', pady=(10,0))
        self.middleFrame = Frame(self, background=self.cget('fg_color'))
        self.middleFrame.pack(expand=True)
        
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

        self.notify = ctk.CTkLabel(self, 
                                   corner_radius=None, 
                                   bg_color="transparent",
                                   image=self.box_img,
                                   text=None
                                   )
        self.notify.place(relx=0.5, rely=0.45, anchor="center")

        self.confirmbtn = MyButton(self)
        self.confirmbtn.configbtn(text="ยืนยัน", command=self.on_comfirmbtn_click, x=0.5, y=0.90)
        self.confirmbtn.configure(width=200, height=50, font=("Noto Sans Thai", 18, "bold"), corner_radius=25)
        self.confirmbtn.place(relx=0.5, rely=0.90, anchor="center")
    
    def on_comfirmbtn_click(self):
        self.pack_forget()
        print(f"page: notify page > Goto Main page")
        self.pages['main_page'].on_display()

    def back(self):
        print("Notify Page: Back clicked")
        self.pack_forget()
        if self.pages and 'import_page' in self.pages:
            self.pages['import_page'].on_display()

    def on_display(self):
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)