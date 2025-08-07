from tkinter import Tk
from ..gui.gui import InventoryUpdaterApp

def main():
    root = Tk()
    app = InventoryUpdaterApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
