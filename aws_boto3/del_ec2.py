import boto3

# Initialize the AWS clients
ec2_client = boto3.client('ec2')

def delete_stopped_instances_and_volumes():
    # Step 1: Describe all instances
    response = ec2_client.describe_instances()
    
    # List to keep track of instances and volumes to be deleted
    instances_to_terminate = []
    volumes_to_delete = set()
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Check if the instance is stopped
            if instance['State']['Name'] == 'stopped':
                instance_id = instance['InstanceId']
                instances_to_terminate.append(instance_id)
                
                # Collect volumes attached to the instance
                for volume in instance.get('BlockDeviceMappings', []):
                    volume_id = volume['Ebs']['VolumeId']
                    volumes_to_delete.add(volume_id)
    
    # Step 2: Terminate the stopped instances
    if instances_to_terminate:
        print(f"Terminating instances: {instances_to_terminate}")
        ec2_client.terminate_instances(InstanceIds=instances_to_terminate)
    else:
        print("No stopped instances to terminate.")
    
    # Step 3: Delete the volumes
    for volume_id in volumes_to_delete:
        print(f"Deleting volume: {volume_id}")
        ec2_client.delete_volume(VolumeId=volume_id)

if __name__ == "__main__":
    delete_stopped_instances_and_volumes()
