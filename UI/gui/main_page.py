import customtkinter as ctk
from tkinter import Frame
import json
from PIL import Image
from utils.api_handler import post_api_data

class Mainpage(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        print("page: Main page > init!")
        self.pages = None
        self.parent = parent
        self.closeApp_stacking = 3
        self.configure(fg_color="#FFFFFF")

        #api key
        self.insert_key = {"status": "insert"}
        self.takeout_key = {"status": "takeout"} 
        self.running_key = {"status":1}
        self.stopping_key = {"status":0}

        self.load_images()
        self.create_widgets()
        self.update_btn()

    def load_images(self) -> None:
        try:

            self.verify_icon = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\main_page\verify_ico.png"), size=(153, 65))
            self.history_icon = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\main_page\history_ico.png"), size=(217, 65)) 
            self.drug_import_icon = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\main_page\import_ico.png"), size=(120, 120)) 
            self.drug_export_icon = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\main_page\export_ico.png"), size=(107, 120)) 
            self.drug_deliver_icon = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\main_page\ongoing_ico.png"), size=(160, 40))
            
        except Exception as e:
            print(f"Error loading images: {e}")
            self.drug_import_img = self.drug_export_img = self.drug_deliver_img = None

    def create_widgets(self) -> None:
        self.frame1 = Frame(master=self, background=self.cget('fg_color')) 
        self.frame2 = Frame(master=self, background=self.cget('fg_color'))
        self.frame3 = Frame(master=self, background=self.cget('fg_color'))

        self.frame1.pack(fill='x', pady=(20, 10))
        self.frame2.pack(pady=30)
        self.frame3.pack(pady=20)     

        self.verify_btn = ctk.CTkButton(
            master=self.frame1,
            image=self.verify_icon,
            text='',
            fg_color= "#FFFFFF",
            hover=False,
            width=153,
            height=65,
            corner_radius=10,
            command=self.verifyBtn_onClick
        )
        self.verify_btn.pack(side='left', padx = 25, pady = 5)     

        self.history_btn = ctk.CTkButton(
            master=self.frame1,
            image=self.history_icon,
            text='',
            fg_color= "#FFFFFF",
            hover =False,
            width=217,  
            height=65,  
            corner_radius=10,
            command=self.historyBtn_onClick
        )
        self.history_btn.pack(side='right', padx = 25, pady = 5)


        self.drugImport_btn = ctk.CTkButton(
            master=self.frame2,
            text="นำยาเข้า",
            font=("Noto Sans Thai", 30, "bold"),
            image=self.drug_import_icon,
            compound="top",
            fg_color="#035E5A",
            hover=True,
            hover_color= "#67A7A4",
            width = 450, 
            height= 320, 
            corner_radius=20,
            command=self.drugImportBtn_onClick
        )
        self.drugImport_btn.pack(side='left', padx = 20)

        self.drugExport_btn = ctk.CTkButton(
            master=self.frame2,
            text="นำยาออก",
            font=("Noto Sans Thai", 30, "bold"),
            image=self.drug_export_icon,
            compound="top",
            fg_color="#035E5A",
            hover_color= "#67A7A4",
            width = 450, 
            height= 320,
            corner_radius=20,
            command=self.drugExportBtn_onClick
        )
        self.drugExport_btn.pack(side='left', padx = 20)

        self.drugDeliver_btn = ctk.CTkButton(
            master=self.frame3,
            text="เริ่มนำส่งยาไปยังปลายทาง/กลับไปยังจุดรับยา",
            font=("Noto Sans Thai", 28, "bold"),
            image=self.drug_deliver_icon,
            compound="left",
            fg_color="#035E5A",
            hover_color= "#67A7A4",
            width= 930,   
            height= 100,   
            corner_radius=20,
            command=self.drugDeliverBtn_onClick
        )
        self.drugDeliver_btn.pack(pady=10)

    def drugImportBtn_onClick(self):
        print("page: Main page > Import Button Clicked.")
        import_api = post_api_data('in_out', self.insert_key)
        if import_api["success"]:
            print(f"Data posted successfully: {import_api['data']}")
        else:
            print(f"Error posting data: {import_api['error']}")
            
        self.pack_forget()
        self.pages['verify_page'].set_branch('in')
        self.pages['verify_page'].pack(fill='both')
        self.pages['verify_page'].on_display()

    def drugExportBtn_onClick(self):
        print("page: Main page > Export Button Clicked.")
        export_api = post_api_data('in_out', self.takeout_key)
        if export_api["success"]:
            print(f"Data posted successfully: {export_api['data']}")
        else:
            print(f"Error posting data: {export_api['error']}")

        self.pack_forget()
        self.pages['verify_page'].set_branch('out')
        self.pages['verify_page'].pack(fill='both')
        self.pages['verify_page'].on_display()

    def drugDeliverBtn_onClick(self):
        print("page: Main page > Deliver Button Clicked.")
        on_running = post_api_data('start', self.running_key)
        if on_running["success"]:
            print(f"Data posted successfully: {on_running['data']}")
        else:
            print(f"Error posting data: {on_running['error']}")

        self.pack_forget()
        self.pages['ongoing_page'].pack(pady = 50)
        self.pages['ongoing_page'].start_animation()

    def verifyBtn_onClick(self):
        print("page: Main page > Verify Button Clicked.")
        self.pack_forget()
        self.pages['reSlot_page'].on_display()

    def historyBtn_onClick(self):
        print("page: Main page > History Button Clicked.")
        self.pack_forget()
        self.pages['history_page'].on_display()

    def update_btn(self):
        if self.pages is not None :
            try:
                robot_status = self.pages['topbar'].robot_status
                if robot_status == 0 and robot_status is not None:
                    self.drugDeliver_btn.configure(state = 'normal', text="เริ่มนำส่งยาไปยังปลายทาง/กลับไปยังจุดรับยา")
                    self.drugDeliver_btn.pack_configure(ipadx = 10)
                else:
                    self.drugDeliver_btn.configure(state = 'disabled', text="รอหุ่นยนต์พร้อมใช้งาน...")
                    self.drugDeliver_btn.pack_configure(ipadx = 10)
            except Exception:
                pass

        self.after(1000, self.update_btn)

    def on_display(self):
        """packing the frame to set the cursor."""
        self.closeApp_stacking = 3
        self.pack(fill = 'both', expand = True)
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)

    def _on_ArtronClick(self):

        print("page: Main page > Artron Button Clicked.")
        self.closeApp_stacking -= 1
        if self.closeApp_stacking == 0:
            try:
                self.pages['topbar'].mqtt.stop() 
                self.pages['barcode_page'].qr_scanner.disconnect()
            except Exception as e:
                print(f"Error stopping services: {e}")
            self.parent.master.destroy()