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
# import boto3
# import os

# ec2 = boto3.client('ec2', region_name=os.environ.get("AWS_REGION"))

# def lambda_handler(event, context):
#     # Accept several possible names for flexibility
#     image_id = event.get('ami_id') or event.get('ImageId') or event.get('imageId')
#     if not image_id:
#         raise Exception("ImageId / ami_id required in event")

#     instance_type = os.environ.get("INSTANCE_TYPE", "t2.micro")

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



import boto3
import os

ec2 = boto3.client('ec2')

KEY_NAME = os.environ.get("KEY_NAME", "")
DEFAULT_INSTANCE_TYPE = os.environ.get("DEFAULT_INSTANCE_TYPE", "t2.micro")

def lambda_handler(event, context):
    image_id = event.get("ImageId")
    existing_instance_id = event.get("existing-instance-id")

    if not image_id or not existing_instance_id:
        raise Exception("ImageId and existing-instance-id required")

    # Describe existing instance
    desc = ec2.describe_instances(InstanceIds=[existing_instance_id])
    reservations = desc.get("Reservations", [])
    if not reservations:
        raise Exception("Existing instance not found")

    ins = reservations[0]["Instances"][0]

    instance_type = ins.get("InstanceType") or DEFAULT_INSTANCE_TYPE
    subnet_id = ins.get("SubnetId")
    sg_ids = [sg["GroupId"] for sg in ins.get("SecurityGroups", [])] or None
    key_name = ins.get("KeyName") or (KEY_NAME if KEY_NAME else None)

    params = {
        "ImageId": image_id,
        "InstanceType": instance_type,
        "MinCount": 1,
        "MaxCount": 1
    }
    if subnet_id:
        params["SubnetId"] = subnet_id
    if sg_ids:
        params["SecurityGroupIds"] = sg_ids
    if key_name:
        params["KeyName"] = key_name

    resp = ec2.run_instances(**params)
    new_id = resp["Instances"][0]["InstanceId"]

    try:
        ec2.create_tags(
            Resources=[new_id],
            Tags=[{"Key": "CreatedBy", "Value": "StepFunctionAmiFlow"}]
        )
    except:
        pass

    return {
        "new-instance-id": new_id
    }
