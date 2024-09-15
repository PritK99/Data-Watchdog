import numpy as np
import pandas as pd
import json

# Initialize the analysis dictionary
analysis_dict = {}

def analyze(df):
    # Extract file extensions from the 'file name' column
    df['file extension'] = df['file name'].apply(lambda x: x.split('.')[-1] if '.' in x else 'unknown')

    # Convert NumPy types to native Python types for JSON serialization
    def to_python_type(x):
        if isinstance(x, (np.int64, np.int32, np.int16, np.int8)):
            return int(x)
        elif isinstance(x, (np.float64, np.float32)):
            return float(x)
        elif isinstance(x, (np.bool_,)):
            return bool(x)
        return x

    # Calculate total risks
    analysis_dict["total_risks"] = to_python_type(len(df))
    
    # Calculate mean risk score and round to two decimal places
    analysis_dict["mean_risk_score"] = round(to_python_type(df["risk"].mean()), 2)
    
    # Calculate bucket distribution
    analysis_dict["bucket distribution"] = {to_python_type(k): to_python_type(v) for k, v in df["bucket"].value_counts().to_dict().items()}
    
    # Calculate PII counts per file
    analysis_dict["pii_counts_per_file"] = {to_python_type(k): to_python_type(v) for k, v in df['file name'].value_counts().to_dict().items()}
    
    # Calculate PII counts per file type (extension)
    analysis_dict["pii_counts_per_file_type"] = {to_python_type(k): to_python_type(v) for k, v in df['file extension'].value_counts().to_dict().items()}
    
    # Calculate mean risk per file extension
    mean_risk_per_extension = df.groupby('file extension')['risk'].mean().to_dict()
    analysis_dict["mean_risk_per_file_type"] = {
        to_python_type(ext): round(to_python_type(mean_risk), 2)
        for ext, mean_risk in mean_risk_per_extension.items()
    }
    
    # Calculate mean risk per file
    mean_risk_per_file = df.groupby('file name')['risk'].mean().to_dict()
    analysis_dict["mean_risk_per_file"] = {
        to_python_type(file): round(to_python_type(mean_risk), 2)
        for file, mean_risk in mean_risk_per_file.items()
    }
    
    # Calculate risk distribution
    risk_distribution = {
        "low": to_python_type(((df["risk"] >= 0) & (df["risk"] <= 5)).sum()),
        "medium": to_python_type(((df["risk"] >= 6) & (df["risk"] <= 8)).sum()),
        "high": to_python_type((df["risk"] >= 9).sum())
    }

    analysis_dict["risk_distribution"] = risk_distribution

    # Calculate top 5 categories with their counts
    top_categories = df['category'].value_counts().head(5).to_dict()
    analysis_dict["top_categories"] = {
        to_python_type(cat): to_python_type(count)
        for cat, count in top_categories.items()
    }

    # Convert the analysis dictionary to a JSON string
    analysis_json = json.dumps(analysis_dict, indent=4)
    
    return analysis_json