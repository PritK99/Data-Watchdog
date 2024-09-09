# This script handles all the preprocessing of different types of files
# Common filetypes include .txt, .log, .pdf, .docx, .jpg, .png, .jpeg, .sql, .csv
import cv2
import PyPDF2
import pytesseract  
import numpy as np
from PIL import Image
from pdf2image import convert_from_path     
from docx import Document

# Path where the tesseract module is installed 
pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'  
poppler_path= r"C:\Users\pritp\Downloads\poppler-24.07.0\Library\bin"

# .txt or .log files
def process_txt_or_log(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    return content 

# .pdf files
def process_pdf(file_path):
    # First extract text from pdf file
    content = ""
    with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                content += page.extract_text()

    # Converting .pdf to images and extracting text using ocr
    # converts the image to result and saves it into result variable 
    images = convert_from_path(file_path, poppler_path=poppler_path)
    for image in images:
        image = np.array(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        denoised = cv2.medianBlur(thresh, 3)
        rescaled_img = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(rescaled_img, kernel, iterations=1)
        content += pytesseract.image_to_string(image) 

    return content

# .docx files
def process_docx(file_path):
    doc = Document(file_path)
    text = '\n'.join([p.text for p in doc.paragraphs])
    return text

# .jpg, .png, .jpeg files
def process_image(file_path):
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    denoised = cv2.medianBlur(thresh, 3)
    rescaled_img = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(rescaled_img, kernel, iterations=1)
    content = pytesseract.image_to_string(image) 
    return content 

"""
TO DO: Processing for SQL and CSV
"""