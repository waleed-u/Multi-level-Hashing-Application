import tkinter as tk
from tkinter import messagebox
from database import Database

class SignupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Sign Up")
        self.geometry("300x250")
        self.resizable(False, False)
        
        self.db = Database()
        self.create_widgets()
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Username
        tk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Password
        tk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Confirm Password
        tk.Label(self, text="Confirm Password:").grid(row=2, column=0, padx=10, pady=10)
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Sign Up Button
        self.signup_button = tk.Button(self, text="Sign Up", command=self.signup)
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=20)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if self.db.add_user(username, password):
            messagebox.showinfo("Success", "Account created successfully!")
            self.destroy()
        else:
            messagebox.showerror("Error", "Username already exists")
