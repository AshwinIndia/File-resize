import os
import PIL.Image
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class Resizer:
    def __init__(self, root):
        self.window = root
        self.window.geometry("520x400")
        self.window.title("File Resizing System")
        self.window.configure(bg="white")
        self.imagePath = ''
        
        Label(self.window, text="Select an Image to Resize", font=("Arial", 14)).pack(pady=10)
        
        Button(self.window, text="Select Image", command=self.select_image).pack(pady=10)
        
        self.resize_option = StringVar(value="compress")
        Radiobutton(self.window, text="Compress", variable=self.resize_option, value="compress").pack(anchor=W)
        Radiobutton(self.window, text="Upscale", variable=self.resize_option, value="upscale").pack(anchor=W)
        
        Label(self.window, text="Desired Size (KB)", font=("Arial", 12)).pack(pady=5)
        self.size_entry = Entry(self.window)
        self.size_entry.pack()

        Label(self.window, text="Quality (%)", font=("Arial", 12)).pack(pady=5)
        self.quality_entry = Entry(self.window)
        self.quality_entry.pack()
        self.quality_entry.insert(0, "75")  

        Button(self.window, text="Resize", command=self.resize_image).pack(pady=10)

    def select_image(self):
        self.imagePath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.imagePath:
            Label(self.window, text=self.imagePath, font=("Arial", 10)).pack()

    def resize_image(self):
        if not self.imagePath:
            messagebox.showerror("Error", "Please select an image first!")
            return
        
        try:
            target_size_kb = int(self.size_entry.get())
            quality = int(self.quality_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid size and quality values!")
            return

        if not (10 <= quality <= 100):
            messagebox.showerror("Error", "Quality must be between 10% and 100%")
            return

        original_size_kb = os.path.getsize(self.imagePath) / 1024  

        if self.resize_option.get() == "upscale":
            if target_size_kb <= original_size_kb:
                messagebox.showwarning("Upscale Warning", 
                                       f"Please enter a size greater than the original size of {original_size_kb:.2f} KB.")
                return

            if quality < 80:
                messagebox.showwarning("Upscale Quality Warning", 
                                       "For upscaling, it's recommended to use a quality setting of 80% or higher.")
                return

            new_width, new_height = self.calculate_new_dimensions()
            img = PIL.Image.open(self.imagePath).resize((new_width, new_height), PIL.Image.Resampling.LANCZOS)
            self.save_image(img, target_size_kb=target_size_kb, quality=quality)
        else:
            img = PIL.Image.open(self.imagePath)
            img = img.resize((img.size), PIL.Image.Resampling.LANCZOS)
            self.save_image(img, target_size_kb=target_size_kb, quality=quality)

    def calculate_new_dimensions(self):
        img = PIL.Image.open(self.imagePath)
        width, height = img.size
        scale_factor = 1.2  
        return int(width * scale_factor), int(height * scale_factor)

    def save_image(self, img, target_size_kb, quality):
        filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")], title="Save As")
        if not filename:
            return  

        img.save(filename, quality=quality, optimize=True)
        
        actual_size_kb = os.path.getsize(filename) / 1024 
        while actual_size_kb > target_size_kb and quality > 10:
            quality -= 2  
            img.save(filename, quality=quality, optimize=True)
            actual_size_kb = os.path.getsize(filename) / 1024
        
        if actual_size_kb > target_size_kb:
            messagebox.showinfo("Note", f"Could not achieve target size. Final size: {actual_size_kb:.2f} KB")
        else:
            messagebox.showinfo("Success", f"Image saved as {filename}, Size: {actual_size_kb:.2f} KB")

def launch_resizer_gui():
    root = Tk()
    app = Resizer(root)
    root.mainloop()
