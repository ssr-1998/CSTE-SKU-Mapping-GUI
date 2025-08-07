import os
import pandas as pd
from ..utils.logger import setup_logger

class SkuMapper:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.msku_sku = None
        self.combo_skus = None
        self.inventory = None
        self.logger = setup_logger()


    def load_mappings(self):
        try:
            mappings_dir = os.path.join(self.base_dir, 'data', 'mappings')

            file_path = os.path.join(mappings_dir, "WMS-04-02.xlsx")

            xls = pd.ExcelFile(file_path, engine='openpyxl')

            # Load Inventory
            self.inventory = pd.read_excel(xls, sheet_name='Current Inventory ', header=1)

            # Load Combos SKUs
            self.combo_skus = pd.read_excel(xls, sheet_name='Combos skus')

            # Load MSKUs With SKUs
            self.msku_sku = pd.read_excel(xls, sheet_name='Msku With Skus')[['msku', 'sku']]

            self.logger.info("Mappings loaded Successfully.")
        except Exception as e:
            self.logger.error(f"Error loading mapping files: {e}")
            # Return False to indicate Partial Failure
            return False
        return True


    def get_msku(self, sku):
        """Return the MSKU for a given SKU. Returns None if not found."""
        try:
            res = self.msku_sku[self.msku_sku['sku'] == sku]
            if res.empty:
                return None
            return res.iloc[0]['msku']
        except Exception as e:
            self.logger.error("Error fetching MSKU for SKU '{}': {}".format(sku, e))
            return None


    def is_combo(self, sku):
        """Check if this SKU is a Combo SKU."""
        try:
            return sku in self.combo_skus['Combo '].values
        except Exception as e:
            self.logger.error("Error checking if SKU '{}' is combo: {}".format(sku, e))
            return False


    def get_combo_components(self, combo_sku):
        """List all component SKUs in a Combo SKU row."""
        try:
            row = self.combo_skus[self.combo_skus['Combo '] == combo_sku]

            if row.empty:
                self.logger.warning("Combo SKU '{}' not found.".format(combo_sku))
                return []
            components = []

            for idx in range(1, 15):
                col_name = f'SKU{idx}'
                if col_name in row.columns:
                    sku_val = row.iloc[0][col_name]
                    if pd.notnull(sku_val):
                        components.append(sku_val)

            return components
        except Exception as e:
            self.logger.error("Error getting components for Combo SKU '{}': {}".format(combo_sku, e))
            return []


    def reduce_inventory_for_sale(self, sold_sku, quantity_sold=1):
        """
        Given a Sold SKU and Quantity, reduce the Opening Stock in Inventory.
        Handles both individual SKUs and Combo SKUs.
        """
        try:
            # Check if SKU is a combo product
            if self.is_combo(sold_sku):

                # Get Component SKUs of the Combo
                component_skus = self.get_combo_components(sold_sku)
                
                if not component_skus:
                    self.logger.warning("Combo SKU '{}' has no components.".format(sold_sku))
                    return 
                
                # For each Component SKU, map it to MSKU and Reduce Stock
                for sku in component_skus:
                    msku = self.get_msku(sku)
                    if msku is None:
                        self.logger.warning("Component SKU '{}' from Combo '{}' not mapped to MSKU.".format(sku, sold_sku))
                        continue
                    self._reduce_msku_stock(msku, quantity_sold)
                    
            else:
                # Single SKU Case
                msku = self.get_msku(sold_sku)
                if msku is None:
                    self.logger.warning("SKU '{}' not mapped to MSKU.".format(sold_sku))
                    return
                self._reduce_msku_stock(msku, quantity_sold)
                
        except Exception as e:
            self.logger.error("Error reducing inventory for SKU '{}': {}".format(sold_sku, e))


    def _reduce_msku_stock(self, msku, quantity):
        """
        Helper Function to reduce Opening Stock for the given MSKU by Quantity.
        Updates the Inventory DataFrame and Opening Stock Totals.
        """
        try:
            # Find Inventory Row for MSKU
            idx = self.inventory.index[self.inventory['msku'] == msku]
            if idx.empty:
                self.logger.warning("MSKU '{}' not found in inventory.".format(msku))
                return
            
            idx = idx[0]
            
            # Reduce Opening Stock
            current_stock = self.inventory.at[idx, 'Opening Stock']
            updated_stock = current_stock - quantity
            
            if updated_stock < 0:
                self.logger.warning("Opening Stock for MSKU '{}' going below zero. Setting to 0.".format(msku))
                updated_stock = 0
            
            self.inventory.at[idx, 'Opening Stock'] = updated_stock
            
            # Reducing Stock in each Warehouse for MSKU.
            for warehouse_col in self.inventory.columns[4:]:
                current_wh_stock = self.inventory.at[idx, warehouse_col]
                new_wh_stock = max(current_wh_stock - quantity, 0)
                self.inventory.at[idx, warehouse_col] = new_wh_stock

            self.logger.info("Reduced Opening Stock for MSKU '{}' by {}. New stock: {}".format(msku, quantity, updated_stock))
            
        except Exception as e:
            self.logger.error("Failed to reduce stock for MSKU '{}': {}".format(msku, e))


# if __name__ == "__main__":
#     mapper = SkuMapper(base_dir='.')
#     success = mapper.load_mappings()
#     if not success:
#         print("Failed to load mappings.")
#         exit(1)
    
#     # Helper to Print Inventory for a SKU or MSKU before and after update
#     def print_inventory(msku):
#         row = mapper.inventory[mapper.inventory["msku"] == msku]
#         if row.empty:
#             print("MSKU '{}' not found in inventory.".format(msku))
#         else:
#             opening_stock = row.iloc[0]["Opening Stock"]
#             print("MSKU '{}' Opening Stock: {}".format(msku, opening_stock))
    
#     # Test inputs:
#     combo_sku = "Caaju_Compression_Travelkit_Blue"
#     print("Testing Combo SKU reduction for '{}'".format(combo_sku))
#     component_skus = mapper.get_combo_components(combo_sku)
#     print("Component SKUs: {}".format(component_skus))
#     for sku in component_skus:
#         msku = mapper.get_msku(sku)
#         if msku is not None:
#             print_inventory(msku)
    
#     # Reduce inventory by 1 for combo sold
#     mapper.reduce_inventory_for_sale(combo_sku, quantity_sold=1)
    
#     print("After reduction:")
#     for sku in component_skus:
#         msku = mapper.get_msku(sku)
#         if msku is not None:
#             print_inventory(msku)
    
#     print("\n------\n")

#     # Now test a single SKU reduction
#     single_sku = "CSTE_O0390_OT_Toiletry_Bottles"  # example; replace with an actual SKU from your mappings
#     print("Testing Single SKU reduction for '{}'".format(single_sku))
#     msku_single = mapper.get_msku(single_sku)
#     print_inventory(msku_single)

#     # Reduce inventory by 2 for single SKU sold
#     mapper.reduce_inventory_for_sale(single_sku, quantity_sold=2)
    
#     print("After reduction:")
#     print_inventory(msku_single)
