# This script performs the core functionality of extracting PII from string.
# We preprocess all major types of data forms to string format for PII Detection
import re
import logging
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Storing the results in a log file when using standalone
# logging.basicConfig(filename='detect.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Loading the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
ner = pipeline("ner", model=model, tokenizer=tokenizer)

# Patterns for PII used in step 2
patterns = {
        "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "IP": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        "PHONE": r'\b(?:\+91|91)?[789]\d{9}\b',
        "AADHAR": r'\b\d{4} \d{4} \d{4}\b',
        "PAN": r'\b[A-Z]{5}\d{4}[A-Z]\b',
        "PINCODE": r'\b\d{6}\b'
    }

"""
PII are detected from string using 2 ways
First, we use REGEX to extract PII which always follow a fixed pattern such as email address, IP address, Aadhar Number, etc.
Next, we use NER to extract PII such as Person name, Location, and Organization
"""
def detect_pii_from_string(input_str: str):
    pii = []

    # Step 1: Tokenizing the input text on space
    # We do not use the tokenizer here because of its subtokenizing approach
    tokenized_output = input_str.split()

    # Step 2: Performing Regex for different types of PII
    # This step handles EMAIL, IP, PHONE, AADHAR, PAN, PINCODE
    for key, pattern in patterns.items():
        matches = re.findall(pattern, input_str)
        for match in matches:
            pii.append([match, key])

    # Step 3: Performing NER and processing the result
    # This step handles PER, ORG, LOC
    ner_results = ner(input_str)
    for instance in ner_results:
        word = instance["word"]
        entity = instance["entity"]

        # This happens because of the subtokenization technique used by tokenizer
        if (word[0] == "#"):
            pii[-1][0] += word[2:]
        # This allows us to handle words like Vice City
        elif (entity[0] == "I" and len(pii) > 0 and pii[-1][1] == entity[2:]):
            word = " " + word
            pii[-1][0] += word
        # # We skip all MISC since they are not usually PII
        # elif (entity[2:] == "MISC"):
        #     continue
        # Appending new NERs
        else:
            pii.append([word, entity[2:]])

    # Logging the results when using standalone
    # logging.info(f'Detected PII: {pii}')

    return pii

# detect_pii_from_string("I live in Jelum Towers, Vice City, 400809, and I go by Sonny. I had an amazing drive through Vice City's neon-lit streets before heading to the storied Malibu Club for an exciting night of music that will never be forgotten. I'm constantly in awe of the city's breathtaking skyline and lively nightlife. Lance Vance, a buddy of mine, will see me shortly to discuss a mission. He is employed with The Dockyards. Using the IP address 172.182.99.1, he emailed me about the mission using the email address lancevance@gmail.com. A message from +919999999999 reached me as well. It appears to be authentic.")

"""
TO DO: PII detection from CSV and SQL dumps
       Binning of PII in categories like Biological, Financial, and Personal
       Better PII detection
"""