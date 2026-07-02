import customtkinter as ctk
from tkinter import Frame
from PIL import Image

class SlotOnProblemPopup(ctk.CTkToplevel):
    def __init__(self, parent, type = None):
        super().__init__(parent)
        self.type = type
        self.parent = parent
        self.wm_overrideredirect(True)
        self.configure(fg_color="#FFFFFF")
        self.geometry("600x350")
        self.center_window()
        self.resizable(False, False)
        
        self.load_images()
        self.create_widgets()

    def load_images(self):
        self.slot_problem_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\popup\problemSlot.png"), size=(580, 60))
        
    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, bg_color="#FFFFFF", fg_color="#FFFFFF",corner_radius=0)
        self.header_frame.pack(padx = 5, pady = 10)

        self.header_image = ctk.CTkLabel(self.header_frame, image=self.slot_problem_img, text=None)
        self.header_image.pack(padx = 5, pady = 5)
        
        self.content_frame = ctk.CTkFrame(self, bg_color="#FFFFFF", fg_color="#F4F4F4",corner_radius=20, width=580, height=120)
        self.content_frame.pack(padx = 10, pady = 5, fill='x')

        header_font = ('Prompt', 18, 'bold')
        body_font = ('Prompt', 18)
        
        headers = ["จำนวนยา", "สาเหตุ", "ชื่อผู้ป่วย", "ชื่อยา"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.content_frame, text=h, font=header_font, text_color="#035E5A").grid(row=0, column=i, padx=25, pady=10)
        
        self.total_Drug = ctk.CTkLabel(self.content_frame, text="2", font=body_font, text_color="#000000")
        self.total_Drug.grid(row=1, column=0)

        self.why_return = ctk.CTkLabel(self.content_frame, text="ยาไม่ตรง", font=body_font, text_color="#000000")
        self.why_return.grid(row=1, column=1)

        self.patientName = ctk.CTkLabel(self.content_frame, text="ชื่อผู้ป่วย", font=body_font, text_color="#000000")
        self.patientName.grid(row=1, column=2)

        self.drugAmout = ctk.CTkLabel(self.content_frame, text="ชื่อยา", font=body_font, text_color="#000000")
        self.drugAmout.grid(row=1, column=3, ipady=10)

        self.button_frame = Frame(self, background="#FFFFFF")
        self.button_frame.pack(pady=10)

        self.takeOutBtn = ctk.CTkButton(self.button_frame,
                                           text="นำยาออก",
                                           text_color="#FFFFFF",
                                           bg_color="#FFFFFF",
                                           fg_color="#035E5A",
                                           hover=False,
                                           corner_radius=25,
                                           width=200,
                                           height=50,
                                           font=('Prompt', 20, 'bold'),
                                           command=self.on_TakeOutClick
                                           )
        self.takeOutBtn.pack()  
        
        self.lift()
        self.wm_transient(self.parent.master)
    
    def on_TakeOutClick(self):
        self.destroy()

    def fetch_data(self, data, slotID):
        plot_data = data[f"slot{slotID}"]
        self.total_Drug.configure(text =str(len(plot_data['drugs'])))
        self.why_return.configure(text= plot_data['WhyReturn'])
        self.patientName.configure(text= plot_data['name']['first'] + ' ' + plot_data['name']['last'])
        self.drugAmout.configure(text=plot_data['drugs'][0])

    def center_window(self):
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")