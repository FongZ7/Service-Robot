import customtkinter as ctk
from PIL import Image
from gui.top_bar import Topbar
from gui.main_page import Mainpage
from gui.verify_page import VerifyPage
from gui.slot_page import SlotPage
from gui.barcode_page import BarcodePage
from gui.check_drug_page import CheckDrugPage
from gui.import_page import ImportPage
from gui.export_page import ExportPage
from gui.drug_page import DrugPage
from gui.ongoing_page import RobotGoing
from gui.closedoornotify_page import CloseDoorNotify
from gui.re_slot_in_page import ReSlotInPage
from gui.re_check_drug_page import ReCheckDrugPage
from gui.history_page import HistoryPage
from gui.page_name import PageName 


class ServiceRobot(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Service Robot Rewrite")
        # Set window size to 1280x800 as requested
        self.geometry("1280x800")
        self.resizable(False, False)
        self.bind("<Escape>", self.close_window)
        self.configure(fg_color = "#FFFFFF", bg_color = "#FFFFFF")
        self.overrideredirect(True)
        # self.host_mqtt = '192.168.1.100'

        #top and content frame
        self.topbar_frame = ctk.CTkFrame(self, fg_color = self.cget('fg_color'), height = 80,corner_radius = 0)
        self.topbar_frame.pack(fill = 'x')

        self.content_frame = ctk.CTkFrame(self, fg_color=self.cget('fg_color'), bg_color="#FFFFFF",corner_radius = 0)
        self.content_frame.pack(expand = True,fill = 'both')

        #page element
        self.top_bar = Topbar(self.topbar_frame)
        self.main_page = Mainpage(self.content_frame)
        self.verify_page = VerifyPage(self.content_frame)
        self.slot_page = SlotPage(self.content_frame)
        self.barcode_page = BarcodePage(self.content_frame)
        self.checkDrugsIn_page = CheckDrugPage(self.content_frame)
        self.import_page = ImportPage(self.content_frame)
        self.drug_page = DrugPage(self.content_frame)
        self.export_page = ExportPage(self.content_frame)
        self.ongoing_page = RobotGoing(self.content_frame)
        self.notify_page = CloseDoorNotify(self.content_frame)
        self.reSlot_page = ReSlotInPage(self.content_frame)
        self.reCheckDrug_page = ReCheckDrugPage(self.content_frame)
        self.history_page = HistoryPage(self.content_frame)

        ##################### New Method #####################
        #pages used for top bar.
        self.topbar_collection = {
            'main_page' :           self.main_page,
            'ongoing_page' :        self.ongoing_page,
            'barcode_page' :        self.barcode_page,
        }

        #page used for main page.
        self.main_page_collection = {
            'verify_page' :         self.verify_page,
            'ongoing_page' :        self.ongoing_page,
            'reSlot_page' :         self.reSlot_page,
            'topbar' :              self.top_bar,
            'barcode_page' :        self.barcode_page,
            'history_page' :        self.history_page,
        }

        #page used for verify page.
        self.verify_page_collection = {
            'main_page' :           self.main_page,
            'slot_page' :           self.slot_page,
        }

        #page used for slot page.
        self.slot_page_collection = {
            'main_page' :           self.main_page,
            'barcode_page' :        self.barcode_page,
        }


        #page used for Barcode page.
        self.barcode_page_collection = {
            'checkDrugsIn_page' :   self.checkDrugsIn_page,
            'drug_page' :           self.drug_page,
            'slot_page' :           self.slot_page,
        }

        #page used for check drug page.
        self.checkDrug_page_collection = {
            'barcode_page' :        self.barcode_page,
            'import_page' :         self.import_page,
        }
        
        #page used for import page.
        self.import_page_collection = {
            'notify_page' :         self.notify_page,
        }

        #page used for drug page.
        self.drug_page_collection = {
            'export_page' :         self.export_page,
            'main_page' :           self.main_page,
        }

        #page used for export page.
        self.export_page_collection = {
            'notify_page' :         self.notify_page,
        }


        #page used for ongoing page.
        self.ongoing_page_collection = {
            'main_page' :           self.main_page,
            'topbar' :              self.top_bar,
        }

        #page used for notify page.
        self.notify_page_collection = {
            'main_page' :           self.main_page,
        }

        #page used for reslot page.
        self.reSlot_page_collection = {
            'recheckdrug_page':     self.reCheckDrug_page,
            'main_page' :           self.main_page,
        }

        #page used for recheckdrug page.
        self.reCheckDrug_page_collection = {
            'reSlot_page' :         self.reSlot_page,
            'main_page' :           self.main_page,
        }

        #page used for history page.
        self.history_page_collection = {
            'main_page' :   self.main_page
        }

        
        #set "pages" parameter to each page
        self.top_bar.pages = self.topbar_collection
        self.main_page.pages = self.main_page_collection
        self.checkDrugsIn_page.pages = self.checkDrug_page_collection
        self.verify_page.pages = self.verify_page_collection
        self.slot_page.pages = self.slot_page_collection
        self.barcode_page.pages = self.barcode_page_collection
        self.import_page.pages = self.import_page_collection
        self.export_page.pages = self.export_page_collection
        self.drug_page.pages = self.drug_page_collection
        self.ongoing_page.pages = self.ongoing_page_collection
        self.notify_page.pages = self.notify_page_collection
        self.reSlot_page.pages = self.reSlot_page_collection
        self.reCheckDrug_page.pages = self.reCheckDrug_page_collection
        self.history_page.pages = self.history_page_collection

        #begin first page.
        self.top_bar.pack(fill='x')
        self.main_page.on_display()

    # def close_window(self, event=None) -> None:
    #     try:
    #         # if hasattr(self, 'barcode_page') and hasattr(self.barcode_page, 'qr_scanner'):
    #         #     self.barcode_page.qr_scanner.disconnect()
            
    #         # # เพิ่มการปิดกล้องของ VerifyPage
    #         # if hasattr(self, 'verify_page') and hasattr(self.verify_page, 'stop_camera'):
    #         #     self.verify_page.stop_camera()
                
    #         # ปิด MQTT
    #         if hasattr(self, 'top_bar') and hasattr(self.top_bar, 'mqtt') and self.top_bar.mqtt:
    #             self.top_bar.mqtt.stop()
                
    #     except Exception as e:
    #         print(f"Error disconnecting devices: {e}")
    #     self.destroy()

    def close_window(self, event=None) -> None:
        # self.barcode_page.qr_scanner.disconnect()
        self.destroy()

if __name__ == "__main__":
    try:
        app = ServiceRobot()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")