import base64
import gzip
import json
from os import getenv
import urllib3
import logging

log = logging.getLogger(__name__)
http = urllib3.PoolManager()
slack_url = getenv("SLACK_URL")
channel_id = getenv("SLACK_CHANNEL")
oauth_token = getenv("OAUTH_TOKEN")


def handler(event, context):
    zipped_log = base64.b64decode(event['awslogs']['data'])
    unzipped_log = gzip.decompress(zipped_log)
    logs = json.loads(unzipped_log)["logEvents"]
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "channels": channel_id,
        "filename": "error.log",
        "content": logs,
        "token": oauth_token,
        "title": "Cloud Inventory Error Logs",
        "filetype": "text",
    }

    try:
        log.info(f'Sending message')
        resp = http.request("POST", url=slack_url, headers=headers, data=payload)
        if resp.status != 200:
            log.error(f"Failed to deliver error {resp.status}")
    except urllib3.exceptions.HTTPError as e:
        log.error(e)
