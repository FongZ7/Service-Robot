import customtkinter as ctk
from PIL import Image
import os

class IconHandler():
    def __init__(self):
        self.icons = {}
        self.load_icon()

    def load_icon(self):
        battery_levels = [10, 20, 30, 50, 60, 70, 80, 100]
        
        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        assets_path = os.path.join(current_dir, "..", "assets", "top_bar", "battery")

        for level in battery_levels:
            try:

                img_path = os.path.join(assets_path, f"batt{level}.png")
                self.icons[f"battery_{level}"] = ctk.CTkImage(light_image=Image.open(img_path), size=(30, 20))
                
                charge_path = os.path.join(assets_path, f"Chargebatt{level}.png")
                self.icons[f"battery_{level}_charging"] = ctk.CTkImage(light_image=Image.open(charge_path), size=(30, 20))
            
            except Exception as e:
                print(f"Error loading battery icon {level}: {e}")
                self.icons[f"battery_{level}"] = None
                self.icons[f"battery_{level}_charging"] = None

    def get_icon(self, percentage, is_charge):
        battery_levels = [10, 20, 30, 50, 60, 70, 80, 100]
        
        target_level = 100
        for level in battery_levels:
            if percentage <= level:
                target_level = level
                break
        
        icon_key = f"battery_{target_level}"

        is_charging_bool = False
        if isinstance(is_charge, str):
            is_charging_bool = is_charge.lower() == "true"
        elif isinstance(is_charge, bool):
            is_charging_bool = is_charge

        if is_charging_bool:
            icon_key += "_charging"

        return self.icons.get(icon_key, self.icons.get("battery_100"))