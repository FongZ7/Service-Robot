import customtkinter as ctk

class MyButton(ctk.CTkButton):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.configure(
            text = None, 
            font = ("Noto Sans Thai", 14, "bold"),
            corner_radius = 10,
            width=30,
            height=40,
            bg_color = "#FFFFFF",
            fg_color = "#035E5A",
            text_color = "#FFFFFF",
            image=None,
            hover=True,
            hover_color= "#67A7A4",
            )
        
    def configbtn(self, text, command,x,y):
        self.configure(text = text, command = command)
        self.place(relx = x, rely = y)
        
        