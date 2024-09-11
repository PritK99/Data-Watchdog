import pandas as pd

# Dictionary mapping different PII categories to their corresponding bucket types
bucket_dict = {
    'aadhar': 'Personal',
    'address': 'Personal',
    'bank_account': 'Financial',
    'creditcard': 'Financial',
    'cvv': 'Financial',
    'dob': 'Personal',
    'drivers_license': 'Personal',
    'email': 'Personal',
    'financial': 'Financial',
    'ip': 'Miscellaneous',
    'location': 'Personal',
    'medical': 'Medical',
    'organization': 'Miscellaneous',
    'pan': 'Financial',
    'passport': 'Personal',
    'personal': 'Personal',
    'phone': 'Personal',
    'pincode': 'Personal',
    'ration card': 'Personal',
    'tin': 'Financial',
    'vin': 'Miscellaneous',
    'voters id': 'Personal'
}

# Dictionary mapping different PII categories to their corresponding risk scores
risk_dict = {
    'aadhar': 9,
    'address': 6,
    'bank_account': 9,
    'creditcard': 10,
    'cvv': 10,
    'dob': 7,
    'drivers_license': 8,
    'email': 5,
    'financial': 8,
    'ip': 4,
    'location': 6,
    'medical': 10,
    'organization': 3,
    'pan': 8,
    'passport': 9,
    'personal': 7,
    'phone': 6,
    'pincode': 5,
    'ration card': 8,
    'tin': 7,
    'vin': 4,
    'voters id': 7
}

def assign_bucket_and_risk(pii_result: list):
    """
    Assigns buckets and risk scores to PII results based on predefined dictionaries.
    
    input: pii_result (list) - List of PII records where each record is a list containing [PII field, category].
    output: processed_pii_results (list) - List of PII records with added bucket and risk information.
    """
    processed_pii_results = []
    for pii in pii_result:
        category = pii[1]  
        bucket = bucket_dict.get(category, 'Unknown')  # Get bucket type using bucket_dict, default to 'Unknown'
        risk = risk_dict.get(category, pd.NA)  # Get risk score using risk_dict, default to pandas NA
        pii.append(bucket) 
        pii.append(risk)  
        processed_pii_results.append(pii) 

    return processed_pii_results

def convert_to_csv(global_pii_results: list):
    """
    Converts processed PII results into a DataFrame and returns it.
    
    input: global_pii_results (list) - List of file results where each file result contains file name and list of PII results.
    output: df (DataFrame) - DataFrame containing the details of each PII record.
    """
    file_names = []
    pii_fields = []
    categories = []
    buckets = []
    risks = []

    for file_result in global_pii_results:
        file_name = file_result[0][21:] 
        file_pii = file_result[1] 

        for result in file_pii:
            pii_field = result[0]
            category = result[1]
            bucket = result[2]
            risk = result[3] 

            file_names.append(file_name)
            pii_fields.append(pii_field)
            categories.append(category)
            buckets.append(bucket)
            risks.append(risk)
    
    # Create a DataFrame from the lists
    df = pd.DataFrame({
        "file name": file_names,
        "pii field": pii_fields,
        "category": categories,
        "bucket": buckets,
        "risk": risks
    })

    return df