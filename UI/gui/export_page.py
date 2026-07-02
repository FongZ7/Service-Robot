import customtkinter as ctk
from tkinter import Button
from PIL import Image, ImageTk
from utils.button_handler import MyButton
from utils.api_handler import post_api_data

class ExportPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF")
        self.pages = None
        self.open_slot_key = {'status': 1}
        self.close_slot_key = {'status': 0}
        print("page: Export page > init!")
        self.load_images()
        self.create_widgets()

    def load_images(self):
        try:
            pil_back = Image.open(r"C:\Service_Robot\UI\assets\check_drug_page\back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)

            self.box_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\export_page\export.png"), size=(600, 260))
        except Exception as e:
            print(f"Error loading images: {e}")
            self.back_img = None
            self.box_img = None
        
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

        self.back_btn.place(relx=0.00, rely=0.04)
        self.box = ctk.CTkLabel(self, corner_radius=None, bg_color="transparent", image=self.box_img, text=None)
        self.box.place(relx=0.5, rely=0.45, anchor="center")

        self.confirmbtn = MyButton(self)
        self.confirmbtn.configbtn(text="ยืนยัน", command=self.on_comfirmbtn_click, x=0.5, y=0.90)
        self.confirmbtn.configure(width=200, height=50, font=("Noto Sans Thai", 18, "bold"), corner_radius=25)
        self.confirmbtn.place(relx=0.5, rely=0.90, anchor="center")
    
    def on_comfirmbtn_click(self):
        print(f"page: Export page > Goto Notify page")
        self.pack_forget()
        self.pages['notify_page'].pack(fill='both', expand=True)

        closeGate = post_api_data('gate', self.close_slot_key)
        if closeGate.get("success", False):
            print(f"Data posted successfully: {closeGate.get('data')}")
        else:
            print(f"Error posting data: {closeGate.get('error')}")


    def back(self):
        print("Exprot Page: back to Main page.")
        self.pack_forget()
        if self.pages and 'main_page' in self.pages:
            self.pages['main_page'].on_display()

    def on_display(self):
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)