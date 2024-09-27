# This script handles the preprocessing of various file types.
# Supported file types include .txt, .log, .pdf, .docx, .jpg, .png, .jpeg, .csv

import os
import cv2
import PyPDF2
import pytesseract  
import subprocess
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
    """
    Processes video files by extracting image frames and audio layers.

    input: file path (string)
    output: extracted audio and images from the video as a string
    """
    in_file = os.path.join(os.getcwd(), file_path[10:])

    # Extract audio from video
    convert_vid_to_aud = f"ffmpeg -y -i {in_file} temp_audio_for_video.wav"
    os.system(convert_vid_to_aud)

    r = sr.Recognizer()
    with sr.AudioFile("temp_audio_for_video.wav") as source:
        audio = r.record(source, duration=120)
    audio_content = r.recognize_google(audio)

    # Extract frames from video
    video_capture = cv2.VideoCapture(file_path)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(frame_count // 10, 1)

    content = audio_content + " | "

    for i in range(0, frame_count, frame_interval):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, i)
        success, frame = video_capture.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        denoised = cv2.medianBlur(thresh, 3)
        rescaled_img = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(rescaled_img, kernel, iterations=1)
        
        frame_content = pytesseract.image_to_string(dilated)
        content += frame_content + " | "

    video_capture.release()
    return content

def process_audio(file_path):
    """
    Processes audio files by extracting speech

    input: file path (string)
    output: extracted speech from the audio as a string
    """
    in_file = os.path.join(os.getcwd(), file_path[10:])
    convert_aud_to_aud = f"ffmpeg -y -i {in_file} temp_audio_for_audio.wav"
    os.system(convert_aud_to_aud)

    r = sr.Recognizer()
    with sr.AudioFile("temp_audio_for_audio.wav") as source:
        audio = r.record(source)
    content = r.recognize_google(audio, language = 'en-IN')

    print(content)

    return content