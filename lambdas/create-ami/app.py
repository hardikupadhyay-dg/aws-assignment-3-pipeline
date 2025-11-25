# import boto3
# import time

# ec2 = boto3.client('ec2')

# def lambda_handler(event, context):
#     instance_id = event.get("existing-instance-id")
#     if not instance_id:
#         raise Exception("existing-instance-id required")

#     name = f"ami-from-{instance_id}-{int(time.time())}"
#     resp = ec2.create_image(InstanceId=instance_id, Name=name, NoReboot=True)

#     image_id = resp["ImageId"]

#     while True:
#         desc = ec2.describe_images(ImageIds=[image_id])
#         state = desc["Images"][0]["State"]
#         if state == "available":
#             break
#         time.sleep(5)

#     return {
#         **event,
#         "ami_id": image_id
#     }


# lambdas/create-ami/app.py
import boto3
import time
import os

ec2 = boto3.client('ec2', region_name=os.environ.get("AWS_REGION"))

def lambda_handler(event, context):
    instance_id = (
        event.get("existing-instance-id")
        or event.get("InstanceId")
        or event.get("instance_id")
    )
    if not instance_id:
        raise Exception("existing-instance-id required")

    name = f"ami-from-{instance_id}-{int(time.time())}"
    resp = ec2.create_image(
        InstanceId=instance_id,
        Name=name,
        NoReboot=True
    )

    image_id = resp.get("ImageId")
    if not image_id:
        raise Exception("Failed to create AMI")

    # Wait until AMI becomes available
    waiter = ec2.get_waiter("image_available")
    waiter.wait(ImageIds=[image_id])

    return {
        "ImageId": image_id
    }
