import boto3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize AWS clients with region
REGION_NAME = 'us-east-1'  # Replace with your desired region
s3_client = boto3.client('s3', region_name=REGION_NAME)
ses_client = boto3.client('ses', region_name=REGION_NAME)

# Replace these with your values
BUCKET_NAME = 'kun-demo-bucket'  # Replace with your S3 bucket name
FILE_NAME = 'hello.txt'           # The name of the file in S3 (should contain email IDs)
FROM_EMAIL = 'your_verified_email@example.com'  # Replace with your verified SES email

def lambda_handler(event, context):
    # Step 1: Retrieve the email file from S3
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        email_content = response['Body'].read().decode('utf-8')
        email_ids = email_content.splitlines()
        logging.info(f"Retrieved email IDs: {email_ids}")
    except Exception as e:
        logging.error(f"Error retrieving file from S3: {e}")
        return {
            'statusCode': 500,
            'body': f"Error retrieving file from S3: {str(e)}"
        }

    # Step 2: Send an email to each email ID
    for email_id in email_ids:
        send_email(email_id)

    return {
        'statusCode': 200,
        'body': 'Emails sent successfully!'
    }

def send_email(to_email):
    try:
        response = ses_client.send_email(
            Source=FROM_EMAIL,
            Destination={
                'ToAddresses': [to_email],
            },
            Message={
                'Subject': {
                    'Data': 'Hello from AWS Lambda and SES',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'This is a test email sent from an AWS Lambda function.',
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        logging.info(f"Email sent to {to_email}: {response['MessageId']}")
    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {e}")

# Uncomment the following lines if you want to test the function locally
# if __name__ == "__main__":
#     lambda_handler(None, None)
