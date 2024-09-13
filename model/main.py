import os
import sys
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from .detect import detect_pii_from_string, detect_pii_from_csv
from .utils import process_txt_or_log, process_pdf, process_docx, process_image
from .postprocess import assign_bucket_and_risk, convert_to_csv
from .analytics import analyze

# Configure logging to store results in a log file
logging.basicConfig(filename='results.log', level=logging.INFO,
                    format='%(message)s')

# Define the path to the temporary folder where files are stored
# temp_folder = '../assets/temp'
temp_folder = '../server/downloads'

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

def get_pii():

    # Get a list of all files in the temporary folder
    files = list_files_recursive(temp_folder)
    global_pii_results = []

    print(files)

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
    analysis_json = analyze(pii_results_df)

    # Saving JSON and CSV in assets folder
    with open('../assets/results/analysis.json', 'w') as f: f.write(analysis_json)
    pii_results_df.to_csv("../assets/results/output.csv", index=False)

    return analysis_json, pii_results_df

# analysis_json, pii_results_df = get_pii()