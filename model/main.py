import os
import logging
from detect import detect_pii_from_string
from utils import process_txt_or_log, process_pdf, process_docx, process_image

# Storing the results in a log file
logging.basicConfig(filename='pii_detection.log', level=logging.INFO,
                    format='%(message)s')

# We treat temp folder as staging area
temp_folder = '../assets/temp'

# This function returns list of all files available in temp folder
def list_files_recursive(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Normalizing for correct slashes
            normalized_path = os.path.normpath(file_path)
            file_list.append(normalized_path)
    return file_list

files = list_files_recursive(temp_folder)

for file in files:

    if (file.endswith(".txt") or file.endswith(".log")):
        content = process_txt_or_log(file)
        pii_result = detect_pii_from_string(content)

    elif (file.endswith(".pdf")):
        content = process_pdf(file)
        pii_result = detect_pii_from_string(content)

    elif (file.endswith(".docx")):
        content = process_docx(file)
        pii_result = detect_pii_from_string(content)

    elif (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")):
        content = process_image(file)
        pii_result = detect_pii_from_string(content)

    else:
        logging.info(f"Unknown file type: {file}")
        continue

    logging.info(f"PII detection result for {file}: {pii_result}")