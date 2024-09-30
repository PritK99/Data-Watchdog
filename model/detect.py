# This script performs the core functionality of extracting PII (Personally Identifiable Information)
import re
import logging
import pandas as pd
from .utils import process_csv
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Patterns for regex-based PII detection
pii_patterns = {
    "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    "phone": r'\b(?:\+91|91)?[789]\d{9}\b',
    "aadhar": r'\b\d{4}\s?\d{4}\s?\d{4}\b',
    "dob": r'\b(?:0[1-9]|[12][0-9]|3[01])/(?:0[1-9]|1[0-2])/\d{4}\b',
    "address": r'\b\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[\w\s]+,\s\d{6}\b',
    "drivers_license": r'\b[A-Z0-9]{15}\b',
    "passport": r'\b[A-Z]{1,2}\d{7,8}\b',
    "voters id": r'\b[A-Z]{3}\d{7}\b',
    "location": r'\b(?:-?\d{1,3}\.\d+),\s*-?\d{1,3}\.\d+\b',
    "vin": r'\b[A-HJ-NPR-Z0-9]{17}\b',
    "pincode": r'\b\d{6}\b',
    "ip": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    "pan": r'\b[A-Z]{5}\d{4}[A-Z]\b',
    "creditcard": r'(?:\d[ -]*?){13,16}',
    "bank_account": r'\b\d{11,18}\b',
    "cvv": r'\b\d{3}\b',
    "ration card": r'\b\d{9,16}\b',
}

# Possible PII column names and their types
pii_cols = {
    "id": "id",
    "user_id": "id",
    "name": "name",
    "username": "name",
    "full name": "name",
    "first name": "name",
    "last name": "name",
    "middle name": "name",
    "given name": "name",
    "surname": "name",
    "email address": "email",
    "email": "email",
    "phone number": "phone",
    "mobile number": "phone",
    "contact number": "phone",
    "cell number": "phone",
    "address": "location",
    "home address": "location",
    "mailing address": "location",
    "street address": "location",
    "city": "location",
    "state": "location",
    "province": "location",
    "zip code": "pincode",
    "postal code": "pincode",
    "country": "location",
    "date of birth": "dob",
    "dob": "dob",
    "username": "id",
    "user id": "id",
    "login id": "id",
    "account id": "id",
    "employee id": "id",
    "employee number": "id",
    "department": "organization",
    "position": "id",
    "unique identifier": "id",
    "student id": "id",
    "customer id": "id",
    "voter id": "voters id",
    "voter identification number": "voters id",
    "ip address": "ip",
    "internet protocol address": "ip",
    "digital address": "location",
    "ration card number": "ration card",
    "aadhaar number": "aadhar",
    "aadhaar": "aadhar",
    "pan number": "pan",
    "pan card": "pan",
    "license number": "drivers_license",
    "passport number": "passport",
    "credit card number": "creditcard",
    "credit card": "creditcard",
    "bank account number": "bank_account",
    "account number": "bank_account",
    "bank account": "bank_account",
    "payment information": "bank_account",
    "insurance": "insurance",
    "tax id": "tin",
    "tax identification number": "tin",
    "driver license": "drivers_license",
    "passport id": "passport",
    "aadhar card": "aadhar",
    "driving license": "drivers_license",
    "passport": "passport",
    "health record number": "medical",
    "medical record number": "medical",
    "medical history": "medical",
    "transaction_id": "transaction_id",
}

# Load the tokenizer and model for Named Entity Recognition (NER)
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
ner = pipeline("ner", model=model, tokenizer=tokenizer)

def detect_using_regex(input_str: str):
    """
    Detects PII fields in a string using regex patterns.

    input: string
    output: list of PII detected along with their type (e.g., email, aadhar number)
    """
    pii = []
    for key, pattern in pii_patterns.items():
        matches = re.findall(pattern, input_str)
        for match in matches:
            pii.append([match, key])
    
    return pii

def detect_using_ner(input_str: str):
    """
    Detects PII fields in a string using Named Entity Recognition (NER).

    input: string
    output: list of PII detected along with their type (e.g., person, organization)
    """
    pii = []
    ner_results = ner(input_str)
    for instance in ner_results:
        word = instance["word"]
        entity = instance["entity"]

        # Handle subtokenization from tokenizer
        if (word[0] == "#" and len(pii) > 0):
            pii[-1][0] += word[2:]
        # Handle multi-word entities
        elif entity[0] == "I" and len(pii) > 0 and pii[-1][1] == entity[2:]:
            word = " " + word
            pii[-1][0] += word
        # Append new NER results
        else:
            pii.append([word, entity[2:]])
    
    # Map NER labels to PII types
    for instance in pii:
        if instance[1] == "LOC":
            instance[1] = "location"
        elif instance[1] == "PER":
            instance[1] = "name"
        elif instance[1] == "ORG":
            instance[1] = "organization"
        else:
            instance[1] = "miscellaneous"

    return pii

def detect_using_cols(file_path):
    """
    Detects PII fields in a CSV file based on column names.

    input: CSV file path
    output: list of PII detected along with their type
    """
    df = pd.read_csv(file_path)
    columns = [col.lower() for col in df.columns]

    pii_detected_cols = []
    for col in columns:
        for pii_type in pii_cols.keys():
            if pii_type == col:
                pii_detected_cols.append([col, pii_cols[pii_type]])

    pii = []
    for col, pii_type in pii_detected_cols:
        for value in df[col].dropna():
            pii.append([value, pii_type])

    return pii

def detect_pii_from_string(input_str: str):
    """
    Detects PII fields from a string using both regex and NER methods.

    input: string
    output: combined list of PII detected from both methods
    """
    regex_pii = detect_using_regex(input_str)
    ner_pii = detect_using_ner(input_str)

    pii = regex_pii + ner_pii
    return pii

def detect_pii_from_csv(file_path):
    """
    Detects PII fields from a CSV file using column names and content.

    input: CSV file path
    output: combined list of PII detected from both column names and content
    """
    content = process_csv(file_path)
    column_pii = detect_using_cols(file_path)
    content_pii = detect_pii_from_string(content)
    
    pii = column_pii + content_pii
    return pii