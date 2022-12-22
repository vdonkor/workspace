import boto3

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
subnets = get_subnets(tw_details[]["VpcId"])
print(subnets)
