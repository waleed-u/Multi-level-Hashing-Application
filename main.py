import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from Tree.Models.Encoder import Encoder  # Importing Encoder for Merkle Tree functionality
from signature import generate_signature, verify_signature  # Importing Digital Signature Module


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


def main():
    root = tk.Tk()
    app = MerkleSignatureApp(root)
    app.mainloop()


if __name__ == "__main__":
    main()
