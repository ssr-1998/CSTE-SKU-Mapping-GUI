import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from ..data_preprocessing.sku_mapper import SkuMapper


class InventoryUpdaterApp:
    def __init__(self, root):
        self.root = root
        root.title("SKU Inventory Updater")

        self.mapper = SkuMapper(base_dir='.')
        loaded = self.mapper.load_mappings()
        if not loaded:
            messagebox.showerror("Error", "Failed to load mappings. Check logs.")
            root.destroy()
            return

        self.label = tk.Label(root, text="Select sales file (.csv or .xlsx):")
        self.label.pack(pady=10)

        self.btn_browse = tk.Button(root, text="Browse File", command=self.load_sales_file)
        self.btn_browse.pack(pady=5)

        self.text = tk.Text(root, height=15, width=60)
        self.text.pack(pady=10)

        self.btn_save = tk.Button(root, text="Save Updated Inventory", command=self.save_inventory, state=tk.DISABLED)
        self.btn_save.pack(pady=5)

        self.sales_df = None


    def load_sales_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return

        # Load Sales Data with SKU and Quantity Columns
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            # Check required columns
            cols = [col.strip() for col in df.columns]
            if 'SKU' not in cols or 'Quantity' not in cols:
                messagebox.showerror("Error", "File must contain 'SKU' and 'Quantity' columns.")
                return
            df.columns = cols  # clean trimmed names

            self.sales_df = df[['SKU', 'Quantity']].copy()
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, "Loaded sales file with {} rows.\n\n".format(len(self.sales_df)))

            self.process_sales()
            self.btn_save.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", "Failed to load file:\n{}".format(str(e)))


    def process_sales(self):
        self.text.insert(tk.END, "Processing sales and updating inventory...\n")
        for index, row in self.sales_df.iterrows():
            sku = row['SKU']
            quantity = row['Quantity']
            # Defensive conversion if quantity is float
            try:
                quantity = int(quantity)
            except:
                self.text.insert(tk.END, "Warning: Could not convert quantity '{}' to int at row {}\n".format(quantity, index))
                continue

            self.mapper.reduce_inventory_for_sale(sku, quantity)

        self.text.insert(tk.END, "Inventory updated in memory.\n")


    def save_inventory(self):
        # Create 'artifacts' folder if not existing
        os.makedirs('artifacts', exist_ok=True)
        save_path = os.path.join('artifacts', 'Updated_Inventory.xlsx')

        try:
            # Save inventory DataFrame to Excel
            self.mapper.inventory.to_excel(save_path, index=False)
            messagebox.showinfo("Saved", "Updated inventory saved to:\n{}".format(save_path))
        except Exception as e:
            messagebox.showerror("Error", "Failed to save updated inventory:\n{}".format(str(e)))
