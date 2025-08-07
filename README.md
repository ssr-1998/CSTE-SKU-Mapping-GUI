# CSTE SKU Mapping GUI Application

This repository contains the code for a Python-based GUI application that handles the core SKU to MSKU mapping logic and inventory updating for CSTE Group, as part of the assignment received for a full-stack developer role.

## Features Implemented

- Loads SKU–MSKU, combo SKUs, and current inventory data from Excel files.
- Identifies whether a sold SKU is a single product or a combo.
- Maps SKUs to their master SKUs (MSKU) and updates the opening stock in inventory accordingly.
- Supports combo SKU expansion and inventory reduction for each component SKU.
- Logs processing details and errors.
- GUI built with Tkinter allowing users to upload sales files (`.csv` or `.xlsx`), process them, and save updated inventory.
- Stores updated inventory in an `artifacts/` folder as an Excel file for further use.

## Project Structure (Simplified)

- `src/data_processing/sku_mapper.py` — Core SKU mapping and inventory update logic.
- `src/gui/gui.py` — GUI application code.
- `src/gui/app.py` — Application entry point to launch the GUI.
- `src/utils/logger.py` — Logger setup for robust logging.
- `data/mappings/` — Folder to hold all mapping and inventory Excel files.
- `data/sales/` — Folder to hold sales data files.
- `artifacts/` — Output folder where updated inventory files are saved.

## How to Run

1. Clone the repo.
2. Place your mapping and sales files in the corresponding folders under `data/`.
3. Run the GUI app locally with:

```bash
python src/gui/app.py
```

4. Use the GUI to upload sales data files and process inventory updates.
5. Save updated inventory to `artifacts/Updated_Inventory.xlsx`.

## Dependencies

- Python 3.11.9
- pandas  
- openpyxl  
- tkinter

---

