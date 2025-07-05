# Create and run the calculator
from calc import Calculator
import customtkinter as ctk

if __name__ == "__main__":
    root = ctk.CTk()
    root.iconbitmap()
    calculator = Calculator(root)
    root.mainloop()
