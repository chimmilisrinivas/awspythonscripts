import boto3
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

# website configuration 
s3 = boto3.client('s3')
s3.put_bucket_website(Bucket='awsboto3ibm',
                      WebsiteConfiguration=website_configuration)