from flask import Flask, request, jsonify, render_template
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
import sys
import pandas as pd
from sqlalchemy import create_engine, inspect
from botocore.client import Config

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importing models
from model.main import get_pii

app = Flask(__name__)

# Path where files will be downloaded
download_dir = os.getcwd() + '\downloads'

# Ensure the directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

@app.route('/')
def index():
    return render_template('index.html')

# AWS S3 Files Download Endpoint
@app.route('/get_files', methods=['POST'])
def get_files():
    data = request.json
    access_key = data.get('access_key')
    secret_key = data.get('secret_key')
    region = data.get('region')

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
            if os.path.exists(csv_file_path):
                print(f"CSV file for table {table_name} already exists at {csv_file_path}. Skipping...")
            else:
                # Save DataFrame to CSV with the table name as the file name
                df.to_csv(csv_file_path, index=False)
                print(f"Table {table_name} has been written to {csv_file_path}")

        # Close the database connection
        engine.dispose()

        return jsonify({"success": True, "tables": [table for table in table_names]})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/get_analytics', methods=['GET'])
def get_analytics():
    # The results are also stored in assets folder
    analysis_json, pii_results_df = get_pii()
    return analysis_json

if __name__ == '__main__':
    app.run(debug=True)