import customtkinter as ctk
from PIL import Image, ImageTk 
from tkinter import Frame, Button 
from utils.slot_handler import TheSlot
from utils.mockup_data import mockup_data, data
from utils.api_handler import get_api_data, post_api_data

try:
    from utils.popup.general_popup import GeneralPopup
    from utils.popup.slot_on_problem import SlotOnProblemPopup
except ImportError:
    try:
        from gui.general_popup import GeneralPopup
        from gui.slot_on_problem import SlotOnProblemPopup
    except ImportError:
        print("Error: Could not import Popups.")
# ----------------------

class SlotPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        print("page: Slot page > init!")

        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF")
        
        self.branch = "in"
        self.pages = None
        self.slots = []

        self.slot_key = {"slot": 1}
        self.takeout_key = {"status": "takeout"}
        self.opengate_key = {"status": 1}
        self.closegate_key = {"status": 0}

        self.load_images()
        self.get_apidata()
        self.create_widgets()

    def load_images(self):
        try:

            pil_back = Image.open(r"C:\Service_Robot\UI\assets\slot_page\back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)

            self.ward_img = ctk.CTkImage(light_image=Image.open(r"C:\Service_Robot\UI\assets\slot_page\wardList.png"), size=(860, 110))
        except Exception as e:
            print(f"Error loading images in SlotPage: {e}")
            self.back_img = None
            self.ward_img = None

    def create_widgets(self):

        self.back_btn = Button(
            master=self,
            text="",
            image=self.back_img,
            borderwidth=0,
            background="#FFFFFF",
            highlightthickness=0,
            activebackground="#FFFFFF",
            command=lambda: self.back()
        )
        self.back_btn.place(relx=0.00, rely=0.06)

        self.guide_text = ctk.CTkLabel(
            self,
            text="เลือกช่องว่างสำหรับใส่ยา",
            font=("Noto Sans Thai", 24, "bold"),
            text_color='#035E5A',
            bg_color="transparent"
        )
        self.guide_text.place(relx=0.10, rely=0.065)

        self.freeSlot = ctk.CTkLabel(
            self,
            text=f"ช่องว่าง {self._count_blank_slots()} ช่อง",
            font=("Noto Sans Thai", 24, "bold"),
            text_color='#035E5A',
            bg_color="transparent"
        )
        self.freeSlot.place(relx=0.95, rely=0.07, anchor="ne")

        self.slotFrame = Frame(self, background="#FFFFFF")
        self.slotFrame.place(relx=0.5, rely=0.47, anchor="center")

        self.row_1 = Frame(self.slotFrame, background="#FFFFFF")
        self.row_1.pack()

        if not hasattr(self, 'plot_data') or not self.plot_data:
             self.plot_data = data

        for i in range(1, 3):
            slot_data = self.plot_data.get(f'slot{i}', {})
            slot = TheSlot(master=self.row_1, slot_id=i, branch=self.branch, slotData=slot_data)

            slot.pack(side='left', padx=40, pady=20)
            self.slots.append(slot)


        if self.ward_img:
            self.legend_label = ctk.CTkLabel(
                self, 
                text="", 
                image=self.ward_img,
                bg_color="transparent"
            )
            self.legend_label.place(relx=0.5, rely=0.98, anchor="s")

    def set_branch(self, branch):
        self.branch = branch
        guide_text = 'เลือกช่องว่างสำหรับใส่ยา' if branch == 'in' else 'เลือกช่องสำหรับนำยาออก'
        self.guide_text.configure(text=guide_text)

    def set_Slot(self):
        self.get_apidata()
        self.freeSlot.configure(text=f"ช่องว่าง {self._count_blank_slots()} ช่อง")

        for i, slot in enumerate(self.slots, start=1):
            slot.slotData = self.plot_data.get(f'slot{i}', {})
            slot.config_parameter()
            slot.set_slot()

            cmd = None
            if self.branch == "in":
                if slot.Isblank:
                    cmd = lambda x=i: self.goto_barcodepage(slotID=x)
                elif not slot.Isblank and slot.IsReturn:
                    cmd = lambda x=i: self._on_return(slotID=x)
                else:
                    cmd = self.notify_fill
            else: # branch out
                if not slot.Isblank:
                    cmd = lambda x=i: self.goto_barcodepage(slotID=x)
                else:
                    cmd = self.notify_cant_fill
            
            slot.bedNo_btn.configure(command=cmd)
            slot.configure(command=cmd)

    def get_apidata(self):
        try:
            self.plot_data = get_api_data('slot')

            valid = isinstance(self.plot_data, dict) and any(k.startswith('slot') for k in self.plot_data.keys())
            if not valid:
                print("Warning: API Data invalid. Using dummy data.")
                self.plot_data = data
        except Exception as e:
            print(f"Error in get_apidata: {e}")
            self.plot_data = data

    def goto_barcodepage(self, slotID):
        print(f"page: Slot page > goto barccode page for slot no.{slotID}")
        self.pack_forget()
        self.slot_key['slot'] = slotID

        post_api_data('select_slot', self.slot_key)

        if self.pages and 'barcode_page' in self.pages:
            barcode_page = self.pages['barcode_page']
            barcode_page.slot_id = slotID
            barcode_page.pack(fill='both')

            if self.branch == "in":
                barcode_page.setbranch_in()
                barcode_page.on_import_qr_event()
            else:
                barcode_page.setbranch_out()
                barcode_page.on_export_qr_event()
                barcode_page.on_export_barcode_call(slotID)
            
            try:
                if hasattr(barcode_page, 'qr_scanner') and not getattr(barcode_page.qr_scanner, 'disabled', True):
                    barcode_page.qr_scanner.connect()
            except Exception:
                pass
            
            barcode_page.start_animation()
            if hasattr(barcode_page, 'on_display'):
                barcode_page.on_display()
        else:
            print("Error: Barcode Page not found in self.pages")

    def notify_fill(self):
        self.used_popup = GeneralPopup(self.master)
        self.used_popup.set_used_popup()

    def notify_cant_fill(self):
        self.cant_used_popup = GeneralPopup(self.master)
        self.cant_used_popup.set_cant_used_popup()

    def _on_return(self, slotID):
        self.return_popup = SlotOnProblemPopup(self.master)
        self.return_popup.fetch_data(self.plot_data, slotID)
        self.return_popup.takeOutBtn.configure(command=lambda: self._on_takeout_popup_click(slotID))

    def _count_blank_slots(self):
        if not hasattr(self, 'plot_data') or not self.plot_data: return 0
        blank_slots = 0

        for i in range(1, 3):
            key = f'slot{i}'
            if key in self.plot_data:
                slot = self.plot_data[key]
                if (slot.get('bed_number') is None and not slot.get('drugs') and
                    slot.get('hn') is None):
                    blank_slots += 1
        return blank_slots

    def _on_takeout_popup_click(self, slotID):
        self.slot_key['slot'] = slotID
        post_api_data('select_slot', self.slot_key)
        post_api_data('in_out', self.takeout_key)
        
        data = self.plot_data[f"slot{slotID}"]
        post_data = {'hn': data['hn'], 'IsReturn': False}
        post_api_data('qr_scan', post_data)
        
        post_api_data('gate', self.opengate_key)
        post_api_data('gate', self.closegate_key)
        
        self.return_popup.destroy()

        self.ack_slot_popup = GeneralPopup(self.master)
        self.ack_slot_popup.set_problem_slot_popup()
        self.ack_slot_popup.returnMainBtn.configure(command=self._on_ackclick)

    def _on_ackclick(self):
        self.ack_slot_popup.destroy()
        self.set_Slot()

    def on_display(self):
        self.pack(fill='both', expand=True)
        self.set_Slot()
        self.after(100, self.set_cursor_position, 0, 0)

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)

    def back(self):
        print("page: Slot Page > back to Main page.")
        self.pack_forget()
        if self.pages and 'main_page' in self.pages:
            self.pages['main_page'].on_display()