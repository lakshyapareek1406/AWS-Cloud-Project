#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3
from botocore.exceptions import ClientError

cgitb.enable()  # Enable debugging

def main():
    print("Content-Type: application/json")
    print()  # End of headers

    form = cgi.FieldStorage()
    region = form.getvalue('region')
    aws_access_key_id = form.getvalue('aws_access_key_id')
    aws_secret_access_key = form.getvalue('aws_secret_access_key')
    instance_type = form.getvalue('instance_type')
    image_id = form.getvalue('image_id')

    if not (region and aws_access_key_id and aws_secret_access_key and instance_type and image_id):
        response = {"error": "All fields are required"}
        print(json.dumps(response))
        return

    try:
        ec2 = boto3.resource(
            "ec2",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        instance = ec2.create_instances(
            InstanceType=instance_type,
            ImageId=image_id,
            MaxCount=1,
            MinCount=1
        )
        instance_id = instance[0].id
        response = {"success": f"Instance created successfully! Instance ID: {instance_id}"}
    except ClientError as e:
        response = {"error": str(e)}

    print(json.dumps(response))

if __name__ == "__main__":
    main()
