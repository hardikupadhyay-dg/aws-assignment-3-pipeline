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
    instance_id = event.get("existing-instance-id") or event.get("InstanceId") or event.get("instance_id")
    if not instance_id:
        raise Exception("existing-instance-id required in the event")

    # 1) make sure the instance exists (otherwise CreateImage will fail)
    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
    except ec2.exceptions.ClientError as e:
        raise

    reservations = resp.get("Reservations", [])
    if not reservations or not reservations[0].get("Instances"):
        raise Exception(f"Instance {instance_id} not found")

    name = f"ami-from-{instance_id}-{int(time.time())}"
    try:
        resp = ec2.create_image(InstanceId=instance_id, Name=name, NoReboot=True)
    except Exception as e:
        # bubble up with clear message
        raise

    image_id = resp["ImageId"]

    # Wait for image to become 'available'
    waiter = ec2.get_waiter('image_available')
    waiter.wait(ImageIds=[image_id])

    # Refresh image data to find snapshot IDs
    desc = ec2.describe_images(ImageIds=[image_id])
    ami = desc["Images"][0]

    snapshot_ids = []
    for bd in ami.get("BlockDeviceMappings", []):
        ebs = bd.get("Ebs")
        if ebs and ebs.get("SnapshotId"):
            snapshot_ids.append(ebs["SnapshotId"])

    # Wait for each snapshot to be completed (if any)
    if snapshot_ids:
        snap_waiter = ec2.get_waiter('snapshot_completed')
        snap_waiter.wait(SnapshotIds=snapshot_ids)

    # Return ami_id for downstream steps
    return {
        **event,
        "ami_id": image_id
    }
