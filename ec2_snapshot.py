import boto3
import schedule

ec2_client = boto3.client('ec2', region_name="eu-west-1")

def create_volume_snapshots():
    volumes = ec2_client.describe_volumes(
        #only take snapshots of prod environments
        Filters=[
            {
                'Name': 'tag:Environment',
                'Values': ['prod']
            }
        ]
    )
    for volume in volumes['Volumes']:
        try:
            new_snapshot = ec2_client.create_snapshot(
                VolumeId=volume['VolumeId']
            )
            print(new_snapshot)
        except:
            print("something went wrong")

#schedule.every(20).seconds.do(create_volume_snapshots)
schedule.every().friday.at("12:00").do(create_volume_snapshots)

while True:
    schedule.run_pending()
