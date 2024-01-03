import boto3
import json
import requests
import os

def format_resource_list(resource_name, resource_list):
    if resource_list:
        formatted_string = f"{resource_name}: {', '.join(resource_list)}"
        return formatted_string
    else:
        return None

def send_message_to_google_chat(webhook_url, message_text):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    message = {
        'text': message_text
    }

    payload = {
        'text': json.dumps(message)
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

# Call the function to send the message
def lambda_handler(event, context):
    # Create an EC2 client
    ec2 = boto3.client('ec2')

    existing_instance_list = ec2.describe_instances()

    instance_ids = []

    for reservation in existing_instance_list['Reservations']:
        state = reservation['State']['Name']
        if reservation['State']['Name']  == 'available':
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_ids.append(instance_id)
    
    # Check EBS volumes
    existing_volume_list = ec2.describe_volumes()

    volume_ids = []

    for volume in existing_volume_list['Volumes']:
        volume_id = volume['VolumeId']
        volume_ids.append(volume_id)

    vpc_ids = []
    nat_gateway_ids = []
    internet_gateway_ids = []

    # Get a list of all VPCs
    vpcs = ec2.describe_vpcs()['Vpcs']

    for vpc in vpcs:
        if 'Tags' in vpc and any(tag['Key'] == 'Name' and tag['Value'] == 'default' for tag in vpc['Tags']):
            continue

        vpc_ids.append(vpc['VpcId'])

    nat_gateways = ec2.describe_nat_gateways()['NatGateways']
    for nat_gateway in nat_gateways:
        if nat_gateway['State']  == 'available':
            nat_gateway_ids.append(nat_gateway['NatGatewayId'])

    internet_gateways = ec2.describe_internet_gateways()['InternetGateways']
    for internet_gateway in internet_gateways:
        if 'Tags' in internet_gateway and any(tag['Key'] == 'Name' and tag['Value'] == 'default' for tag in internet_gateway['Tags']):
            continue
        internet_gateway_ids.append(internet_gateway['InternetGatewayId'])

    # CHECK EKS   
    eks = boto3.client('eks')

    eks_cluster_names = []

    eks_cluster_list = eks.list_clusters()

    for cluster_name in eks_cluster_list['clusters']:
        cluster_details = eks.describe_cluster(name=cluster_name)
        eks_cluster_names.append(cluster_details['cluster']['name'])

    # Check ECS resources
    ecs = boto3.client('ecs')

    ecs_cluster_names = []

    ecs_list = ecs.list_clusters()

    for cluster_arn in ecs_list['clusterArns']:
        cluster_name = cluster_arn.split('/')[-1]
        ecs_cluster_names.append(cluster_name)

    # Check RDS resource
    rds = boto3.client('rds')

    rds_instance_names = []

    response = rds.describe_db_instances()

    for db_instance in response['DBInstances']:
        rds_instance_names.append(db_instance['DBInstanceIdentifier'])

    # Check redshift
    redshift = boto3.client('redshift')

    redshift_cluster_names = []

    redshift_list = redshift.describe_clusters()

    for cluster in redshift_list['Clusters']:
        redshift_cluster_names.append(cluster['ClusterIdentifier'])
        
    # Check Elasticache
    elasticache = boto3.client('elasticache')

    redis_cluster_names = []

    redis_list = elasticache.describe_cache_clusters()

    for cluster in redis_list['CacheClusters']:
        if is_valid_identifier(cluster['CacheClusterId']):
            redis_cluster_names.append(cluster['CacheClusterId'])
        else:
            print(f"Invalid CacheClusterId: {cluster['CacheClusterId']}")
    
    formatted_strings = [
        format_resource_list("Redis Clusters", redis_cluster_names),
        format_resource_list("ECS Clusters", ecs_cluster_names),
        format_resource_list("Redshift Clusters", redshift_cluster_names),
        format_resource_list("RDS Instances", rds_instance_names),
        format_resource_list("EKS Clusters", eks_cluster_names),
        format_resource_list("Volume IDs", volume_ids),
        format_resource_list("VPC IDs", vpc_ids),
        format_resource_list("NAT Gateway IDs", nat_gateway_ids),
        format_resource_list("Internet Gateway IDs", internet_gateway_ids),
        format_resource_list("Instance IDs", instance_ids)
    ]
    # Notification part
    webhook_url = os.environ.get('WEBHOOK_URL')
    formatted_strings = [s for s in formatted_strings if s is not None]
    if formatted_strings:
        message_text = "DELETE ME: " + ", ".join(formatted_strings)
        send_message_to_google_chat(webhook_url, message_text)
    else:
        print("No formatted strings to send.")
