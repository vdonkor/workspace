import os
import boto3
from tenable.sc import TenableSC
import logging
logging.basicConfig(format="%(levelname)s | %(asctime)s | %(message)s")
sc_url = os.getenv('SC_HOST')
s3_bucket = os.getenv('INVENTORY_BUCKET')
sc_secret_name = os.getenv('TENABLE_SECRET')
report_file = "vpc-endpoints.csv"
dns_asset_name = "AWS VPC Endpoints"
sc_access_key = os.getenv('SC_ACCESS_KEY')
sc_secret_key = os.getenv('SC_SECRET_KEY')
# client = boto3.client('secretsmanager')
s3 = boto3.client('s3')
sc = TenableSC(
    host=sc_url,
    access_key=sc_access_key,
    secret_key=sc_secret_key,
    ssl_verify=False
)
def read_csv_file(bucket_name, key):
    logging.info("Reading s3 file")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    lines = response['Body'].read().decode('utf-8').splitlines()
    logging.info(f"Found a total {len(lines)} records")
    return lines
def get_asset_id(asset_name):
    logging.info("Retrieving dns asset id")
    asset_list = sc.asset_lists.list(fields=["name"])
    asset_id = [asset["id"] for asset in asset_list["usable"] if asset.get("name") == asset_name ][0]
    logging.info(f"Asset ID {asset_id} retrieved for {asset_name}")
    return asset_id
def handler(event,context):
    vpce = read_csv_file(s3_bucket,report_file)
    asset_id = get_asset_id(dns_asset_name)
    logging.info("Updating DNS Asset List...")
    dns = sc.asset_lists.edit(id=asset_id,dns_names=vpce)
    logging.info("Asset updated:")
    logging.info(f"{dns}")
white_check_mark
eyes
raised_hands














