import customtkinter as ctk
from tkinter import Frame, Canvas
from PIL import Image


class PopupDrugReturn(ctk.CTkFrame):
    def __init__(self, parent, first_name, last_name, why_return, drugs):
        super().__init__(parent)
        self.configure(width=795, height=316, corner_radius=0, fg_color="#F4F4F4")
        self.parent = parent
        self.first_name = first_name
        self.last_name = last_name
        self.why_return = why_return
        self.drugs = drugs
        self.load_images()
        self.create_widgets()
        self.ack_popup = PopupDrugReturnAck(self.parent)  

    def load_images(self):
        self.popup_img = ctk.CTkImage(light_image=Image.open("assets/slot_page/popup.png"), size=(800, 316))
        self.notifytakeout_img = ctk.CTkImage(light_image=Image.open("assets/slot_page/notifyTakeout.png"), size=(390, 220))

    def create_widgets(self):
        self.PopupLabel1 = ctk.CTkLabel(self, text=None, image=self.popup_img, fg_color="#F4F4F4", width=795, height=316)
        self.name_text = ctk.CTkLabel(self.PopupLabel1, text=str(self.first_name) + " " + str(self.last_name), font=("Noto Sans Thai", 20),
                                      text_color="#035E5A",
                                      )
        self.why_return_text = ctk.CTkLabel(self.PopupLabel1, text=str(self.why_return), font=("Noto Sans Thai", 20),text_color="#035E5A")
        self.drugs_text = ctk.CTkLabel(self.PopupLabel1, text=str(len(self.drugs)), font=("Noto Sans Thai", 20),text_color="#035E5A")
                
        self.confirmtakeout_btn = ctk.CTkButton(self.PopupLabel1, 
                                                text="เอายาออก", 
                                                hover=False, 
                                                width=140, height=45, 
                                                fg_color="#035E5A", 
                                                corner_radius=30, font=("Noto Sans Thai", 20), 
                                                command=self.show_ack_popup)
        self.close_btn = ctk.CTkButton(self.PopupLabel1, 
                                       text="X", 
                                       corner_radius=30, 
                                       width=30, height=30, 
                                       font=("Noto Sans Thai", 20), 
                                       fg_color="#035E5A", 
                                       hover=False, command=self.closepopup)

    def show_ack_popup(self):
        self.place_forget()
        self.ack_popup.place(relx=0.4, rely=0.35)  

    def closepopup(self):
        self.place_forget()

    def place(self, relx, rely):
        self.PopupLabel1.place(x=0, y=0)
        self.confirmtakeout_btn.place(x=320, y=240)
        self.close_btn.place(x=720, y=20)
        self.name_text.place(x=120, y=170)
        self.why_return_text.place(x=350, y=170)
        self.drugs_text.place(x=620, y=170)
        super().place(relx=relx, rely=rely)


#on dev.
class SlotOnProblem(ctk.CTkFrame):
    def __init__ (self, parent):
        super().__init__(parent)
        self.configure(fg_color = '#035E5A', width = 1050, height = 420, corner_radius = 20)
        self.font_styte = {'font': ("Noto Sans Thai", 18, "bold") , 'text_color' : '#FFFFFF'}
        self.load_images()
        self.create_widget()

    def load_images(self):    
        self.shadow_img = ctk.CTkImage(light_image=Image.open("assets/popup/shadowbox.png"), size=(1063,421))
        
    def create_widget(self):
        self.headerFrame = Frame(self, background= self.cget("fg_color"))
        self.headerFrame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.headerFrame, text="ช่องที่พบปัญหา",**self.font_styte).pack(padx = 20 , pady = 20)






class PopupDrugReturnAck(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(width=390, height=225, corner_radius=0, fg_color="#F4F4F4")
        self.load_images()
        self.create_widgets()

    def load_images(self):
        self.notifytakeout_img = ctk.CTkImage(light_image=Image.open(r"C:\UI-Service_Robot\assets\slot_page\notifyTakeout.png"), size=(390, 220))

    def create_widgets(self):
        self.PopupLabel = ctk.CTkLabel(self, image=self.notifytakeout_img, text=None, width=380, height=225, fg_color="#F4F4F4")
        self.PopupLabel.place(x=0, y=0)
        self.takeoutConfirm_btn = ctk.CTkButton(self, 
                                                text="ยืนยัน", 
                                                hover=False, width=140, height=45, 
                                                fg_color="#035E5A", corner_radius=35, 
                                                font=("Noto Sans Thai", 20), 
                                                command=lambda : self.place_forget())
        self.takeoutConfirm_btn.place(x=120, y=140)

class PopupUsedSlot(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(width=350, height=270, corner_radius=25, fg_color = "#FFFFFF")
        self.load_images()
        self.create_widgets()
        self.place(relx=0.35, rely=0.2)

    def load_images(self):
        self.usedslot_img = ctk.CTkImage(light_image=Image.open("assets/slot_page/popupused.png"), size=(485, 270))
    
    def create_widgets(self):

        self.PopupLabel = ctk.CTkLabel(self, image=self.usedslot_img, text=None, width=485, height=270, fg_color="#F4F4F4")
        self.PopupLabel.pack()

        self.ack_btn = ctk.CTkButton(self.PopupLabel, 
                                                text="ตกลง", 
                                                hover=False, width=150, height=55, 
                                                fg_color="#035E5A", corner_radius=35, 
                                                font=("Noto Sans Thai", 24), 
                                                command=lambda : self.place_forget())
        self.ack_btn.place(relx = 0.32, rely = 0.7)

        