import boto3

eks_client = boto3.client('eks')

#assign list of clusters to a list using the list_clusters function
clusters = eks_client.list_clusters()['clusters']

for cluster in clusters:
    response = eks_client.describe_cluster(
        name=cluster
    )
    cluster_status = response['cluster']['status']
    cluster_endoint = response['cluster']['endpoint']
    cluster_version = response['cluster']['version']
    print(f"Cluster {cluster} status is {cluster_status}")
    print(f"The endpoint is {cluster_endoint}")
    print(f"Version is {cluster_version}")
