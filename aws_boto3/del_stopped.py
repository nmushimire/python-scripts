import boto3

def terminate_stopped_instances():
    # Initialize the AWS EC2 client
    ec2_client = boto3.client('ec2')

    # Step 1: Describe all instances
    response = ec2_client.describe_instances()
    
    # List to keep track of instances to be terminated
    instances_to_terminate = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Check if the instance is stopped
            if instance['State']['Name'] == 'stopped':
                instances_to_terminate.append(instance['InstanceId'])
    
    # Step 2: Terminate the stopped instances
    if instances_to_terminate:
        print(f"Terminating instances: {instances_to_terminate}")
        ec2_client.terminate_instances(InstanceIds=instances_to_terminate)
        print("Termination request sent.")
    else:
        print("No stopped instances to terminate.")

if __name__ == "__main__":
    terminate_stopped_instances()
