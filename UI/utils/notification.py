#on dev.
import customtkinter as ctk
from tkinter import Frame,Label,Canvas
from PIL import Image

class Notification(ctk.CTkFrame):
    def __init__ (self, parent):
        super().__init__(parent)
        self.configure(fg_color = '#F3F3F3', width = 200, height = 200,corner_radius = 20)
        self.font_styte = {'font': ("Noto Sans Thai", 18)}
        self.font_styte2 = {'font': ("Noto Sans Thai", 16)}

        self.create_widget()

    def create_widget(self):

        Label(self,text = "แจ้งเตือน", **self.font_styte, fg="#035E5A",justify="left", bg=self.cget("fg_color")).grid(row=0,column=0, padx=10, pady = 5,ipadx=10,sticky='w')

        self.canvas = Canvas(self, width=200, height=10, background=self.cget("fg_color"))
        self.canvas.create_line(0, 1, self.canvas.cget("width"), 1 , width=10, fill='#035E5A')
        self.canvas.grid(row=1, column=0)

        #for notify
        # self.msg = ctk.CTkLabel(self,text = "นำยาออกเรียบร้อย", font = ("Noto Sans Thai", 20), corner_radius=5,fg_color = "#FFFFFF", text_color="#035E5A")
        # self.msg.grid(row=2,column=0, padx=20, pady = 20, ipadx=20)

        #for report
        self.content_frame = ctk.CTkFrame(self) 
        self.content_frame.grid(row=2,column=0, padx=20, pady = 20, ipadx=20)

        Label(self.content_frame, text= "จำนวนยา", **self.font_styte2).grid(row=0, column=0, padx = 30, pady=5)
        Label(self.content_frame, text= "สาเหตุ", **self.font_styte2).grid(row=0, column=1,padx = 10, pady=5)
        Label(self.content_frame, text= "ชื่อผู้ป่วย", **self.font_styte2).grid(row=0, column=2,padx = 10, pady=5)
        Label(self.content_frame, text= "ชื่อยา", **self.font_styte2).grid(row=0, column=3,padx = 10, pady=5)

        self.confirmBtn = ctk.CTkButton(self, text="ยืนยัน", **self.font_styte, corner_radius = 15, fg_color='#035E5A',width=100)
        self.confirmBtn.grid(row = 3, column =0, pady = 10, padx =70)
        
        self.takeoutBtn = ctk.CTkButton(self, text="นำยาออก", **self.font_styte, corner_radius = 15, fg_color='#035E5A',width=100)
        self.takeoutBtn.grid(row = 3, column =0, pady = 10, padx =70)

    # def set_notification(self, new_text):
    #     self.msg.configure(text = new_text)
                
class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)
