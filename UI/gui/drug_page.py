import customtkinter as ctk
import tkinter
from PIL import Image, ImageTk
from utils.table_handler import Table
from utils.mockup_data  import mockup_data
from utils.button_handler import MyButton
from utils.api_handler import post_api_data, get_api_data
from utils.popup.why_return import WhyReturnPopup

class DrugPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master = parent)
        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF")
        self.pages = None
        self.slot_id = None 
        self.parent = parent
        
        self.open_slot_key = {'status': 1}
        self.close_slot_key = {'status': 0}
        print("page: Drug page > init!")

        self.load_images()
        self.create_widgets()

    def load_images(self):
        try:
            pil_back = Image.open("C:/Service_Robot/UI/assets/check_drug_page/back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)
            
            self.template_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/check_drug_page/template.png"), size=(920,360))
        except Exception as e:
            print(f"Error: {e}")

    def create_widgets(self):
        self.back_btn = tkinter.Button(
            master=self, 
            text="", 
            image=self.back_img, 
            borderwidth=0,
            background="#FFFFFF",
            highlightthickness=0,
            activebackground="#FFFFFF",
            command=lambda: self.back())
        self.back_btn.place(relx=0.00, rely=0.04)

        self.title = ctk.CTkLabel(self, text="เลือกยาที่ต้องการนำออก", 
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
        self.shadow.place(relx=0.5, rely=0.45, anchor="center")

        self.table_frame = Table(master=self, 
            width=900, height=360,            
            bg_color="#FFFFFF",
            fg_color="#FFFFFF")
        self.table_frame.place(relx=0.5, rely=0.45, anchor="center")
    
        self.takeout_btn = MyButton(self)
        self.return_btn = MyButton(self)

        self.takeout_btn.configbtn(text="นำยาออก", 
                                  command=self._on_confirmTakeout_click,
                                  x=0.38, 
                                  y=0.85
                                  )
        self.takeout_btn.configure(width=200, height=50, font=("Noto Sans Thai", 18, "bold"), corner_radius=25)

        self.return_btn.configbtn(text="ส่งยากลับ", 
                                  command=self._on_return_click,
                                  x=0.62, 
                                  y=0.85
                                  )
        self.return_btn.configure(width=200, height=50, font=("Noto Sans Thai", 18, "bold"), corner_radius=25)
                                  
    def _on_confirmTakeout_click(self):
        print(f"page: Drug page > Goto Export page")
        self.pack_forget()
        self.pages['export_page'].pack(fill='both', expand=True)
        self.pages['export_page'].on_display()
        
        qrScan = post_api_data('qr_scan', self.plot_data)
        if qrScan["success"]:
            print(f"Data posted successfully: {qrScan['data']}")
        else:
            print(f"Error posting data: {qrScan['error']}")

    def back(self):
        print(f"page: Drug page > back click (no action)")

    def _on_return_click(self):
        print(f"page: Drug page > return click" )
        self.popup = WhyReturnPopup(self.master)
        self.popup.confirm_btn.configure(command=self._on_popup_confirmclick)

    def update_table(self):
        self.data = get_api_data('slot')
        self.plot_data = self.data[f"slot{self.slot_id}"]
        self.table_frame.update_table(self.plot_data)

    def _on_popup_confirmclick(self):
        print("page: Drug page > Confirm to return click.")
        self.selected_reason = self.popup.radio_button_group.get_why()

        data = {
            'hn': self.plot_data['hn'],
            'IsReturn' : True,
            'WhyReturn': self.selected_reason
        }
        
        closeGate = post_api_data('gate', self.close_slot_key)
        qrScan = post_api_data('qr_scan', data)
        
        self.popup.destroy()
        self.pack_forget()
        self.pages['main_page'].on_display()

    def on_display(self):
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)

class RadioButtonGroup:
    def __init__(self, master, radio_var, options, relx_start=0.1, rely_start=0.1, rely_step=0.25, **kwargs):
        self.master = master
        self.radio_var = radio_var
        self.options = options
        self.relx_start = relx_start
        self.rely_start = rely_start
        self.rely_step = rely_step
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
            radio_button.place(relx=self.relx_start, rely=self.rely_start + index * self.rely_step)

    def get_why(self):
        selected_value = self.radio_var.get()
        for text, value in self.options:
            if value == selected_value:
                return text
        return None