
import customtkinter as ctk
from tkinter import Frame
from PIL import Image
import os
from utils.mockup_data import mockup_data

class BarcodeAnimate(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # Main Frame config.
        self.parent = parent
        self.scale = 0.80
        self.width = int(777 * self.scale)
        self.height = int(376 * self.scale)
        self.configure(width=self.width, height=self.height)

        # Animation config.
        self.frames = []
        self.frame_index = 0
        self.direction = 1  # 1 for forward, -1 for backward
        self.delay = 15  # delay in milliseconds between frames
        self.animating = False  # flag to control animation

        self.load_images()
        self.create_widgets()

    def load_images(self):
        frame_folder = "assets/barcode_import_page/animation"
        for filename in sorted(os.listdir(frame_folder)):
            if filename.endswith(".png"):
                image_path = os.path.join(frame_folder, filename)
                image = Image.open(image_path)
                resized_image = image.resize((self.width, self.height))
                self.frames.append(ctk.CTkImage(light_image=resized_image, size=(self.width, self.height)))

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text=None, fg_color="#FFFFFF", image=self.frames[0])
        self.label.place(x=0, y=0)

    def animate(self):
        if not self.animating:
            return  # Stop animation if flag is False

        self.label.configure(image=self.frames[self.frame_index])
        self.frame_index += self.direction

        if self.frame_index == len(self.frames) or self.frame_index == -1:
            self.direction *= -1
            self.frame_index += self.direction

        self.after(self.delay, self.animate)

    def start_animation(self):
        if not self.animating:
            self.animating = True
            self.animate()

    def stop_animation(self):
        self.animating = False