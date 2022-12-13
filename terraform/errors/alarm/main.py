import base64
import gzip
import json
from os import getenv
import logging
from slack import WebClient
from slack.errors import SlackApiError

logger = logging.getLogger(__name__)
slack_url = getenv("SLACK_URL")
channel_id = getenv("SLACK_CHANNEL")
oauth_token = getenv("OAUTH_TOKEN")
log_file = "/tmp/log-events.txt"
client = WebClient(token=oauth_token)


def handler(event, context):
    zipped_log = base64.b64decode(event["awslogs"]["data"])
    unzipped_log = gzip.decompress(zipped_log)
    logs = json.loads(unzipped_log)["logEvents"]

    with open(log_file, "a") as f:
        for log in logs:
            f.writelines(log["message"])

    try:
        result = client.files_upload(
            channels=channel_id,
            initial_comment="Errors processing cloud inventory :beer:",
            file=log_file
        )
        logger.info(result)
    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))
