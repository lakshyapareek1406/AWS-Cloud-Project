#!/usr/bin/env python
import cgi
import boto3
import os
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Set up basic logging
logging.basicConfig(filename='/var/log/upload_to_s3.log', level=logging.DEBUG)

# CGI Response headers
print("Content-type:text/html\r\n\r\n")

form = cgi.FieldStorage()

# Environment variables for AWS credentials (you can set these in your OS)
region = os.getenv('AWS_REGION', 'your-default-region')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', 'your-access-key')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'your-secret-key')

try:
    # Get file data and bucket name from form
    file_item = form['file']
    bucket_name = form.getvalue('bucketName')

    if file_item and bucket_name:
        # Initialize S3 client
        s3 = boto3.client(
            's3', 
            region_name=region,
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key
        )
        
        # Upload file to S3
        s3.upload_fileobj(file_item.file, bucket_name, file_item.filename)

        print(f"File '{file_item.filename}' uploaded successfully to '{bucket_name}'.")
    else:
        print("File or bucket name not provided.")

except NoCredentialsError:
    print("Error: AWS credentials not found.")
    logging.error("AWS credentials not found.")
except PartialCredentialsError:
    print("Error: Incomplete AWS credentials.")
    logging.error("Incomplete AWS credentials.")
except Exception as e:
    print(f"Error uploading file: {e}")
    logging.error(f"Exception occurred: {e}")

