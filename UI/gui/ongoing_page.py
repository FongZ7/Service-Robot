import customtkinter as ctk
from tkinter import Frame
from PIL import Image
import os
from utils.mockup_data import mockup_data
from utils.api_handler import post_api_data

class RobotGoing(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.width = 1280  
        self.height = 800 
        self.pages = None
        self.configure(width=self.width, height=self.height, fg_color="#FFFFFF")
        print("page: OnGoing page > init!")
        
        self.frames = []
        self.frame_index = 0
        self.direction = 1  
        self.delay = 33
        self.animating = False
        self.pause_key = {'status' : 'pause'}
        self.resume_key = {'status' : 'resume'}
        self.after_id = None
        self.load_images()
        self.create_widgets()
        self.stop_animation()

    def load_images(self):
        self.pause_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/ongoing_page/pause.png"), size=(30, 30))
        self.resume_img = ctk.CTkImage(light_image=Image.open("C:/Service_Robot/UI/assets/ongoing_page/resume.png"), size=(30, 30))

        frame_folder = "assets/ongoing_page/robotgoing"
        for filename in sorted(os.listdir(frame_folder)):
            if filename.endswith(".png"):
                image_path = os.path.join(frame_folder, filename)
                image = Image.open(image_path)
                resized_image = image.resize((self.width, self.height)) # 480x320
                self.frames.append(ctk.CTkImage(light_image=resized_image, size=(self.width, self.height)))

    def create_widgets(self):
        self.animatetion = ctk.CTkLabel(self, text=None, fg_color="#FFFFFF", image=self.frames[0])
        self.animatetion.place(x=0, y=0)

        self.resume_btn = ctk.CTkButton(self, text="RESUME", 
                                        text_color="#FFFFFF", 
                                        font=('Inter', 20, "bold"), 
                                        corner_radius=20,
                                        fg_color="#035E5A",
                                        image=self.resume_img,
                                        compound='left',
                                        command=self.on_resumeClick,
                                        width=140,
                                        height=50,
                                        hover=False,
                                        bg_color="#FFFFFF"
                                        )
        
        self.pause_btn = ctk.CTkButton(self, text="PAUSE", 
                                text_color="#FFFFFF", 
                                font=('Inter', 20, "bold"), 
                                corner_radius=20,
                                fg_color="#FFA236",
                                image=self.pause_img,
                                compound='left',
                                command=self.on_pauseClick,
                                width=140,
                                height=50,
                                hover=False,
                                bg_color="#FFFFFF"
                                )
        self.pause_btn.place(relx=0.5, rely=0.85, anchor="center")

    def animate(self):
        if not self.animating:
            return

        self.animatetion.configure(image=self.frames[self.frame_index])
        self.frame_index += self.direction

        if self.frame_index == len(self.frames) or self.frame_index == -1:
            self.direction *= -1
            self.frame_index += self.direction

        if self.pages['topbar'].robot_status == 2:
            self.on_arriving()
            return

        if self.pages['topbar'].robot_charge_status == "true" and (self.pages['topbar'].robot_status == 8 or self.pages['topbar'].robot_status == 10):
            self.on_charger_arriving()

        self.after_id = self.after(self.delay, self.animate)

    def start_animation(self):
        if not self.animating:
            self.animating = True
            self.animate()

    def stop_animation(self):
        self.animating = False
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.frame_index = 0  

    def on_resumeClick(self):
        print("On Going Page: Resume Btn clicked.")
        post_api_data('pause', self.resume_key)
        self.start_animation()
        self.resume_btn.place_forget()
        self.pause_btn.place(relx=0.5, rely=0.85, anchor="center")

    def on_pauseClick(self):
        print("On Going Page: Pause Btn clicked.")
        post_api_data('pause', self.pause_key)
        self.stop_animation()
        self.pause_btn.place_forget()
        self.resume_btn.place(relx=0.5, rely=0.85, anchor="center")

    def on_arriving(self):
        print("On Going Page: Arriving.")
        self.stop_animation()
        self.pause_btn.place_forget()
        self.pause_btn.place(relx=0.5, rely=0.85, anchor="center")
        self.pack_forget()
        self.pages['topbar'].robot_status = 0
        self.pages['main_page'].on_display()
        self.pages['topbar'].home_btn.configure(state="normal")
        self.pages['topbar'].chargeAction_btn.configure(state="normal")

    def on_charger_arriving(self):
        print("On Going Page: Arriving at charger station.")
        self.stop_animation()
        self.pause_btn.place_forget()
        self.pause_btn.place(relx=0.5, rely=0.85, anchor="center")
        self.pack_forget()
        self.pages['topbar'].robot_status = 0
        self.pages['main_page'].on_display()
        self.pages['topbar'].home_btn.configure(state="normal")
        self.pages['topbar'].chargeAction_btn.configure(state="normal")