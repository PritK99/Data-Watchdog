import os
import logging
from detect import detect_pii_from_string, detect_pii_from_csv
from utils import process_txt_or_log, process_pdf, process_docx, process_image
from postprocess import assign_bucket_and_risk, convert_to_csv

# Configure logging to store results in a log file
logging.basicConfig(filename='results.log', level=logging.INFO,
                    format='%(message)s')

# Define the path to the temporary folder where files are stored
temp_folder = '../assets/temp'

global_pii_results = []

def list_files_recursive(folder_path):
    """
    Lists all files in a folder and its subfolders.

    input: folder path
    output: list of file paths
    """
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Normalize the path to ensure correct slashes
            normalized_path = os.path.normpath(file_path)
            file_list.append(normalized_path)
    return file_list

# Get a list of all files in the temporary folder
files = list_files_recursive(temp_folder)

for file in files:
    # Process text and log files
    if file.endswith(".txt") or file.endswith(".log"):
        content = process_txt_or_log(file)
        pii_result = detect_pii_from_string(content)

    # Process PDF files
    elif file.endswith(".pdf"):
        content = process_pdf(file)
        pii_result = detect_pii_from_string(content)

    # Process DOCX files
    elif file.endswith(".docx"):
        content = process_docx(file)
        pii_result = detect_pii_from_string(content)

    # Process image files (JPG, PNG, JPEG)
    elif file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
        content = process_image(file)
        pii_result = detect_pii_from_string(content)

    # Process CSV files
    elif file.endswith(".csv"):
        pii_result = detect_pii_from_csv(file)

    # Handle unknown file types
    else:
        logging.info(f"Unknown file type: {file}")
        continue

    # Log the PII detection result for each file
    logging.info(f"PII detection result for {file}: {pii_result}")
    processed_pii_result = assign_bucket_and_risk(pii_result)
    final_result = [file, processed_pii_result]
    global_pii_results.append(final_result)

pii_results_df = convert_to_csv(global_pii_results)
pii_results_df.to_csv("../assets/results/output.csv", index=False)