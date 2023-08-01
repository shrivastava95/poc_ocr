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
lang = 'ori+eng'

# file paths where the page images and bounding boxes will be saved
path_page_images = 'page_images'
path_page_boxes = 'page_boxes'
path_page_outputs = 'page_outputs'

for path_page_xx in [path_page_outputs, path_page_images, path_page_boxes]:
    if os.path.exists(path_page_xx):
        shutil.rmtree(path_page_xx)
    os.mkdir(path_page_xx)

def process_boxes(file_path, custom_config=''):
    # open image file
    img = Image.open(file_path)

    # extract bounding box data
    boxes = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=lang, config=custom_config)

    # save bounding box data to json file
    with open(os.path.join(path_page_boxes, os.path.basename(file_path).replace('.png', '.json')), 'w') as f:
        json.dump(boxes, f)
    
    # extract OCR text
    ocr_text = pytesseract.image_to_string(img, lang=lang, config=custom_config)

    # save OCR text to txt file
    output_file = os.path.join(path_page_outputs, os.path.basename(file_path).replace('.png', '.txt'))
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ocr_text)

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

        pdf.RasterizeToImageFiles(f"{path_page_images}/*.png", DPI=150)

        # process bounding boxes for each page
        for page_path in glob.glob(f"{path_page_images}/*.png"):
            process_boxes(page_path, f'--psm {psm_mode_variable.get()}')

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
    color_mapping = {
        1: 'blue',
        2: 'green',
        3: 'red',
        4: 'cyan',
        5: 'yellow'
    }

    # draw bounding boxes
    for i in range(len(boxes['text'])):
        # if int(boxes['conf'][i]) > 50: # find out what this line does?
        if True:
            x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
            draw.rectangle(((x, y), (x + w, y + h)), outline=color_mapping[boxes['level'][i]], width=4)

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

def reprocess_page():
    page_number = variable.get()
    if page_number != 'Select Page':
        img_path = os.path.join(path_page_images, f"{page_number}.png")
        process_boxes(img_path, f'--psm {psm_mode_variable.get()}')
        view_page()

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

    # Add a Label to display the PSM mode dropdown
    psm_mode_label = tk.Label(controls_frame, text="PSM mode:")
    psm_mode_label.pack(pady=5)

    # Create a list of PSM modes
    # psm_modes = ["0", "1", "3", "4", "6", "7", "11", "12", "13"]
    psm_modes = ["3", "6"]
    global psm_mode_variable
    psm_mode_variable = tk.StringVar(root)
    psm_mode_variable.set("3")  # Set the default value of the PSM mode dropdown

    # Create the PSM mode OptionMenu
    psm_mode_menu = tk.OptionMenu(controls_frame, psm_mode_variable, *psm_modes)
    psm_mode_menu.pack(pady=5)

    # Add the reprocess button
    reprocess_button = tk.Button(controls_frame, text="Reprocess Page", command=reprocess_page)
    reprocess_button.pack(pady=10)

    global image_label
    image_label = None

    root.mainloop()

if __name__ == "__main__":
    create_gui()
