# poc_ocr
A repository for the POC for parsing translation dicitonaries using OCR. This is a part of the C4GT work under ai-tools/dictionary-augmented-transformers.

# Requirements
- Python version 3.11
- ironpdf - `pip install ironpdf`
- ensure `Pillow` library is installed with version < 10 (deprecation errors)

# Files and Folders
- `Hanuman_Chalisa_In_Odia.pdf` - a sample pdf to test the OCR on.
- `poc_ocr_window.py` - the final POC for loading PDFs and showing the bounding boxes.
- `poc_ocr.py` - a fallback checkpoint for poc_ocr_window.py
- `test.py` - testing some features

# Instructions to run
`python poc_ocr_windows.py` to run the POC. Once the window opens, load a PDF and select a page to be displayed. Then view the page with the bounding boxes overlaid.