import json
import os
import urllib3
import time
import logging

slack_url = os.getenv("SLACK_URL")
slack_channel = os.getenv("SLACK_CHANNEL")
epoch = time.ctime()
http = urllib3.PoolManager()
log = logging.getLogger(__name__)
slack_colors = {
    "ALARM": "#E01E5A",
}


def handler(event, context):
    log.info(f'Received event{event}')
    url = slack_url
    message = event['Records'][0]['Sns']['Message']
    message = json.loads(message)
    alarm_type = message['NewStateValue']
    alarm_name = message['AlarmName']
    # msg = "ok"
    msg = {
        "channel": slack_channel,
        "icon_emoji": ":alert:",
        "attachments": [
            {
                "fallback": "Errors from Cloud Inventory Scrapper",
                "color": slack_colors[alarm_type],
                "author_name": "@GDIT",
                "title": "Errors Processing Cloud Inventory",
                "text": f'''{alarm_name} has changed state to {alarm_type}''',
                "mrkdwn_in": ["footer", "title"],
                "footer": "GDIT CloudOps",
                "ts": epoch
            }
        ]
    }

    msg = json.dumps(msg).encode('utf-8')
    try:
        log.info(f'Sending message {msg}')
        http.request('POST', url, body=msg)
    except urllib3.exceptions.HTTPError as e:
        log.error(e)
