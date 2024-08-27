import boto3

def get_all_snapshots():
    ec2_client = boto3.client('ec2')
    snapshots = []
    next_token = None
    
    while True:
        response = ec2_client.describe_snapshots(OwnerIds=['self'], NextToken=next_token if next_token else None)
        snapshots.extend(response['Snapshots'])
        next_token = response.get('NextToken')
        if not next_token:
            break

    return snapshots

def get_attached_snapshots():
    ec2_client = boto3.client('ec2')
    volumes = ec2_client.describe_volumes(Filters=[{'Name': 'snapshot-id', 'Values': ['*']}])
    attached_snapshot_ids = {volume['SnapshotId'] for volume in volumes['Volumes']}
    return attached_snapshot_ids

def delete_snapshots(snapshot_ids):
    ec2_client = boto3.client('ec2')

    for snapshot_id in snapshot_ids:
        try:
            print(f"Deleting snapshot: {snapshot_id}")
            ec2_client.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Successfully deleted snapshot: {snapshot_id}")
        except Exception as e:
            print(f"Error deleting snapshot {snapshot_id}: {e}")

def main():
    all_snapshots = get_all_snapshots()
    attached_snapshot_ids = get_attached_snapshots()

    # Identify detached snapshots
    detached_snapshots = [snapshot['SnapshotId'] for snapshot in all_snapshots if snapshot['SnapshotId'] not in attached_snapshot_id
    ]