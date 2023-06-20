import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name="eu-west-1")

volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Environment',
                'Values': ['prod']
            }
        ]
    )

for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )

    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    #only delete the ones older than the most recent two snapshots
    for snap in sorted_by_date:
        ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )

