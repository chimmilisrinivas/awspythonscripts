import boto3

# create client for ec2 service and pass aws_access_key_id and aws_secret_access_key as parameter
client = boto3.client('ec2', region_name='us-east-1', aws_access_key_id= 'AWS_ACCESS_KEY_ID',
                          aws_secret_access_key= 'AWS_SECRET_ACCESS_KEY' )
# dictionary with names of databases or instances as key and their volume ids as value that we had created previously
volumes_dict = {
                  'database-1' : 'volume-id-1',
                  'database-2' : 'volume-id-2',
                  'database-3' : 'volume-id-3',
          }
# create a list of snapshot-ids which were deleted successfully
deleted_snapshots = []
# working for each volumeid
for snapshot in volumes_dict:
    snapshots_list = client.describe_snapshots(Filters=[
        {
            'Name': 'volume-id',
            'Values': [
                '{}'.format(volumes_dict[snapshot]),
            ]
        },
    ])
    # snapshots_list is the response dictionary of client.describe_snapshots() method which contains 
    # 'Snapshots' and 'ResponseMetadata'. snapshots_list['Snapshots'] is list of snapshot ids of given volume-id
    # roughly the structure of snapshots_list would be {'Snapshots': ['snap1','snap2'], 'ResponseMetadata': {'RequestId': '757f9e'...}}
    if snapshots_list['ResponseMetadata']['HTTPStatusCode'] == 200:
        # iterate through the list of snapshot ids of snapshots_list['Snapshots'] and perform deletion of each
        for snapshot_id in snapshots_list['Snapshots']:
            response = client.delete_snapshot(SnapshotId=snapshot_id, DryRun=False)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                deleted_snapshots.append(snapshot_id)
# print the snapshot-ids which were deleted successfully
print(deleted_snapshots)