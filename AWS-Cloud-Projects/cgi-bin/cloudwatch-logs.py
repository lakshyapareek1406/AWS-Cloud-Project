#!/usr/bin/env python3
import cgi
import boto3
import json
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Fetching AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', 'your-default-access-key')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'your-default-secret-key')

# Function to fetch CloudWatch logs
def fetch_logs(log_group_name, log_stream_name, region_name):
    try:
        client = boto3.client('logs',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name)

        response = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            limit=10  # Adjust as needed
        )

        logs = []
        for event in response['events']:
            logs.append({
                'timestamp': event['timestamp'],
                'message': event['message']
            })

        return logs

    except NoCredentialsError:
        return {'error': 'AWS credentials not found'}
    except PartialCredentialsError:
        return {'error': 'Incomplete AWS credentials'}
    except Exception as e:
        return {'error': str(e)}

# Main CGI script handling
def main():
    print("Content-Type: application/json")
    print()  # Blank line required, end of headers

    form = cgi.FieldStorage()
    log_group_name = form.getvalue('log_group_name')
    log_stream_name = form.getvalue('log_stream_name')
    region_name = form.getvalue('region_name')

    # Input validation
    if not log_group_name:
        print(json.dumps({'error': 'Missing log group name'}))
        return
    if not log_stream_name:
        print(json.dumps({'error': 'Missing log stream name'}))
        return
    if not region_name:
        print(json.dumps({'error': 'Missing AWS region'}))
        return

    # Fetch logs
    logs = fetch_logs(log_group_name, log_stream_name, region_name)
    print(json.dumps(logs, indent=4))

if __name__ == '__main__':
    main()
