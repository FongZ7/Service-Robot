import customtkinter as ctk
from tkinter import Button, PhotoImage
from PIL import Image, ImageTk 
from utils.table_handler import Table
from utils.mockup_data import mockup_data
from utils.button_handler import MyButton
from utils.api_handler import post_api_data, get_api_data

class ReCheckDrugPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF") 
        self.slot_id = None
        self.pages = None
        self.data = None
        
        self.open_slot_key = {'status': 1}
        self.close_slot_key = {'status': 0}
        print("page: ReCheck Drug page > init!")

        self.load_images()
        self.create_widgets()

    def load_images(self):
        try:
            pil_back = Image.open(r"C:\Service_Robot\UI\assets\check_drug_page\back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)

            self.add_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\check_drug_page\add.png"), size=(30, 30))
            self.add_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\check_drug_page\add.png"), size=(30, 30))
            self.template_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\check_drug_page\template.png"), size=(920, 470))
        except Exception as e:
            print(f"Error loading images: {e}")
            self.back_img = None
            self.add_img = None
            self.template_img = None

    def create_widgets(self):
        self.back_btn = Button(
            master=self, 
            text="", 
            image=self.back_img, 
            borderwidth=0,
            background="#FFFFFF",
            highlightthickness=0,
            command=self.back
        )
        self.back_btn.place(relx=0.00, rely=0.04)

        self.title = ctk.CTkLabel(self, text="ยานำเข้าทุกรายการ", 
                                  font=("Noto Sans Thai", 24, "bold"), 
                                  text_color="#035E5A",
                                  bg_color="transparent")
        self.title.place(relx=0.10, rely=0.050) 

        self.shadow = ctk.CTkLabel(
            master=self,
            image=self.template_img,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
            text=None,
        )
        self.shadow.place(relx=0.5, rely=0.48, anchor="center")

        self.table_frame = Table(master=self, 
            width=900, height=450,            
            bg_color="#FFFFFF",
            fg_color="#FFFFFF")
        
        self.table_frame.place(relx=0.5, rely=0.48, anchor="center")
    
        self.return_main_btn = MyButton(self)
        self.return_main_btn.configbtn(
                                  text="กลับหน้าหลัก", 
                                  command=self._on_returnMainBtn_click,
                                  x=0.5, y=0.90 
                                  )
        
        self.return_main_btn.place(relx=0.5, rely=0.90, anchor="center")

        try:
             self.return_main_btn.configure(width=200, height=50, font=("Noto Sans Thai", 18, "bold"), corner_radius=25)
        except:
             pass 

    def back(self):
        print("page: reCheckDrug page > goto reCheckSlot page")
        self.pack_forget()
        if self.pages and 'reSlot_page' in self.pages:
            self.pages['reSlot_page'].on_display()

    def _on_returnMainBtn_click(self):
        print("page: reCheckDrug page > goto main page")
        self.pack_forget()
        if self.pages and 'main_page' in self.pages:
            self.pages['main_page'].on_display()

    def update_table(self):
        print("page: ReCheckDrugPage > Detail Phamacy")
        
        self.data = get_api_data('slot')

        if self.slot_id is not None:
            self.plot_data = self.data.get(f"slot{self.slot_id}", {})
            
            if not self.plot_data:
                self.plot_data = {} 

            self.table_frame.update_table(self.plot_data)
        else:
            print("Warning: Slot ID is None")
            self.table_frame.update_table({})

    def on_display(self):
        """packing the frame to set the cursor."""
        self.update_table()
        self.pack(fill='both', expand=True)
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)