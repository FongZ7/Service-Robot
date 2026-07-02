import customtkinter as ctk
from tkinter import Frame
from PIL import Image
import tkinter

class RadioButtonGroup:
    def __init__(self, master, radio_var, options, **kwargs):
        self.master = master
        self.radio_var = radio_var
        self.options = options
        self.kwargs = kwargs
        self.create_radio_buttons()

    def create_radio_buttons(self):
        for index, (text, value) in enumerate(self.options):
            radio_button = ctk.CTkRadioButton(
                master=self.master, 
                variable=self.radio_var, 
                value=value, 
                text=text,
                **self.kwargs
            )
            radio_button.pack(padx = 5 ,pady = 5) # ลด padding

    def get_why(self):
        selected_value = self.radio_var.get()
        for text, value in self.options:
            if value == selected_value:
                return text
        return None
    
class WhyReturnPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="#FFFFFF", bg_color = "#FFFFFF", corner_radius= 10)
        self.wm_overrideredirect(True)
        # ปรับขนาดหน้าต่าง
        self.geometry("500x350")
        self.center_window()
        self.resizable(False, False)
        self.deiconify() 

        self.options = [
            ("ยาไม่ตรง", 0),
            ("ยาไม่ครบ", 1),
            ("อื่นๆ    ", 2),
        ]

        self.radio_var = tkinter.IntVar(value=0)
        self.load_images()
        self.create_widgets()

    def load_images(self):
        # Correct path and resize image
        self.whyReturn_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\popup\whyreturn.png"), size=(480, 60))

    def create_widgets(self):
        self.header_frame = Frame(self, background="#FFFFFF")
        self.header_frame.pack(pady = 5)

        self.content_frame = ctk.CTkFrame(self, bg_color="#FFFFFF", fg_color="#F4F4F4", corner_radius=20, width=450, height=180)
        self.content_frame.pack(pady = 5, padx = 20, fill = 'both', expand = True)

        self.header_image = ctk.CTkLabel(self.header_frame, 
                    image=self.whyReturn_img,
                    text=None,
                    fg_color="#FFFFFF",
                    bg_color="transparent"
                     )
        self.header_image.pack(padx = 5, pady = 5, fill = 'x')

        self.radio_button_group = RadioButtonGroup(
            master= self.content_frame,
            radio_var=self.radio_var,
            options=self.options,
            fg_color="#035E5A",
            text_color="#035E5A",
            font=("Noto Sans Thai", 18) 
        )
        
        self.button_frame = Frame(self, background="#FFFFFF")
        self.button_frame.pack(pady = 10)

        # Scale buttons
        btn_config = {
            "text_color": "#FFFFFF",
            "bg_color": "#FFFFFF",
            "fg_color": "#035E5A",
            "corner_radius": 22,
            "width": 160,
            "height": 45,
            "font": ('Prompt', 16, 'bold')
        }

        self.confirm_btn = ctk.CTkButton(self.button_frame, text="ยืนยัน", hover_color="#67A7A4", **btn_config)
        self.return_btn = ctk.CTkButton(self.button_frame, text="กลับ", hover_color="#67A7A4", command=self._on_returnClick, **btn_config)
        
        self.confirm_btn.pack(side = 'left', padx = 15)
        self.return_btn.pack(side = 'right',padx = 15)

        self.lift()
        self.wm_transient(self.parent.master)

    def _on_returnClick(self):
        print("page: Drug page > Back click.")
        self.destroy()

    def center_window(self):
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")