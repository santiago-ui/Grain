import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from grain_code import Grain
from image_converter import image_to_byte_array, byte_array_to_image
from io import BytesIO


class CifradorFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cifrador de Grain")

        self.clave_label = ttk.Label(root, text="Clave")
        self.clave_label.grid(row=0, column=0, padx=5, pady=5)
        self.clave_entry = ttk.Entry(root, width=20)
        self.clave_entry.grid(row=0, column=1, padx=5, pady=5)

        self.semilla_label = ttk.Label(root, text="Semilla")
        self.semilla_label.grid(row=1, column=0, padx=5, pady=5)
        self.semilla_entry = ttk.Entry(root, width=20)
        self.semilla_entry.grid(row=1, column=1, padx=5, pady=5)

        self.open_button = ttk.Button(root, text="Abrir imagen", command=self.open_image)
        self.open_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.encrypt_button = ttk.Button(root, text="Cifrar / Descifrar", command=self.encrypt_decrypt)
        self.encrypt_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.save_button = ttk.Button(root, text="Guardar imagen", command=self.save_image)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.clear_button = ttk.Button(root, text="Limpiar", command=self.clear)
        self.clear_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        self.image_original = None
        self.image_encrypted = None
        self.image_label_original = ttk.Label(root)
        self.image_label_original.grid(row=0, column=2, rowspan=6)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if file_path:
            self.image_original = Image.open(file_path)
            self.display_image(self.image_label_original, self.image_original)

    def display_image(self, label, image):
        image = ImageTk.PhotoImage(image)
        label.configure(image=image)
        label.image = image

    def encrypt_decrypt(self):
        clave = self.clave_entry.get()
        semilla = self.semilla_entry.get()
        if not clave or not semilla:
            tk.messagebox.showerror("Error", "La clave y la semilla son obligatorias")
            return

        if not self.image_original:
            tk.messagebox.showerror("Error", "Debe cargar una imagen para cifrar")
            return

        try:
            # Replace with your Grain encryption code
            grain = Grain(clave.encode(), semilla.encode(), self.image_original.tobytes())
            encrypted_data = grain.xor()
            self.image_encrypted = Image.frombytes(self.image_original.mode, self.image_original.size, encrypted_data)
            self.display_image(self.image_label_original, self.image_encrypted)
        except Exception as e:
            tk.messagebox.showerror("Error", "Error al cifrar la imagen: " + str(e))

    def save_image(self):
        if self.image_encrypted:
            file_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
            if file_path:
                self.image_encrypted.save(file_path)

    def clear(self):
        self.clave_entry.delete(0, tk.END)
        self.semilla_entry.delete(0, tk.END)
        self.image_original = None
        self.image_encrypted = None
        self.image_label_original.config(image="")
        self.image_label_original.image = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = CifradorFrame(root)
    root.geometry("800x400")
    root.mainloop()