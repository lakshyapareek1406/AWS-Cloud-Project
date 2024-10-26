import json
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event: %s", json.dumps(event))  # Log the incoming event

    s3_client = boto3.client('s3')
    transcribe_client = boto3.client('transcribe')

    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        logger.info("Bucket: %s, File Key: %s", bucket_name, file_key)

        job_name = f"TranscriptionJob-{file_key.split('/')[-1].split('.')[0]}"
        file_uri = f"s3://{bucket_name}/{file_key}"

        # Start transcription job
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat=file_key.split('.')[-1],  # Extract file extension
            LanguageCode='en-US'  # Change as per the audio file's language
        )
        logger.info("Started transcription job: %s", response)

        return {
            'statusCode': 200,
            'body': json.dumps(f"Started transcription job: {job_name}")
        }

    except Exception as e:
        logger.error("Error: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
