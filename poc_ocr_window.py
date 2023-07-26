import tkinter as tk
from tkinter import filedialog
import os, shutil

# file path where the page images will be saved
path_page_images = f'page_images'
if os.path.exists(path_page_images):
    shutil.rmtree(path_page_images)
os.mkdir(path_page_images)


from ironpdf import *
# Instantiate Renderer


def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        # Here, you can perform further processing on the selected PDF file
        print("Selected PDF File:", file_path)
        # Create a PDF from a URL or local file path
        pdf = PdfDocument.FromFile(file_path)
        # Extract all pages to a folder as image files
        shutil.rmtree(path_page_images)
        pdf.RasterizeToImageFiles(f"{path_page_images}/*.png",DPI=150)
        update_label(file_path)

def update_label(file_path):
    label.config(text=f"Currently Loaded PDF: {file_path}")

def create_gui():
    root = tk.Tk()
    root.title("PDF Processor")
    root.geometry("1400x800")
    root.configure(bg="brown")

    browse_button = tk.Button(root, text="Browse PDF", command=browse_pdf)
    browse_button.pack(pady=20)

    global label
    label = tk.Label(root, text="Currently Loaded PDF: None")
    label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
