import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from utils import validate_image_file, validate_secret_text

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Kleid: Steganography Tool")

        self.original_image_label = tk.Label(master, text="Original Image:")
        self.original_image_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.original_image_entry = tk.Entry(master, width=50)
        self.original_image_entry.grid(row=0, column=1, padx=10, pady=5)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_original_image)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        self.secret_text_label = tk.Label(master, text="Secret Text:")
        self.secret_text_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.secret_text_entry = tk.Entry(master, width=50)
        self.secret_text_entry.grid(row=1, column=1, padx=10, pady=5)

        self.hide_button = tk.Button(master, text="Hide Text", command=self.hide_text)
        self.hide_button.grid(row=2, column=1, padx=10, pady=5)

    def browse_original_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.original_image_entry.delete(0, tk.END)
            self.original_image_entry.insert(0, file_path)

    def hide_text(self):
        original_image_path = self.original_image_entry.get()
        secret_text = self.secret_text_entry.get()

        try:
            validate_image_file(original_image_path)
            validate_secret_text(secret_text)

            img = Image.open(original_image_path)
            binary_secret_text = ''.join(format(ord(char), '08b') for char in secret_text)
            secret_text_length = len(binary_secret_text)
            img_data = iter(img.getdata())

            new_img_data = []
            for i in range(secret_text_length):
                pixel = next(img_data)
                new_pixel = list(pixel)
                new_pixel[-1] = int(binary_secret_text[i])
                new_img_data.append(tuple(new_pixel))

            img.putdata(new_img_data)
            hidden_image_path = "hidden_image.png"
            img.save(hidden_image_path)

            messagebox.showinfo("Huzzah!", "Text hidden successfully! Proceed with your dastardly deeds!\nThe hidden image file is saved as: {}".format(hidden_image_path))

        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
