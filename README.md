# poc_ocr
A repository for the POC for parsing translation dicitonaries using OCR. This is a part of the C4GT work under ai-tools/dictionary-augmented-transformers.

# Requirements
- Python version 3.11
- ironpdf - `pip install ironpdf`
- ensure `Pillow` library is installed with version < 10 (deprecation errors)

# Files and Folders
- `page_boxes` - stores the bounding box data for each page.
- `page_images` - stores the images of each page for pre-processing.
- `page_outputs` - stores the OCR outputs on each page.
- `Hanuman_Chalisa_In_Odia.pdf` - a sample pdf to test the OCR on.
- `poc_ocr_window.py` - the final POC for loading PDFs and showing the bounding boxes.
- `poc_ocr.py` - a fallback checkpoint for poc_ocr_window.py - to where only the pdf is loaded and there is no display.
- `test.py` - testing some features

# Instructions to run
`python poc_ocr_windows.py` to run the POC. Once the window opens, load a PDF and then select a page to be displayed. Then view the page with the bounding boxes overlaid. If you spot any errors with the bounding boxes displayed for a particular page, select another PSM mode using the drop down menu and re-run the parsing for that page.

# demo video - Instructions
This demo video should clarify instructions on how to use the POC.
[demo video - youtube](https://www.youtube.com/watch?v=JezsfryQvKo)