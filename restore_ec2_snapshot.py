import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name="eu-west-1")
ec2_resource = boto3.resource('ec2', region_name="eu-west-1")

instance_id = "i-0629b6fee94933959"

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

#get the latest volume from the instance
instance_volume = volumes['Volumes'][0]
print(instance_volume)

#View all snapshots created from this volume
snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        }
    ]
)

#the latest snapshot for this
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

#the latest snapshot for instance
print(latest_snapshot['StartTime'])

#create volume from snapshot
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="eu-west-1c",
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Environment',
                    'Value': 'prod'
                }
            ]
        }
    ]
)

#wait for volume to get created and become available
while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)
    if vol.state == 'available':
        # attach volume to EC2 instance
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/sdf'
        )
        #break or you'll get an infinite loop
        break
