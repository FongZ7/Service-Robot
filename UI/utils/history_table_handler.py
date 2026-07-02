import customtkinter as ctk
import textwrap

class HistoryTable(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = ["เวลา", "ชื่อผู้ป่วย", "ชื่อยา", "รายละเอียด", "สถานะ"]

        for i in range(len(self.columns)):
            self.grid_columnconfigure(i, weight=1)

        for idx, col in enumerate(self.columns):
            header = ctk.CTkLabel(master=self, text=col, font=("Noto Sans Thai", 18, "bold"), text_color="#035E5A")
            header.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")

    def extract_by_prefix(self, data_dict, prefix):
        """Extract the first value that starts with the given prefix."""
        for key, value in data_dict.items():
            if key.startswith(prefix):
                return value
        return "-"


    def wrap_text(self, text, width=20):
        """Wrap text for better readability."""
        return "\n".join(textwrap.wrap(str(text), width))

    def update_table(self, data_list):
        """Update the table with a list of entries with dynamic keys."""

        for widget in self.winfo_children():
            widget.destroy()

        for idx, col in enumerate(self.columns):
            header = ctk.CTkLabel(master=self, text=col, font=("Noto Sans Thai", 18, "bold"), text_color="#035E5A")
            header.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")

        for row_idx, entry in enumerate(data_list, start=1):
            time = self.extract_by_prefix(entry, "time")
            name = self.extract_by_prefix(entry, "name")
            drug = self.extract_by_prefix(entry, "drug")
            detail = self.extract_by_prefix(entry, "detail")
            status = self.extract_by_prefix(entry, "status")

            
            ctk.CTkLabel(master=self, text=time, font=("Noto Sans Thai", 16), text_color="#035E5A").grid(
                row=row_idx, column=0, padx=10, pady=8, sticky="nsew"
            )
            ctk.CTkLabel(master=self, text=name, font=("Noto Sans Thai", 16), text_color="#035E5A").grid(
                row=row_idx, column=1, padx=10, pady=8, sticky="nsew"
            )
            ctk.CTkLabel(master=self, text=self.wrap_text(drug), font=("Noto Sans Thai", 16), text_color="#035E5A").grid(
                row=row_idx, column=2, padx=10, pady=8, sticky="nsew"
            )
            ctk.CTkLabel(master=self, text=self.wrap_text(detail), font=("Noto Sans Thai", 16), text_color="#035E5A").grid(
                row=row_idx, column=3, padx=10, pady=8, sticky="w"
            )
            ctk.CTkLabel(master=self, text=self.wrap_text(status), font=("Noto Sans Thai", 16), text_color="#035E5A").grid(
                row=row_idx, column=4, padx=10, pady=8, sticky="nsew"
            )