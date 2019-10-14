import boto3
import logging
from botocore.exceptions import ClientError

def create_sec_group(SECURITY_GROUP_NAME, Description, vpc_id):
    """Creating Sec Group"""
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
    """Create security group and define Ingress rules"""
    try:
        response = ec2.create_security_group(GroupName=SECURITY_GROUP_NAME,
                                            Description=Description,
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)
    return security_group_id

def change_instance_security_groups(instance_id, security_group_ids):
    """Change the security groups assigned to an EC2 instance"""
    # Retrieve the IDs of the network interfaces attached to the EC2 instance
    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
    except ClientError as e:
        logging.error(e)
        return False
    instance_info = response['Reservations'][0]['Instances'][0]

    # Assign the security groups to each network interface
    for network_interface in instance_info['NetworkInterfaces']:
        try:
            ec2_client.modify_network_interface_attribute(
                NetworkInterfaceId=network_interface['NetworkInterfaceId'],
                Groups=security_group_ids)
        except ClientError as e:
            logging.error(e)
            return False
    return True
      

def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # create sec group and define ingress rules
    sec_group_id = create_sec_group("test_sec", "Secgroup", "xxxxxxx")
    security_group_ids = list()
    security_group_ids.append(sec_group_id)
    change_instance_security_groups("xxxxxxxxxxx", security_group_ids)
if __name__ == '__main__':
    main()
