import boto3

ec2_client_ireland = boto3.client('ec2')

ec2_client_frankfurt = boto3.client('ec2', region_name="eu-central-1")

instances_ids_ireland = []
instances_ids_frankfurt = []


reservations_ireland = ec2_client_ireland.describe_instances()['Reservations']
#This will iterate through all reservations, and add all instance ids to a list
for res in reservations_ireland:
    instances = res['Instances']
    for ins in instances:
        #collect all intance ids into a list
        instances_ids_ireland.append(ins['InstanceId'])


reservations_frankfurt = ec2_client_frankfurt.describe_instances()['Reservations']
for res in reservations_frankfurt:
    instances = res['Instances']
    for ins in instances:
        #collect all intance ids into a list
        instances_ids_frankfurt.append(ins['InstanceId'])


print(instances_ids_ireland)
print(instances_ids_frankfurt)


response = ec2_client_ireland.create_tags(
    Resources=instances_ids_ireland,
    Tags=[
        {
            'Key': 'region',
            'Value': 'Ireland'
        },
    ]
)

