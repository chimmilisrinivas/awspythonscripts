import boto3
import logging
import datetime
from botocore.exceptions import ClientError


def create_ec2_image():
    """
    The method creates AMIs for instances avaialble in the region
    """
    date = datetime.datetime.utcnow().strftime('%Y%m%d')
    instanceid_list = list()
    image_list = list()
    client = boto3.client('ec2')
    try:
        response = client.describe_instances()
        for instance in range(len(response['Reservations'][0]['Instances'])):
            instanceid_list.append(response['Reservations'][0]['Instances'][instance]['InstanceId'])
        for instanceid in instanceid_list:
            name = f"InstanceID_{instanceid}_Image_Backup_{date}"
            try:
                image_response = client.create_image(InstanceId=instanceid, Name=name)
                if image_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    image_list.append(image_response['ImageId'])
            except ClientError as e:
                logging.error(e)

    except ClientError as e:
        logging.error(e)
        return None
    return image_list


def main():
    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')
    # Create AMIs for Instances
    image_info = create_ec2_image()
    print(image_info)

if __name__ == '__main__':
    main()
