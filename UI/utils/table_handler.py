import customtkinter as ctk
import textwrap
import json

class Table(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = ["ลำดับ", "ชื่อยา", "รายละเอียด"]

        # Create and place column headers
        for idx, col in enumerate(self.columns):
            header = ctk.CTkLabel(master=self, text=col, font=("Noto Sans Thai", 18, "bold"), text_color="#035E5A")
            header.grid(row=0, column=idx, padx=30, pady=15, sticky="nsew")

    def map_drugs_and_details(self, slot_data):
        """Extract and map drugs and details for the table."""
        mapped_data = {}
        drugs = slot_data.get("drugs", [])
        details = slot_data.get("detail", [])

        for idx, (drug, detail) in enumerate(zip(drugs, details), start=1):
            mapped_data[f"{idx}"] = {"drug": drug, "detail": detail}

        return mapped_data

    def update_table(self, slot_data):
        """Update the table with data from a specific slot."""
        # Map drugs and details
        mapped_data = self.map_drugs_and_details(slot_data)

        # Clear existing table content
        for widget in self.winfo_children():
            widget.destroy()

        # Redraw headers
        for idx, col in enumerate(self.columns):
            header = ctk.CTkLabel(master=self, text=col, font=("Noto Sans Thai", 18, "bold"), text_color="#035E5A")
            header.grid(row=0, column=idx, padx=30, pady=15, sticky="nsew")

        # Populate the table with data
        for row_idx, (index, drug_detail) in enumerate(mapped_data.items(), start=1):
            ctk.CTkLabel(master=self, text=index, font=("Noto Sans Thai", 18), text_color="#035E5A").grid(
                row=row_idx, column=0, padx=30, pady=10, sticky="nsew"
            )
            ctk.CTkLabel(master=self, text=drug_detail["drug"], font=("Noto Sans Thai", 18), text_color="#035E5A").grid(
                row=row_idx, column=1, padx=30, pady=10, sticky="nsew"
            )
            ctk.CTkLabel(master=self, text=self.wrap_text(drug_detail["detail"]), font=("Noto Sans Thai", 18), text_color="#035E5A").grid(
                row=row_idx, column=2, padx=30, pady=10, sticky="nsew"
            )

    def wrap_text(self, text, width=80):
        """Wrap text for better readability."""
        return "\n".join(textwrap.wrap(text, width))
