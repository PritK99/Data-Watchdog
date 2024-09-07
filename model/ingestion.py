import os
import PyPDF2
import logging
import pypandoc

from docx import Document

from pii_core import detect_pii_from_string

# Storing the results in a log file
logging.basicConfig(filename='pii_detection.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

temp_folder = '../assets/temp'

text_files_extensions = [".txt", ".log"]
media_files_extensions = [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".avi"]
pdf_files_extensions = [".pdf"]
csv_files_extensions = [".csv"]
sql_files_extensions = [".sql"]

def list_files_recursive(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Normalizing for correct slashes
            normalized_path = os.path.normpath(file_path)
            file_list.append(normalized_path)
    return file_list

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        pii_detection_result = detect_pii_from_string(content)
        return pii_detection_result

def process_pdf_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            pii_detection_result = detect_pii_from_string(text)
            return pii_detection_result
    except Exception as e:
        logging.error(f"Failed to process PDF file {file_path}: {e}")
        return None


def process_doc_file(file_path):
    try:
        output = pypandoc.convert_file(file_path, 'plain')
        pii_detection_result = detect_pii_from_string(output)
        return pii_detection_result
    except Exception as e:
        logging.error(f"Failed to process DOC file {file_path}: {e}")
        return None

def process_docx_file(file_path):
    try:
        doc = Document(file_path)
        text = '\n'.join([p.text for p in doc.paragraphs])
        pii_detection_result = detect_pii_from_string(text)
        return pii_detection_result
    except Exception as e:
        logging.error(f"Failed to process DOCX file {file_path}: {e}")
        return None

files = list_files_recursive(temp_folder)

for file in files:
    # Process text files (TXT, LOG)
    if any(file.endswith(ext) for ext in text_files_extensions):
        pii_result = process_text_file(file)
        logging.info(f"PII detection result for {file}: {pii_result}")

    # Process PDF files    
    elif file.endswith(tuple(pdf_files_extensions)):
        pii_result = process_pdf_file(file)
        if pii_result is not None:
            logging.info(f"PII detection result for {file}: {pii_result}")

    # Process DOCX files    
    elif file.endswith('.docx'):
        pii_result = process_docx_file(file)
        if pii_result is not None:
            logging.info(f"PII detection result for {file}: {pii_result}")

    # Process DOC files    
    elif file.endswith('.doc'):
        pii_result = process_doc_file(file)
        if pii_result is not None:
            logging.info(f"PII detection result for {file}: {pii_result}")

    # We are yet to add support for such files
    elif file.endswith(tuple(media_files_extensions)):
        logging.info(f"Media file found: {file}")
    elif file.endswith(tuple(csv_files_extensions)):
        logging.info(f"CSV file found: {file}")
    elif file.endswith(tuple(sql_files_extensions)):
        logging.info(f"SQL file found: {file}")
    else:
        logging.info(f"Unknown file type: {file}")