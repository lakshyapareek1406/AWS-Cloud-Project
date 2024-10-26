#!/usr/bin/env python3
import cgi
import boto3
import os

def upload_to_s3(bucket_name, file_item):
    s3 = boto3.client('s3')
    s3.upload_fileobj(file_item.file, bucket_name, file_item.filename)
    return f"File '{file_item.filename}' uploaded successfully to '{bucket_name}'."

def main():
    print("Content-Type: text/html")
    print()  # End of headers

    form = cgi.FieldStorage()
    file_item = form['audioFile']
    bucket_name = form.getvalue('bucketName')

    if file_item and bucket_name:
        try:
            message = upload_to_s3(bucket_name, file_item)
            print(f"<h3>{message}</h3>")
        except Exception as e:
            print(f"<h3>Error: {str(e)}</h3>")
    else:
        print("<h3>Missing file or bucket name!</h3>")

if __name__ == '__main__':
    main()
