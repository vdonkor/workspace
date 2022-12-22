import boto3
import json

ec2 = boto3.client("ec2")


def get_tw_attachment():
    resp = ec2.describe_transit_gateway_vpc_attachments()
    return [{"VpcId": tw["VpcId"], "SubnetIds": tw["SubnetIds"]} for tw in resp["TransitGatewayVpcAttachments"]]


def get_subnets(vpc_id):
    resp = ec2.describe_subnets(
        Filters=[
            {
                "Name": "vpc-id",
                "Values": [
                    vpc_id
                ]
            },
        ],
    )
    return [{"SubnetId": subnet["SubnetId"], "AvailabilityZoneId": subnet["AvailabilityZoneId"]} for subnet in
            resp["Subnets"]]


tw_details = get_tw_attachment()
subnets = get_subnets(tw_details[0]["VpcId"])
print(json.dumps(subnets, indent=3))


tw_az_ids = [subnet["AvailabilityZoneId"] for subnet in subnets if subnet["SubnetId"] in tw_details[0]["SubnetIds"]]
unique_subnet_az_ids = list(set([subnet["AvailabilityZoneId"] for subnet in subnets]))

if len(unique_subnet_az_ids) > len(tw_az_ids):
    new_subnet_az_id = list(set(unique_subnet_az_ids) ^ set(tw_az_ids))
    # get all subnets with the new az ids
    unattached_subnet_ids = [subnet["SubnetId"] for subnet in subnets if subnet["AvailabilityZoneId"] in new_subnet_az_id]


print(tw_az_ids)
print(unique_subnet_az_ids)
