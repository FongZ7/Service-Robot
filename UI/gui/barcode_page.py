import customtkinter as ctk
from tkinter import PhotoImage, Frame, Button
from PIL import Image, ImageTk
import json
from utils.mockup_data import mockup_data
from utils.api_handler import post_api_data, get_api_data
from utils.animation.wait_barcode import BarcodeAnimate
from utils.popup.slide_popupExport import SlidePopupExport
from utils.popup.slide_popupImport import SlidePopupImport
from utils.popup.general_popup import GeneralPopup

# --- Mock QRScanner Class (กรณีไม่มี Hardware) ---
class MockQRScanner:
    def __init__(self): pass
    def wait_for_data(self): return False
    def wait_for_hn(self): return False
    def get_data(self): return ""
    def disconnect(self): pass

# Try importing real scanner, else use mock
try:
    from utils.qr_handler import QRScanner
except ImportError:
    QRScanner = MockQRScanner

class BarcodePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # 1. กำหนดขนาดให้ถูกต้อง 1280x800
        self.configure(width=1280, height=800, corner_radius=0, fg_color="#FFFFFF")
        self.pages = None
        self.branch = "in"
        self.slot_id = None 

        self.open_slot_key = {'status': 1}
        self.close_slot_key = {'status': 0} 
        
        self.slot_detail = None
        self.export_plot_data = {
            'name': None, 
            'hn': None
        }

        self.font_styte = {'font': ("Noto Sans Thai", 24, "bold"), 'text_color': '#035E5A'}
        print("page: Barcode page > init!")
        
        # Initialize Scanner safely
        try:
            if QRScanner:
                self.qr_scanner = QRScanner()
            else:
                self.qr_scanner = None
        except Exception as e:
            print(f"Scanner Hardware Error (Using Mock): {e}")
            self.qr_scanner = None
        
        self.load_images()
        self.create_widgets()
        
        self.qr_data = {
            "qr_number": "900000178291111",
            "name": "นาง จันเพ็ง ผุกแสน",
            "drug": "Dophamine",
            "detail": "drip",
            "hn": "46608226",
            "location": "S049"
        }

    def load_images(self):
        try:
            pil_back = Image.open(r"C:\Service_Robot\UI\assets\barcode_import_page\back.png")
            resized_back = pil_back.resize((70, 55), Image.Resampling.LANCZOS)
            self.back_img = ImageTk.PhotoImage(resized_back)
        except Exception as e:
            print(f"Image Error: {e}")
            self.back_img = None
        
    def create_widgets(self):
        self.back_btn = Button(
            master=self, 
            text="", 
            image=self.back_img, 
            borderwidth=0,
            background=self.cget('fg_color'),
            highlightthickness=0,
            activebackground=self.cget('fg_color'),
            command=self.back
        )
        self.back_btn.place(relx=0.00, rely=0.04)

        self.content_frame = ctk.CTkFrame(self, width=700, height=500, fg_color="#FFFFFF")
        self.content_frame.place(relx=0.5, rely=0.55, anchor="center")

        self.animation = BarcodeAnimate(self.content_frame)
        self.animation.place(relx=0.5, rely=0.4, anchor="center")

        # [แก้ไข] เก็บ Label ลงตัวแปร self.lbl_instruction เพื่อให้ Bind Event ได้
        self.lbl_instruction = ctk.CTkLabel(self.content_frame, text='นำ QR code ของยามาแสดงตรงจุดสแกน', **self.font_styte)
        self.lbl_instruction.place(relx=0.5, rely=0.85, anchor="center")

        self.import_popup = SlidePopupImport(self)
        self.import_popup.confirm_btn.configure(command = self._on_confirm_popupclick)
        self.import_popup.add_btn.configure(command = self._on_add_popupclick)

        self.export_popup = SlidePopupExport(self)
        self.export_popup.confirm_btn.configure(command = self._on_confirm_popupclick)

        self.finish_btn = ctk.CTkButton(self.content_frame, 
                                        text="ไปหน้าสรุปรายการยา",
                                        font=("Noto Sans Thai", 18, "bold"),
                                        corner_radius=25,
                                        width=250,
                                        height=50,
                                        bg_color="#FFFFFF",
                                        fg_color="#035E5A",
                                        text_color="#FFFFFF",
                                        hover=True,
                                        hover_color="#67A7A4",
                                        command=self._on_finish_click
                                        )
        
        # --- [ส่วนสำคัญ] Binding Click Event ---
        self.bind("<Button-1>", self.on_screen_click)          # พื้นหลังหลัก
        self.content_frame.bind("<Button-1>", self.on_screen_click)  # พื้นหลังสีขาว
        self.animation.bind("<Button-1>", self.on_screen_click)      # พื้นที่ Animation
        self.lbl_instruction.bind("<Button-1>", self.on_screen_click)# ข้อความ
        
        # ผูกกับรูปภาพภายใน Animation (ถ้ามี)
        if hasattr(self.animation, 'label'):
            self.animation.label.bind("<Button-1>", self.on_screen_click)

    # --- ฟังก์ชันใหม่: คลิกหน้าจอแล้วไปต่อเลย ---
    def on_screen_click(self, event):
        
        print("Screen Clicked: Auto-processing scan data...")
        if hasattr(self.animation, 'stop_animation'):
            self.animation.stop_animation()

        if self.branch == "in":

            self.import_popup.config_popupDetail(self.qr_data)
            self._slide_popup_up()
        else:

            if self.slot_detail:
                self.qr_data['hn'] = self.slot_detail.get('hn', '000000')
                f_name = self.slot_detail.get('name', {}).get('first', '')
                l_name = self.slot_detail.get('name', {}).get('last', '')
                self.export_plot_data['name'] = f"{f_name} {l_name}"
                self.export_plot_data['hn'] = self.qr_data['hn']
                self.export_popup.config_popupDetail(self.export_plot_data)
                self._slide_popup_up()
            else:
                self.qr_data['hn'] = '000000'

    def setbranch_in(self):
        self.branch = "in"
    
    def setbranch_out(self):
        self.branch = "out"

    def start_animation(self):
        if hasattr(self.animation, 'start_animation'):
            self.animation.start_animation()

    # def simulate_scan_success(self):
    #     # ไม่ได้ใช้แล้ว
    #     pass

    def _slide_popup_up(self):
        if hasattr(self.animation, 'stop_animation'):
            self.animation.stop_animation()  
        if self.branch == 'in':
            self.import_popup.lift()   
            self.import_popup.slide_up()
        else:
            self.export_popup.lift()
            self.export_popup.slide_up()

    def _slide_popup_down(self):
        if hasattr(self.animation, 'start_animation'):
            self.animation.start_animation()
        self.import_popup.slide_down() if self.branch == "in" else self.export_popup.slide_down()

    def _on_confirm_popupclick(self):
        if hasattr(self.animation, 'stop_animation'):
            self.animation.stop_animation()

        if self.branch == "in":
            final_data = self.qr_data.copy()
            final_data['slot_id'] = self.slot_id 
            final_data['is_return'] = False
            final_data['why_return'] = None

            print(f"Confirming Import: Sending Mock Data to Slot {self.slot_id}...")

            postData = post_api_data('qr_scan', final_data) 

            self.import_popup.place_forget()
            self.import_popup.reset_pos()

            if postData.get("success", True): 
                print("Data posted successfully")
                self.finish_btn.place_forget()
                self.pack_forget()
                
                if self.pages and 'checkDrugsIn_page' in self.pages:
                    target_page = self.pages['checkDrugsIn_page']
                    target_page.slot_id = self.slot_id
                    target_page.update_table() 
                    target_page.pack(fill='both', expand=True)
                    target_page.on_display()
                else:
                    print("Error: checkDrugsIn_page not found in pages")
            else:
                print(f"Error posting data: {postData.get('error')}")
                self._on_api_error()

        else: # Export Branch
            self.export_popup.place_forget()
            self.export_popup.reset_pos()

            openGate = post_api_data('gate', self.open_slot_key)

            if openGate.get("success", True):
                print(f"Data posted successfully: Open Gate")
                self.pack_forget()
                
                if self.pages and 'drug_page' in self.pages:
                    target_page = self.pages['drug_page']
                    target_page.slot_id = self.slot_id
                    target_page.update_table()
                    target_page.pack()
                    target_page.on_display()
            else:
                print(f"Error posting data: {openGate.get('error')}")

    def _on_not_found_hn(self):
        self.export_popup.reset_pos()
        self.start_animation()
        self.export_popup.confirm_btn.configure(command = self._on_confirm_popupclick)

    def _on_add_popupclick(self):
        self.export_popup.reset_pos()
        self.import_popup.reset_pos()
        
        final_data = self.qr_data.copy()
        final_data['slot_id'] = self.slot_id
        final_data['is_return'] = False
        final_data['why_return'] = None
        
        postData = post_api_data('qr_scan', final_data)

        if postData.get("success", True):
            print(f"Data posted successfully")
            self.import_popup.reset_pos()
            self.finish_btn.place(relx = 0.5, rely = 0.85, anchor="center") 
            self.start_animation()
        else:
            print(f"Error posting data: {postData.get('error')}")
            self.start_animation()
            self._on_api_error()

    def on_import_qr_event(self):
        if self.qr_scanner is None:
            return 

        try:
            if self.qr_scanner.wait_for_data():
                data = self.qr_scanner.get_data()
                self.qr_data = json.loads(data)
                self.import_popup.config_popupDetail(self.qr_data)
                self._slide_popup_up()
                return
        except Exception as e:
            print(f"Error during QR event: {e}") 
            pass
        
        if hasattr(self, 'import_popup') and self.import_popup.winfo_exists():
            self.import_qr_after_id = self.import_popup.after(2000, self.on_import_qr_event)

    def on_export_qr_event(self):
        if self.qr_scanner is None:
            return

        try:
            if self.qr_scanner.wait_for_hn():
                data = self.qr_scanner.get_data()
                self.qr_data = json.loads(data)

        except Exception as e:
            pass
        
        if hasattr(self, 'export_popup') and self.export_popup.winfo_exists():
            self.export_qr_after_id = self.export_popup.after(2000, self.on_export_qr_event)

    def _on_finish_click(self):
        if hasattr(self.animation, 'stop_animation'):
            self.animation.stop_animation()
        self.pack_forget()
        self.finish_btn.place_forget()
        self.pages['checkDrugsIn_page'].slot_id = self.slot_id
        self.pages['checkDrugsIn_page'].update_table()
        self.pages['checkDrugsIn_page'].pack(fill='both', expand = True)
        self.pages['checkDrugsIn_page'].on_display()
        self.finish_btn.place_forget()

    def _process_qr_data(self, qr_data):
        qr_data['is_return'] = False 
        qr_data['why_return'] = None
        qr_data['slot_id'] = self.slot_id 
        return qr_data

    def back(self):     
        if self.branch == "in":
            self.import_popup.reset_pos()
            try:
                if hasattr(self, 'import_qr_after_id'):
                    self.import_popup.after_cancel(self.import_qr_after_id)
            except: pass
        else:   
            self.export_popup.reset_pos()
            try:
                if hasattr(self, 'export_qr_after_id'):
                    self.export_popup.after_cancel(self.export_qr_after_id)
            except: pass

        self.finish_btn.place_forget()
        self.pack_forget()
        if hasattr(self.animation, 'stop_animation'):
            self.animation.stop_animation()
        print(f"page: Barcode page > Goto SlotPage")
        self.pages['slot_page'].pack(fill='both')
        self.pages['slot_page'].set_Slot()

    def on_export_barcode_call(self, slotID):
        data = get_api_data('slot')
        if data and f"slot{slotID}" in data:
            self.slot_detail = data[f"slot{slotID}"]
        else:
            self.slot_detail = {"hn": "46608226", "name": {"first": "Test", "last": "Patient"}}

    def _volidate_hn(self, qr_hn):
        if self.slot_detail and self.slot_detail.get('hn') == qr_hn:
            return True
        return False

    def _on_api_error(self):
        self.api_error_popup = GeneralPopup(self.master)
        self.api_error_popup.set_api_error_popup()
        if self.branch == "in":
            self.import_popup.reset_pos()
        else:
            self.export_popup.reset_pos()

    def on_display(self):
        self.after(100, lambda: self.update())
        
        if self.branch == "in" and self.qr_scanner:
            self.on_import_qr_event()

    def set_cursor_position(self, x, y):
        self.update()
        self.event_generate("<Motion>", warp=True, x=x, y=y)