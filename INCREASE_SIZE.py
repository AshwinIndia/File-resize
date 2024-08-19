import os
import PIL.Image
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# The Compressor class
class Compressor:
    def __init__(self, root):
        self.window = root
        self.window.geometry("520x320")
        self.window.title("Image resize MAX LIMIT 80%")
        self.window.configure(bg="white")
        self.window.resizable(width=False, height=False)

        # Setting the image path Null initially
        self.imagePath = ''

        # Header Label
        headingLabel = Label(self.window, text="IMAGE RESIZE", 
        font=("Kokila", 18, "bold"), bg="red")
        headingLabel.place(x=130, y=30)

      # Button to select the Image
        selectButton = Button(self.window, text="Select Image", 
        font=("Helvetica", 10), bg="green", fg="white", command=self.Open_Image)
        selectButton.place(x=120, y=110)

        # Label for Image Quality
        imageQuality = Label(self.window, text="Image Size", 
        font=("Times New Roman", 12), bg="white")
        imageQuality.place(x=245, y=110)

        # Image quality options
        imageQualityList = [10, 20, 30, 40, 50, 60, 70, 80]

        # Image quality options
        imageQualityList = [10, 20, 30, 40, 50, 60, 70, 80]
         # Dropdown menu for image quality
        self.clicked = StringVar()
        self.clicked.set(80)
        qualityMenu = OptionMenu(self.window, self.clicked, *imageQualityList)
        qualityMenu.config(width=2, font=("Helvetica", 9, "bold"), bg="gray50", fg="white")
        qualityMenu.place(x=345, y=109)

        # Button to compress the selected image
        compressButton = Button(self.window, text="Resize Image", 
        font=("Helvetica", 10), bg="yellow", fg="black", command=self.Compress_Image)
        compressButton.place(x=190, y=160)

        # Frame to display selected image path
        self.frame = Frame(self.window, bg="white", width=520, height=100)
        self.frame.place(x=0, y=200)

    # Open an Image through the filedialog widget
    def Open_Image(self):
        self.imagePath = filedialog.askopenfilename(initialdir="/", 
        title="Select an Image", filetypes=(("Image files", "*.jpg *.jpeg *.png"),))

        # Display selected image path
        if len(self.imagePath) != 0:
            imagePathLabel = Label(self.frame, text=self.imagePath, 
            font=("Times new roman", 12), bg="white", fg="red")
            imagePathLabel.place(x=260-(len(self.imagePath)/2)*7, y=20)

    # Function to Compress the chosen image
    def Compress_Image(self):
        if len(self.imagePath) == 0:
            messagebox.showerror("Error", "Please Select an Image first")
        else:
            img = PIL.Image.open(self.imagePath)
            width, height = img.size
            img = img.resize((width, height), PIL.Image.Resampling.LANCZOS)
            filename, extension = os.path.splitext(os.path.basename(self.imagePath))
            savetoPath = filedialog.askdirectory()
            resultFilename = f"{savetoPath}/{filename}-Resized.jpg"


            try:
                img = img.convert("RGB")
                img.save(resultFilename, quality=int(self.clicked.get()), optimize=True)
                messagebox.showinfo("Done!", "The Image has been Resized.")
                self.reset()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to {es}")

    # Reset function
    def reset(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.imagePath = ''

# Main function
if __name__ == "__main__":
    root = Tk()
    obj = Compressor(root)
    root.mainloop()

