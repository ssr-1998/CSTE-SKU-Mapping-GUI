# CSTE SKU Mapping GUI Application

This repository contains the code for a Python-based GUI application that handles the core SKU to MSKU mapping logic and inventory updating for CSTE Group, as part of the Assignment received for a Full-Stack Developer Role.

## Features Implemented

- Loads SKU–MSKU, Combo SKUs, and Current Inventory Data from Excel files.
- Identifies whether a Sold SKU is a Single Product or a Combo.
- Maps SKUs to their Master SKUs (MSKU) and updates the Opening Stock in Inventory accordingly.
- Supports Combo SKU Expansion and Inventory Reduction for each component SKU.
- Logs processing details and errors with a rotating log file approach.
- GUI built with Tkinter allowing users to upload sales files (`.csv` or `.xlsx`), process them, and save updated inventory.
- Stores updated inventory in an `artifacts/` folder as an Excel file for further use.

## Project Structure

- `src/data_processing/sku_mapper.py` — Core SKU mapping and inventory update logic.
- `src/gui/gui.py` — GUI application code.
- `src/gui/app.py` — Application entry point to launch the GUI.
- `src/utils/logger.py` — Logger setup for robust logging.
- `data/mappings/` — Folder to hold all mapping and inventory Excel files.
- `data/sales/` — Folder to hold sales data files.
- `artifacts/` — Output folder where updated inventory files are saved.
- `Dockerfile` — For containerizing the application.

## How to Run

1. Clone the repo.
2. Place your mapping and sales files in the corresponding folders under `data/`.
3. Build and run the Docker container (instructions below) or run locally after installing dependencies.
4. Use the GUI to upload sales data files and process inventory updates.
5. Save updated inventory to `artifacts/Updated_Inventory.xlsx`.

## Dependencies

- Python 3.11.9
- pandas
- openpyxl
- tkinter (usually bundled with Python)
- Additional dependencies as listed in `requirements.txt`

## License

This project is for assignment purposes only.
