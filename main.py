import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from Tree.Models.Encoder import Encoder  # Importing Encoder for Merkle Tree functionality
from signature import generate_signature, verify_signature  # Importing Digital Signature Module
from login import LoginWindow
from signup import SignupWindow


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Authentication")
        self.geometry("300x200")
        self.current_user = None
        self.create_auth_widgets()
        self.center_window()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_auth_widgets(self):
        login_btn = tk.Button(self, text="Login", command=self.show_login)
        login_btn.pack(pady=20)
        
        signup_btn = tk.Button(self, text="Sign Up", command=self.show_signup)
        signup_btn.pack(pady=20)

    def show_login(self):
        LoginWindow(self)

    def show_signup(self):
        SignupWindow(self)

    def show_main_application(self):
        self.withdraw()  # Hide the auth window
        main_window = tk.Toplevel(self)
        app = MerkleSignatureApp(main_window)
        
        def on_closing():
            self.destroy()  # Close the entire application
            
        main_window.protocol("WM_DELETE_WINDOW", on_closing)


class MerkleSignatureApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Merkle Tree & Digital Signature App")
        self.grid(padx=10, pady=10)

        # Input Data Section
        tk.Label(self, text="Input Data:").grid(row=0, column=0, sticky="w")
        self.data_text = scrolledtext.ScrolledText(self, width=60, height=10)
        self.data_text.grid(row=0, column=1, columnspan=2)

        # File Upload Button
        self.upload_file_btn = tk.Button(self, text="Upload Text File", command=self.upload_file)
        self.upload_file_btn.grid(row=0, column=3, padx=5, pady=5)

        # Buttons for Operations
        self.create_tree_btn = tk.Button(self, text="Create Merkle Tree", command=self.create_merkle_tree)
        self.create_tree_btn.grid(row=1, column=1, pady=10)

        self.sign_data_btn = tk.Button(self, text="Generate Digital Signature", command=self.generate_signature, state="disabled")
        self.sign_data_btn.grid(row=2, column=1, pady=10)

        self.verify_signature_btn = tk.Button(self, text="Verify Digital Signature", command=self.verify_signature, state="disabled")
        self.verify_signature_btn.grid(row=3, column=1, pady=10)

        # Add Export Signature Button
        self.export_signature_btn = tk.Button(self, text="Export Signature", command=self.export_signature, state="disabled")
        self.export_signature_btn.grid(row=5, column=3, padx=5)

        # Add Import Signature Button after Export Signature Button
        self.import_signature_btn = tk.Button(self, text="Import Signature", command=self.import_signature)
        self.import_signature_btn.grid(row=5, column=4, padx=5)

        # Editable Merkle Tree Root Hash Section
        tk.Label(self, text="Merkle Tree Root Hash:").grid(row=4, column=0, sticky="w")
        self.root_hash_entry = tk.Entry(self, width=60)
        self.root_hash_entry.grid(row=4, column=1, columnspan=2, sticky="w")

        tk.Label(self, text="Digital Signature:").grid(row=5, column=0, sticky="w")
        self.signature_label = tk.Label(self, text="", wraplength=500, anchor="w", justify="left")
        self.signature_label.grid(row=5, column=1, columnspan=2, sticky="w")

        # Internal State
        self.encoder = None
        self.root_hash = None
        self.digital_signature = None

    def upload_file(self):
        """
        Open a file dialog to upload a text file and load its content into the input field.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.data_text.delete("1.0", tk.END)
                    self.data_text.insert(tk.END, content)
                messagebox.showinfo("File Loaded", "File content loaded into input field.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def create_merkle_tree(self):
        """
        Create a Merkle Tree using input data.
        """
        input_data = self.data_text.get("1.0", tk.END).strip()
        if not input_data:
            messagebox.showerror("Error", "Input data cannot be empty!")
            return

        self.encoder = Encoder(input_data, isFile=False)
        self.root_hash = self.encoder.getFinalHash()
        self.root_hash_entry.delete(0, tk.END)
        self.root_hash_entry.insert(0, self.root_hash)
        self.sign_data_btn.config(state="normal")
        messagebox.showinfo("Success", "Merkle Tree created successfully!")

    def generate_signature(self):
        """
        Generate a digital signature for the Merkle Tree's root hash.
        """
        try:
            self.root_hash = self.root_hash_entry.get().strip()
            if not self.root_hash:
                messagebox.showerror("Error", "Root hash cannot be empty!")
                return

            self.digital_signature = generate_signature(self.root_hash)
            self.signature_label.config(text=self.digital_signature)
            self.verify_signature_btn.config(state="normal")
            self.export_signature_btn.config(state="normal")  # Enable export button
            messagebox.showinfo("Success", "Digital signature generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate digital signature: {e}")

    def verify_signature(self):
        """
        Verify the digital signature for the Merkle Tree's root hash.
        """
        try:
            is_valid = verify_signature(self.root_hash_entry.get().strip(), self.digital_signature)
            if is_valid:
                messagebox.showinfo("Success", "Digital signature is valid!")
            else:
                messagebox.showerror("Error", "Digital signature is invalid!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to verify digital signature: {e}")

    def export_signature(self):
        """
        Export the digital signature to a text file.
        """
        if not self.digital_signature:
            messagebox.showerror("Error", "No signature to export!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Export Digital Signature"
        )
        
        if file_path:
            try:
                # Convert bytes to string using hex encoding
                signature_str = self.digital_signature.hex()
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(signature_str)
                messagebox.showinfo("Success", "Signature exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export signature: {e}")

    def import_signature(self):
        """
        Import a digital signature from a text file and convert it from hex format.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")],
            title="Import Digital Signature"
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    hex_signature = file.read().strip()
                    # Convert hex string back to bytes
                    self.digital_signature = bytes.fromhex(hex_signature)
                    self.signature_label.config(text=hex_signature)
                    self.verify_signature_btn.config(state="normal")
                    messagebox.showinfo("Success", "Signature imported successfully!")
            except ValueError as e:
                messagebox.showerror("Error", "Invalid signature format. Please ensure the file contains a valid hex signature.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import signature: {e}")


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
