import boto3
import time

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    instance_id = event.get("existing-instance-id")
    if not instance_id:
        raise Exception("existing-instance-id required")

    name = f"ami-from-{instance_id}-{int(time.time())}"
    resp = ec2.create_image(InstanceId=instance_id, Name=name, NoReboot=True)

    image_id = resp["ImageId"]

    # Wait for AMI to be available (OPTIONAL – can remove if Step Function waits)
    while True:
        desc = ec2.describe_images(ImageIds=[image_id])
        state = desc["Images"][0]["State"]
        if state == "available":
            break
        time.sleep(5)

    return {
        **event,
        "ami_id": image_id
    }
