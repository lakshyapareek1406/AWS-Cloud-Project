def configure_aws_session():
    session = boto3.Session(
        aws_access_key_id='AKIAxxxxxx',        
        aws_secret_access_key='xxxxxxxx', 
        region_name='us-west-2'                     
    )
    return session

def launch_rhel_gui_instance(session):
    ec2_client = session.client('ec2')

    # Replace with valid RHEL AMI ID for your region
    ami_id = 'ami-xxxxxxxxxxxxxxx'
    instance_type = 't2.large'
    key_name = 'my-key-pair'

    try:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'RHEL-GUI-Instance'
                        },
                    ]
                },
            ]
        )

        instance_id = response['Instances'][0]['InstanceId']
        print(f"RHEL GUI instance launched with ID: {instance_id}")

        # Wait for the instance to be in a running state
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is now running.")

    except Exception as e:
        print(f"Failed to launch RHEL GUI instance: {e}")

def main():
    session = configure_aws_session()
    launch_rhel_gui_instance(session)

if __name__ == "__main__":
    main()
