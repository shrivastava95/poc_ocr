import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import os, shutil
from ironpdf import *
import glob
import pytesseract
import json

# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
# Set the language
lang='ori+eng'

# file paths where the page images and bounding boxes will be saved
path_page_images = 'page_images'
path_page_boxes = 'page_boxes'

if os.path.exists(path_page_images):
    shutil.rmtree(path_page_images)
os.mkdir(path_page_images)

if os.path.exists(path_page_boxes):
    shutil.rmtree(path_page_boxes)
os.mkdir(path_page_boxes)

def process_boxes(file_path):
    # open image file
    img = Image.open(file_path)

    # extract bounding box data
    boxes = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=lang)

    # save bounding box data to json file
    with open(os.path.join(path_page_boxes, os.path.basename(file_path).replace('.png', '.json')), 'w') as f:
        json.dump(boxes, f)

def browse_pdf():
    global menu
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        # display waiting message
        # update_label('PDF is loading, please wait before further actions...') # this does not work for some reason. also it is not even needed.
        # Create a PDF from a URL or local file path
        pdf = PdfDocument.FromFile(file_path)
        # Extract all pages to a folder as image files
        if os.path.exists(path_page_images):
            shutil.rmtree(path_page_images)
        os.mkdir(path_page_images)

        if os.path.exists(path_page_boxes):
            shutil.rmtree(path_page_boxes)
        os.mkdir(path_page_boxes)

        pdf.RasterizeToImageFiles(f"{path_page_images}/*.png",DPI=150)

        # process bounding boxes for each page
        for page_path in glob.glob(f"{path_page_images}/*.png"):
            process_boxes(page_path)

        update_label(file_path)
        update_dropdown()

def update_label(file_path):
    label_text.delete(1.0, tk.END)
    label_text.insert(tk.END, f"Currently Loaded PDF: {file_path}")

def update_dropdown():
    global variable
    global menu
    pages = glob.glob(f"{path_page_images}/*.png")
    page_numbers = [os.path.splitext(os.path.basename(page))[0] for page in pages]
    variable.set('Select Page') 
    menu['menu'].delete(0, 'end')
    for page in page_numbers:
        menu['menu'].add_command(label=page, command=tk._setit(variable, page))

def draw_boxes(img, boxes):
    # create a draw object
    draw = ImageDraw.Draw(img)

    # draw bounding boxes
    for i in range(len(boxes['text'])):
        if int(boxes['conf'][i]) > 50:
            x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
            draw.rectangle(((x, y), (x + w, y + h)), outline='red', width=10)

    return img

def view_page():
    page_number = variable.get()
    if page_number != 'Select Page':
        img_path = os.path.join(path_page_images, f"{page_number}.png")
        img = Image.open(img_path)

        # load bounding box data
        with open(os.path.join(path_page_boxes, f"{page_number}.json"), 'r') as f:
            boxes = json.load(f)

        # draw bounding boxes
        img = draw_boxes(img, boxes)

        max_size = (800, 800)
        img.thumbnail(max_size, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        global image_label
        if image_label is not None:
            image_label.destroy()

        image_label = tk.Label(root, image=img)
        image_label.image = img  
        image_label.pack(side="right")

def create_gui():
    global root
    root = tk.Tk()
    root.title("PDF Processor")
    root.geometry("1400x800")
    root.configure(bg="brown")

    controls_frame = tk.Frame(root)
    controls_frame.pack(side="left", padx=10, pady=10)

    browse_button = tk.Button(controls_frame, text="Browse PDF", command=browse_pdf)
    browse_button.pack(pady=20)

    global label_text
    label_text = tk.Text(controls_frame, width=50, height=2)
    label_text.pack(pady=10)

    global variable
    variable = tk.StringVar(root)
    variable.set('Select Page') 

    global menu
    menu = tk.OptionMenu(controls_frame, variable, ())
    menu.pack(pady=10)

    view_button = tk.Button(controls_frame, text="View Page", command=view_page)
    view_button.pack(pady=20)

    global image_label
    image_label = None 

    root.mainloop()

if __name__ == "__main__":
    create_gui()
