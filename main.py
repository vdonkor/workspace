import json
import boto3
import botocore.exceptions
import logging

log = logging.getLogger(__name__)

ses = boto3.Session()


class Scrapper:

    def __init__(self, session, region="us-east-1"):
        self.session = session
        self.region = region
        self.account_id = self.session.client("sts").get_caller_identity()["Account"]

    def check_kms_usage(self):
        keys = []
        try:
            client = self.session.client("kms", region_name=self.region)
            paginator = client.get_paginator("list_aliases")
            page_iter = paginator.paginate()
            for page in page_iter:
                keys.extend([item["AliasName"] for item in page["Aliases"] if item["AliasName"].split("/")[1] != "aws"])

            return {
                "account_id": self.account_id,
                "resource": "kms",
                "count": len(keys),
                "keys": keys
            }
        except botocore.exceptions.ClientError as e:
            log.error(e)
            return {
                "account_id": self.account_id,
                "resource": "kms",
                "count": 0,
                "keys": []
            }

    def check_kinesis_usage(self):
        streams = []
        client = self.session.client("kinesis", region_name=self.region)
        paginator = client.get_paginator("list_streams")
        page_iter = paginator.paginate()
        for page in page_iter:
            streams.extend(page["StreamNames"])
        return {
                "account_id": self.account_id,
                "resource": "kinesis",
                "count": len(streams),
                "streams": streams
            }

    def check_firehose_usage(self):
        client = self.session.client("firehose", region_name=self.region)
        resp = client.list_delivery_streams()
        return {
                "account_id": self.account_id,
                "resource": "firehose",
                "count": len(resp["DeliveryStreamNames"]),
                "dilivery_streams": resp["DeliveryStreamNames"]
            }


scrapper = Scrapper(ses)

stream = scrapper.check_firehose_usage()
print(stream)
