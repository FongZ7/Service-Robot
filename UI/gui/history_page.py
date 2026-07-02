import customtkinter as ctk
from tkinter import Button, PhotoImage
from PIL import Image, ImageTk
from utils.history_table_handler import HistoryTable 
from utils.button_handler import MyButton
from utils.api_handler import get_api_data

class HistoryPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master = parent)
        self.configure(corner_radius = 0, fg_color = "#FFFFFF")
        self.slot_id = None
        self.pages= None
        self.data = None
        print("page: History page > init!")

        self.load_images()
        self.create_widgets()

    def load_images(self):
        try:
            pil_image = Image.open("C:/Service_Robot/UI/assets/check_drug_page/back.png")
            resized_image = pil_image.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_image)
        except Exception:
            self.back_img = None

        self.add_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/check_drug_page/add.png"), size=(30,30))
        self.template_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/check_drug_page/template.png"), size=(920,470))

    def create_widgets(self):

        self.back_btn = Button(
            master=self,  
            text="", 
            image=self.back_img, 
            borderwidth=0,
            background="#FFFFFF",
            highlightthickness=0,
            activebackground="#FFFFFF", 
            command=self.back)
        
        self.back_btn.place(relx=0.00, rely=0.06)

        self.title = ctk.CTkLabel(self, text="ประวัติการนำเข้ายา", 
                                  font=("Noto Sans Thai", 24, "bold"), 
                                  text_color="#035E5A",
                                  bg_color="transparent"
                                  )
        self.title.place(relx=0.10, rely=0.065) 

        self.shadow = ctk.CTkLabel(
            master=self,
            image=self.template_img, 
            text="", 
        )

        self.shadow.place(relx=0.5, rely=0.48, anchor="center")

        self.table_frame = HistoryTable(master=self, 
            width=900,   
            height=450,  
            bg_color="#FFFFFF", 
            fg_color="#FFFFFF",
            corner_radius=0
            )
        

        self.table_frame.place(relx=0.5, rely=0.48, anchor="center")
    
        self.return_main_btn = MyButton(self)
        self.return_main_btn.configbtn(
                                  text="กลับหน้าหลัก", 
                                  command=self._on_returnMainBtn_click,
                                  x=0.5, 
                                  y=0.90 
                                  )
        self.return_main_btn.place(relx=0.5, rely=0.90, anchor="center")

        try:
             self.return_main_btn.configure(width=200, height=50, font=("Noto Sans Thai", 18, "bold"), corner_radius=25)
        except:
             pass 

    def back(self):
        print("page: History page > back to Main page")
        self.pack_forget()
        self.pages['main_page'].on_display()

    def _on_returnMainBtn_click(self):
        print("page: History page > back to Main page")
        self.pack_forget()
        self.pages['main_page'].on_display()

    def update_table(self):
        self.data = get_api_data('drug_log')
        self.table_frame.update_table(self.data)

    def on_display(self):
        self.update_table()
        self.pack(fill='both', expand=True)
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)