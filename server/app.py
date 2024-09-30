from flask import Flask, request, jsonify, render_template, send_file
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
import sys
import pandas as pd
import json
from sqlalchemy import create_engine, inspect
from botocore.client import Config
import csv
from collections import defaultdict
from apscheduler.schedulers.background import BackgroundScheduler


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from model.main import get_pii


# Define paths to templates and static folders
templates_folder = os.path.join(current_dir, '..', 'client', 'templates')
static_folder = os.path.join(current_dir, '..', 'client', 'static')

app = Flask(__name__, template_folder=templates_folder, static_folder=static_folder)

# Path where files will be downloaded
download_dir = os.getcwd() + '\downloads'

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Memory-based storage for credentials (can be replaced with DB)
credentials = {
    "aws": None,
    "postgres": None
}

# Ensure the directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/configure')
def configure():
    return render_template('configure.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/get_analysis')
def get_analysis():
    analysis_json, pii_results_df = get_pii()
    print(analysis_json)
    return analysis_json
        
# AWS S3 Files Download Endpoint
@app.route('/get_files', methods=['POST'])
def get_files():
    data = request.json
    access_key = data.get('access_key')
    secret_key = data.get('secret_key')
    region = data.get('region')
    if not access_key or not secret_key or not region:
        return jsonify({"success": False, "message": "Missing AWS credentials"}), 400
    print("Fetching files from S3...")
    
    # Store AWS credentials in memory
    credentials['aws'] = {
        "access_key": access_key,
        "secret_key": secret_key,
        "region": region
    }
    return fetch_s3_files()
    # return jsonify({"success": True, "message": "AWS credentials stored successfully and files fetched."})

    


# AWS S3 Data Fetch Function
def fetch_s3_files():
    print("Fetching files from S3...")
    
    # Retrieve stored credentials
    aws_creds = credentials.get("aws")
    
    if not aws_creds:
        print("AWS credentials not set.")
        return

    access_key = aws_creds['access_key']
    secret_key = aws_creds['secret_key']
    region = aws_creds['region']
    # Retrieve stored credentials
    aws_creds = credentials.get("aws")
    
    if not aws_creds:
        print("AWS credentials not set.")
        return

    access_key = aws_creds['access_key']
    secret_key = aws_creds['secret_key']
    region = aws_creds['region']

    if not access_key or not secret_key or not region:
        return jsonify({"success": False, "message": "Missing AWS credentials"}), 400

    try:
        s3 = boto3.client('s3',
                          endpoint_url='http://localhost:4566',
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name=region,
                          config=Config(signature_version='s3v4'))

        buckets = s3.list_buckets()['Buckets']
        for bucket in buckets:
            bucket_name = bucket['Name']
            response = s3.list_objects_v2(Bucket=bucket_name)

            if 'Contents' in response:
                for obj in response['Contents']:
                    file_key = obj['Key']
                    file_path = os.path.join(download_dir, file_key)
                    s3.download_file(bucket_name, file_key, file_path)

        return jsonify({"success": True})

    except NoCredentialsError:
        return jsonify({"success": False, "message": "Invalid AWS credentials"}), 403
    except PartialCredentialsError:
        return jsonify({"success": False, "message": "Incomplete AWS credentials"}), 403
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



# PostgreSQL Connection Endpoint
@app.route('/connect_postgres', methods=['POST'])
def connect_postgres():
    data = request.json
    db_host = data.get('db_host')
    db_port = data.get('db_port')
    db_name = data.get('db_name')
    db_user = data.get('db_user')
    db_password = data.get('db_password')

    if not all([db_host, db_port, db_name, db_user, db_password]):
        return jsonify({"success": False, "message": "Missing PostgreSQL credentials"}), 400

    credentials['postgres'] = {
        "db_host": db_host,
        "db_port": db_port,
        "db_name": db_name,
        "db_user": db_user,
        "db_password": db_password
    }

    return fetch_postgres_data()
    

def fetch_postgres_data():
    print("Fetching data from PostgreSQL...")
    
    # Retrieve stored credentials
    postgres_creds = credentials.get("postgres")
    
    if not postgres_creds:
        print("PostgreSQL credentials not set.")
        return
    

    db_host = postgres_creds['db_host']
    db_port = postgres_creds['db_port']
    db_name = postgres_creds['db_name']
    db_user = postgres_creds['db_user']
    db_password = postgres_creds['db_password']

    try:
        # Connect to PostgreSQL
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

        # Create an inspector object to get table names
        inspector = inspect(engine)

        # Get all table names
        table_names = inspector.get_table_names()

        # Loop through all tables and save them as CSV
        for table_name in table_names:
            # Load table into a pandas DataFrame
            query = f'SELECT * FROM {table_name}'
            df = pd.read_sql(query, engine)
            
            # Create the CSV file path
            csv_file_path = os.path.join(download_dir, f'{table_name}.csv')
            
            # Check if the CSV file already exists
            # if os.path.exists(csv_file_path):
            #     print(f"CSV file for table {table_name} already exists at {csv_file_path}. Skipping...")
            # else:
                # Save DataFrame to CSV with the table name as the file name
            df.to_csv(csv_file_path, index=False)
            print(f"Table {table_name} has been written to {csv_file_path}")

        # Close the database connection
        engine.dispose()

        return jsonify({"success": True, "tables": [table for table in table_names]})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
# Schedule the functions to run every 30 minutes
scheduler.add_job(func=fetch_s3_files, trigger="interval", minutes=2)
scheduler.add_job(func=fetch_postgres_data, trigger="interval", minutes=2)
# Start the scheduler
scheduler.start()


@app.route('/download_csv', methods=['GET'])
def download_csv():
    path = os.getcwd()
    path = path[0:-7]
    path += r"\assets\results\output.csv"
    return send_file(path, as_attachment=True)

@app.route('/get_results', methods=['GET'])
def get_results():
    analysis_json, pii_results_df = get_pii()
    analysis = read_csv_data()
    return jsonify(analysis)

# Function to read the CSV and build the data structure
def read_csv_data():
    pii_data = {
        "pii_counts_per_file": defaultdict(int),  # {'file_name': pii_count}
        "risk_per_file": defaultdict(float),  # {'file_name': risk_sum}
        "mean_risk_per_file": {},  # {'file_name': mean_risk}
        "categories_per_file": defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # {'file_name': {'category': {'sub_category': pii_count}}}
    }
    
    # Reading the CSV file
    path = os.getcwd()
    path = path[0:-7]
    path += r"\assets\results\output.csv"
    with open(path, 'r') as csvfile:  # Replace with your file path
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            file_name = row['file name']
            category = row['category']
            bucket = row['bucket']
            risk = row['risk']
            # file_extension = row['file extension']
            # risk_category = row['risk_category']
            
            # Parse risk as float (or skip if it's empty)
            if risk:
                risk = float(risk)
            else:
                risk = 0

            # Increment PII count for each file
            pii_data["pii_counts_per_file"][file_name] += 1
            
            # Add risk to the total risk for the file
            pii_data["risk_per_file"][file_name] += risk

            # Add category and subcategory PII count for each file
            pii_data["categories_per_file"][file_name][bucket][category] += 1

    # Calculate mean risk per file
    for file_name in pii_data["pii_counts_per_file"]:
        pii_count = pii_data["pii_counts_per_file"][file_name]
        total_risk = pii_data["risk_per_file"][file_name]
        pii_data["mean_risk_per_file"][file_name] = total_risk / pii_count if pii_count > 0 else 0

    return pii_data

if __name__ == '__main__':
    app.run(debug=True)
