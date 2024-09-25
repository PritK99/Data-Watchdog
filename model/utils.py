# This script handles the preprocessing of various file types.
# Supported file types include .txt, .log, .pdf, .docx, .jpg, .png, .jpeg, .csv

import os
import cv2
import PyPDF2
import pytesseract  
import numpy as np
import pandas as pd
import speech_recognition as sr
from pdf2image import convert_from_path     
from docx import Document

# Path to the Tesseract OCR module
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Path to the Poppler library for PDF-to-image conversion
poppler_path = r"C:\Users\pritp\Downloads\poppler-24.07.0\Library\bin"

def process_txt_or_log(file_path):
    """
    Processes text and log files.

    input: file path (string)
    output: content of the file as a string
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    return content 

def process_pdf(file_path):
    """
    Processes PDF files by extracting text from both text and image layers.

    input: file path (string)
    output: extracted text from the PDF as a string
    """
    content = ""
    # Extract text from PDF file
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content += page.extract_text() or ""
    
    # Convert PDF pages to images and use OCR to extract text
    images = convert_from_path(file_path, poppler_path=poppler_path)
    for image in images:
        image = np.array(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        denoised = cv2.medianBlur(thresh, 3)
        rescaled_img = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(rescaled_img, kernel, iterations=1)
        content += pytesseract.image_to_string(dilated) 

    return content

def process_docx(file_path):
    """
    Processes DOCX files.

    input: file path (string)
    output: content of the DOCX file as a string
    """
    doc = Document(file_path)
    text = '\n'.join([p.text for p in doc.paragraphs])
    return text

def process_image(file_path):
    """
    Processes image files (JPG, PNG, JPEG) using OCR to extract text.

    input: file path (string)
    output: extracted text from the image as a string
    """
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    denoised = cv2.medianBlur(thresh, 3)
    rescaled_img = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(rescaled_img, kernel, iterations=1)
    content = pytesseract.image_to_string(dilated) 
    return content 

def process_csv(file_path):
    """
    Processes CSV files by concatenating all cell values into a single string.

    input: file path (string)
    output: concatenated cell values from the CSV as a string
    """
    df = pd.read_csv(file_path)
    cell_values = df.values.flatten().astype(str)
    cell_values = [str(value) for value in cell_values if value != "nan"]
    content = ' | '.join(cell_values)
    return content

def process_video(file_path):
    base_out_path = os.getcwd()[:-5]

    temp_dir = os.path.join(base_out_path, "assets", "results")
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, "temp.mp3")
    out_path = os.path.join(temp_dir, "temp.wav")

    convert_vid_to_aud = f"ffmpeg -y -i {file_path} {temp_path}"
    convert_aud_to_wav = f"ffmpeg -y -i {temp_path} {out_path}"

    os.system(convert_vid_to_aud)
    os.system(convert_aud_to_wav)

    r = sr.Recognizer()
    with sr.AudioFile(out_path) as source:
         audio = r.record(source, duration=120) 
    content = r.recognize_google(audio)

    os.remove(out_path)
    os.remove(temp_path)
    return content

def process_audio(file_path):
    base_out_path = os.getcwd()[:-5]

    temp_dir = os.path.join(base_out_path, "assets", "results")
    os.makedirs(temp_dir, exist_ok=True)
    out_path = os.path.join(temp_dir, "temp.wav")

    convert_vid_to_aud = f"ffmpeg -y -i {file_path} {out_path}"
    os.system(convert_vid_to_aud)
    r = sr.Recognizer()
    with sr.AudioFile(out_path) as source:
        audio = r.record(source, duration=120) 
    content = r.recognize_google(audio)

    os.remove(out_path)
    return content