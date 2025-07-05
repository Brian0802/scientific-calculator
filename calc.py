import customtkinter as ctk
import math
import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root: ctk.CTk):
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        # Create main window
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        
        # Calculator state
        self.display_var = tk.StringVar(value="0")
        self.previous_value = None
        self.operation = None
        self.waiting_for_operand = False
        self.is_degrees = True
        self.memory = 0
        self.is_second_function = False
        
        self.create_widgets()
        self.setup_keybindings()
        
    def create_widgets(self):
        
        # Display
        display_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        display_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        self.display_label = ctk.CTkLabel(display_frame, textvariable=self.display_var,
                                        font=("Arial", 36, "bold"), anchor="e",
                                        height=60)
        self.display_label.pack(fill="x")
        
        # Degree/Radian toggle
        deg_rad_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        deg_rad_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.deg_btn = ctk.CTkButton(deg_rad_frame, text="DEG", width=60, height=30,
                                   command=self.set_degrees)
        self.deg_btn.pack(side="left", padx=(0, 5))
        
        self.rad_btn = ctk.CTkButton(deg_rad_frame, text="RAD", width=60, height=30,
                                   command=self.set_radians, fg_color="gray30")
        self.rad_btn.pack(side="left")
        
        # Memory row
        memory_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        memory_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        memory_buttons = [
            ("MC", self.memory_clear, "gray30"),
            ("MR", self.memory_recall, "gray30"),
            ("M+", self.memory_add, "gray50"),
            ("M−", self.memory_subtract, "gray50"),
            ("MS", self.memory_store, "gray50"),
            ("M⌄", None, "gray30")
        ]
        
        for i, (text, command, color) in enumerate(memory_buttons):
            btn = ctk.CTkButton(memory_frame, text=text, width=55, height=35,
                              command=command, fg_color=color)
            btn.pack(side="left", padx=2)
        
        # Function categories
        func_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        func_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        trig_btn = ctk.CTkButton(func_frame, text="📐 Trigonometry ⌄", width=190, height=35,
                               anchor="w", command=self.toggle_trig)
        trig_btn.pack(side="left", padx=(0, 5))
        
        func_btn = ctk.CTkButton(func_frame, text="f Function ⌄", width=190, height=35,
                               anchor="w", command=self.toggle_func)
        func_btn.pack(side="left")
        
        # Main button grid
        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.create_button_grid()
        
    def create_button_grid(self):
        # Button layout (6 rows, 5 columns)
        buttons = [
            # Row 1
            [("2ⁿᵈ", self.second_function), ("π", lambda: self.input_constant(math.pi)), 
             ("e", lambda: self.input_constant(math.e)), ("C", self.clear), ("⌫", self.backspace)],
            
            # Row 2
            [("x²", lambda: self.unary_operation("square")), ("¹∕ₓ", lambda: self.unary_operation("reciprocal")),
             ("|x|", lambda: self.unary_operation("abs")), ("exp", lambda: self.unary_operation("exp")),
             ("mod", lambda: self.binary_operation("mod"))],
            
            # Row 3
            [("²√x", lambda: self.unary_operation("sqrt")), ("(", lambda: self.input_text("(")),
             (")", lambda: self.input_text(")")), ("n!", lambda: self.unary_operation("factorial")),
             ("÷", lambda: self.binary_operation("÷"))],
            
            # Row 4
            [("xʸ", lambda: self.binary_operation("power")), ("7", lambda: self.input_number(7)),
             ("8", lambda: self.input_number(8)), ("9", lambda: self.input_number(9)),
             ("×", lambda: self.binary_operation("×"))],
            
            # Row 5
            [("10ˣ", lambda: self.unary_operation("10power")), ("4", lambda: self.input_number(4)),
             ("5", lambda: self.input_number(5)), ("6", lambda: self.input_number(6)),
             ("−", lambda: self.binary_operation("−"))],
            
            # Row 6
            [("log", lambda: self.unary_operation("log")), ("1", lambda: self.input_number(1)),
             ("2", lambda: self.input_number(2)), ("3", lambda: self.input_number(3)),
             ("+", lambda: self.binary_operation("+"))],
            
            # Row 7
            [("ln", lambda: self.unary_operation("ln")), ("+/−", self.plus_minus),
             ("0", lambda: self.input_number(0)), (".", self.input_decimal),
             ("=", self.calculate)]
        ]
        
        for row, button_row in enumerate(buttons):
            for col, (text, command) in enumerate(button_row):
                # Special styling for different button types
                if text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    fg_color = "gray20"
                    hover_color = "gray30"
                elif text in ["+", "−", "×", "÷", "="]:
                    fg_color = "#1f538d" if text == "=" else "gray40"
                    hover_color = "#2d5aa0" if text == "=" else "gray50"
                else:
                    fg_color = "gray30"
                    hover_color = "gray40"
                
                btn = ctk.CTkButton(self.button_frame, text=text, width=70, height=50,
                                  command=command, fg_color=fg_color, hover_color=hover_color,
                                  font=("Arial", 14))
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # Configure grid weights
        for i in range(7):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_columnconfigure(i, weight=1)
    
    def setup_keybindings(self):
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
    
    def on_key_press(self, event):
        key = event.char
        if key.isdigit():
            self.input_number(int(key))
        elif key in "+-*/":
            op_map = {"+": "+", "-": "−", "*": "×", "/": "÷"}
            self.binary_operation(op_map[key])
        elif key == ".":
            self.input_decimal()
        elif key == "=":
            self.calculate()
        elif key == "\r":  # Enter key
            self.calculate()
        elif key == "\x08":  # Backspace
            self.backspace()
        elif key.lower() == "c":
            self.clear()
    
    def input_number(self, num):
        if self.waiting_for_operand:
            self.display_var.set(str(num))
            self.waiting_for_operand = False
        else:
            current = self.display_var.get()
            if current == "0":
                self.display_var.set(str(num))
            else:
                self.display_var.set(current + str(num))
    
    def input_decimal(self):
        if self.waiting_for_operand:
            self.display_var.set("0.")
            self.waiting_for_operand = False
        else:
            current = self.display_var.get()
            if "." not in current:
                self.display_var.set(current + ".")
    
    def input_text(self, text):
        if self.waiting_for_operand:
            self.display_var.set(text)
            self.waiting_for_operand = False
        else:
            current = self.display_var.get()
            self.display_var.set(current + text)
    
    def input_constant(self, value):
        self.display_var.set(str(value))
        self.waiting_for_operand = True
    
    def plus_minus(self):
        current = float(self.display_var.get())
        self.display_var.set(str(-current))
    
    def clear(self):
        self.display_var.set("0")
        self.previous_value = None
        self.operation = None
        self.waiting_for_operand = False
    
    def backspace(self):
        current = self.display_var.get()
        if len(current) > 1:
            self.display_var.set(current[:-1])
        else:
            self.display_var.set("0")
    
    def binary_operation(self, op):
        try:
            current = float(self.display_var.get())
            
            if self.previous_value is not None and self.operation and not self.waiting_for_operand:
                result = self.perform_calculation(self.previous_value, current, self.operation)
                self.display_var.set(str(result))
                self.previous_value = result
            else:
                self.previous_value = current
            
            self.operation = op
            self.waiting_for_operand = True
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
    
    def unary_operation(self, op):
        try:
            current = float(self.display_var.get())
            
            if op == "square":
                result = current ** 2
            elif op == "reciprocal":
                if current == 0:
                    raise ValueError("Cannot divide by zero")
                result = 1 / current
            elif op == "abs":
                result = abs(current)
            elif op == "exp":
                result = math.exp(current)
            elif op == "sqrt":
                if current < 0:
                    raise ValueError("Cannot take square root of negative number")
                result = math.sqrt(current)
            elif op == "factorial":
                if current < 0 or current != int(current):
                    raise ValueError("Factorial only defined for non-negative integers")
                result = math.factorial(int(current))
            elif op == "10power":
                result = 10 ** current
            elif op == "log":
                if current <= 0:
                    raise ValueError("Logarithm undefined for non-positive numbers")
                result = math.log10(current)
            elif op == "ln":
                if current <= 0:
                    raise ValueError("Natural logarithm undefined for non-positive numbers")
                result = math.log(current)
            elif op == "sin":
                angle = math.radians(current) if self.is_degrees else current
                result = math.sin(angle)
            elif op == "cos":
                angle = math.radians(current) if self.is_degrees else current
                result = math.cos(angle)
            elif op == "tan":
                angle = math.radians(current) if self.is_degrees else current
                result = math.tan(angle)
            else:
                return
            
            self.display_var.set(str(result))
            self.waiting_for_operand = True
            
        except (ValueError, OverflowError) as e:
            messagebox.showerror("Error", str(e))
    
    def calculate(self):
        if self.operation and self.previous_value is not None:
            try:
                current = float(self.display_var.get())
                result = self.perform_calculation(self.previous_value, current, self.operation)
                self.display_var.set(str(result))
                self.previous_value = None
                self.operation = None
                self.waiting_for_operand = True
            except (ValueError, ZeroDivisionError, OverflowError) as e:
                messagebox.showerror("Error", str(e))
    
    def perform_calculation(self, first, second, operation):
        if operation == "+":
            return first + second
        elif operation == "−":
            return first - second
        elif operation == "×":
            return first * second
        elif operation == "÷":
            if second == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return first / second
        elif operation == "power":
            return first ** second
        elif operation == "mod":
            if second == 0:
                raise ZeroDivisionError("Cannot calculate modulo by zero")
            return first % second
        else:
            return second
    
    def set_degrees(self):
        self.is_degrees = True
        self.deg_btn.configure(fg_color="#1f538d")
        self.rad_btn.configure(fg_color="gray30")
    
    def set_radians(self):
        self.is_degrees = False
        self.rad_btn.configure(fg_color="#1f538d")
        self.deg_btn.configure(fg_color="gray30")
    
    def memory_clear(self):
        self.memory = 0
    
    def memory_recall(self):
        self.display_var.set(str(self.memory))
        self.waiting_for_operand = True
    
    def memory_add(self):
        try:
            current = float(self.display_var.get())
            self.memory += current
        except ValueError:
            pass
    
    def memory_subtract(self):
        try:
            current = float(self.display_var.get())
            self.memory -= current
        except ValueError:
            pass
    
    def memory_store(self):
        try:
            current = float(self.display_var.get())
            self.memory = current
        except ValueError:
            pass
    
    def second_function(self):
        self.is_second_function = not self.is_second_function
        # This would toggle between primary and secondary functions
        # For now, just toggle the state
        pass
    
    def toggle_trig(self):
        # Placeholder for trigonometry menu
        pass
    
    def toggle_func(self):
        # Placeholder for function menu
        pass
    
    def minimize_window(self):
        self.root.iconify()
    
    def maximize_window(self):
        if self.root.state() == "zoomed":
            self.root.state("normal")
        else:
            self.root.state("zoomed")