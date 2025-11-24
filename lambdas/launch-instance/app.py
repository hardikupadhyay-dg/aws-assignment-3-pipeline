# import boto3
# import os

# ec2 = boto3.client('ec2')

# def lambda_handler(event, context):
#     image_id = event.get('ImageId')
#     if not image_id:
#         raise Exception("ImageId required")

#     instance_type = "t2.micro"

#     response = ec2.run_instances(
#         ImageId=image_id,
#         InstanceType=instance_type,
#         MinCount=1,
#         MaxCount=1,
#         KeyName=os.environ.get("KEY_NAME"),
#         NetworkInterfaces=[{
#             "AssociatePublicIpAddress": True,
#             "DeviceIndex": 0,
#             "SubnetId": os.environ.get("SUBNET_ID"),
#             "Groups": [os.environ.get("SG_ID")]
#         }]
#     )

#     return {
#         "InstanceId": response["Instances"][0]["InstanceId"]
#     }


# lambdas/launch-instance/app.py
import boto3
import os

ec2 = boto3.client('ec2', region_name=os.environ.get("AWS_REGION"))

def lambda_handler(event, context):
    # Accept several possible names for flexibility
    image_id = event.get('ami_id') or event.get('ImageId') or event.get('imageId')
    if not image_id:
        raise Exception("ImageId / ami_id required in event")

    instance_type = os.environ.get("INSTANCE_TYPE", "t2.micro")

    response = ec2.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=os.environ.get("KEY_NAME"),
        NetworkInterfaces=[{
            "AssociatePublicIpAddress": True,
            "DeviceIndex": 0,
            "SubnetId": os.environ.get("SUBNET_ID"),
            "Groups": [os.environ.get("SG_ID")]
        }]
    )

    return {
        "InstanceId": response["Instances"][0]["InstanceId"]
    }
