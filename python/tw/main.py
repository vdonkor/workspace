import boto3

ec2 = boto3.client("ec2")


def get_tw_attachment():
    resp = ec2.describe_transit_gateway_vpc_attachments()
    return [{"VpcId": tw["VpcId"], "SubnetIds": tw["SubnetIds"]} for tw in resp["TransitGatewayVpcAttachments"]]


tw_details = get_tw_attachment()
