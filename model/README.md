# Model for PII Detection

## Methodology

1) **PII Detection from Strings**

    I) Regular Expressions (REGEX):
Used to detect PII with fixed patterns, such as email addresses, IP addresses, Aadhar numbers, and credit card numbers.

    II) Named Entity Recognition (NER):
Utilizes pre-trained models to identify PII such as personal names, locations, and organizations.

2) **PII Detection from CSV Files**

    I) Column Name Matching: Checks if any column names in the CSV match known PII-related terms. All fields in detected columns are flagged as PII.

    II) Cell Pattern Matching: Scans through all cells in the CSV and applies REGEX patterns to identify potential PII.

## Steps to create virtual environment on windows

Create a virtual environment

`python -m venv data-watchdog`

Activate the virtual environment

`.\data-watchdog\Scripts\activate`

Navigate to the model folder

`cd model`

Install all the required libraries

`pip install -r .\requirements.txt`

*Note*: Path to `poppler` and `pytesseract` are required in `utils.py` to perform pdf to image conversion and OCR respectively.

## Usage

Create a directory named `assets/temp/` in the home directory. This folder will act as a staging area for files to be processed. The supported file formats are: `.txt`, `.log`, `.pdf`, `.docx`, `.jpg`, `.png`, `.jpeg`, and `.csv`.

To run the standalone model, first resolve all the import errors.

`python main.py`

All the results will be logged into `results.log`