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

```py
python -m venv data-watchdog
```

Activate the virtual environment

```
.\data-watchdog\Scripts\activate
```

*Note*: If this doesn't work, try navigating to `Scripts` directory and run `source activate`.

Navigate to the model folder

```py
cd model
```

Install all the required libraries

```py
pip install -r .\requirements.txt
```

*Note*: Path to `poppler` and `pytesseract` are required in `utils.py` to perform pdf to image conversion and OCR respectively.

## Usage

Create a directory named `backend/downloads/` from the home directory. This folder will act as a staging area for files to be processed. The supported file formats are: `.txt`, `.log`, `.pdf`, `.docx`, `.jpg`, `.png`, `.jpeg`, and `.csv`. You can either use the files provided in `assets/temp` or use your own files of compatible file formats.

To run the standalone model, first we need to resolve all the imports by replacing code at 2 places.

1) Replace the code section in `main.py` from

```py
from .detect import detect_pii_from_string, detect_pii_from_csv
from .utils import process_txt_or_log, process_pdf, process_docx, process_image
from .postprocess import assign_bucket_and_risk, convert_to_csv
from .analytics import analyze
```

to

```
from detect import detect_pii_from_string, detect_pii_from_csv
from utils import process_txt_or_log, process_pdf, process_docx, process_image
from postprocess import assign_bucket_and_risk, convert_to_csv
from analytics import analyze
```

2) Replace the code line in `detect.py` from

```py
from .utils import process_csv
```
to

```
from utils import process_csv
```

We also need to uncomment the line `91` to call the function.

To run the standalone model after making the changes as mentioned above

```py
python main.py
```

All the results will be logged into `results.log`