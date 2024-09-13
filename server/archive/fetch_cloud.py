import boto3
from botocore.client import Config

# Create a session and S3 client
s3 = boto3.client('s3',
                  endpoint_url='http://localhost:4566',  # LocalStack endpoint
                  aws_access_key_id='test',  # Dummy credentials for LocalStack
                  aws_secret_access_key='test',
                  region_name='us-east-1',
                  config=Config(signature_version='s3v4'))

bucket_name = 'my-pii-bucket'

# List all objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

if 'Contents' in response:
    for obj in response['Contents']:
        file_key = obj['Key']
        download_path = f".\excel\{file_key}"  # Save to local file system, keeping the original name
        
        # Download the file
        print(f"Downloading {file_key}...")
        s3.download_file(bucket_name, file_key, download_path)
        print(f"File {file_key} downloaded to {download_path}")
else:
    print(f"No files found in bucket {bucket_name}")
