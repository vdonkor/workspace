"""
This module implements lambda functions that processes Athena data through Api requests.
"""

import boto3
import json
import time
import datetime
import os

session = boto3.Session()
client = session.client("athena")
s3 = session.resource("s3")

s3_bucket = os.getenv("S3_BUCKET")
athena_database_name = os.getenv("ATHENA_DATABASE_NAME")
athena_table_name = os.getenv("ATHENA_TABLE_NAME")
athena_query_log_bucket = os.getenv("ATHENA_QUERY_LOG_BUCKET")
# get previous date

previous_date = datetime.datetime.today() - datetime.timedelta(days=1)
# s3 key prefix since files are stored in days
key_prefix = '{:04d}'.format(previous_date.year) + "/" + '{:02d}'.format(previous_date.month) + "/" + '{:02d}'.format(
    previous_date.day)

query = 'select * from example'


# update list of blocked in key in s3
def write_csv_file(file_name, data: list):
    pass


# upload file to s3
def upload_s3_file(bucket_name, key, file_name):
    s3.meta.client.upload_file(file_name, bucket_name, key)
    if os.path.exists(file_name):
        os.remove(file_name)


def get_row_value(col):
    """
    Mini function to help with data extraction from Athena.
    :param col: row data from
    :return:
    """
    result = []
    for record in col['Data']:
        if not record:
            continue
        result.append(record['VarCharValue'])
    return result


def check_request_status(execution_id, wait_time):
    """
    This function checks the job status of Athena. It takes execution id return from get_execution_id.
    :param execution_id: executionId from get_execution_id function
    :param wait_time: Time in seconds to wait for athena to process the job.
    :return: SUCCEEDED or None
    """
    wait_time = wait_time
    while wait_time > 0:
        wait_time = wait_time - 0.1
        response = client.get_query_execution(QueryExecutionId=execution_id)
        status = response['QueryExecution']['Status']['State']
        if status == "SUCCEEDED":
            return status
        elif status == "FAILED" or status == "CANCELLED":
            return None
        else:
            time.sleep(0.1)


def get_query_data(header, execution_id, max_result_per_page=None, next_token=None, skip_rows=1):
    """
    This function is responsible for extracting data from Athena json response. A little tricky here since
    we need to take into consideration if the request is the first time or subsequent requests
    :param header: column headers specified by fields variable above
    :param execution_id: executionId from get_execution_id function
    :param max_result_per_page: specified number of rows desired. Note athena supports max of 1000
    :param next_token: value of nextToke return from this function. If the page_size is greater than actual rows then
    the value is None.
    :param skip_rows: This value is either 1 or 0. It helps to determine where to start our data extraction, skip_rows
    is always 1 for the first request and 0 for the subsequent requests
    :return: extracted data and nextToken
    """
    if next_token:
        query_result = client.get_query_results(QueryExecutionId=execution_id, MaxResults=max_result_per_page,
                                                NextToken=next_token)
    else:
        query_result = client.get_query_results(QueryExecutionId=execution_id, MaxResults=max_result_per_page)
    try:
        next_token = query_result['NextToken']
    except KeyError:
        next_token = None
    if len(query_result['ResultSet']['Rows']) > 1:
        rows = query_result['ResultSet']['Rows'][skip_rows:]
        query_result = [dict(zip(header, get_row_value(row))) for row in rows]
        return query_result, next_token
    else:
        return [], next_token


def process_athena_data():
    """
    This function when called, will check querystring parameter from Api gateway for nextToken and executionId.
    If nextToken is not None, it means there is more data to be retrieved, and it will call athena again.
    :param event: This is a lambda event parameter as result of the lambda invocation
    :return: returns json body including http header and status code
    """
    # columns header for queries.
    fields = ("dns_name,account_id")

    if 'nextToken' in event["queryStringParameters"].keys():
        next_token = event["queryStringParameters"]["nextToken"]
        execution_id = event["queryStringParameters"]["executionId"]
        # nextToken could be None
        if next_token:
            usage, next_id = get_query_data(header=fields, execution_id=execution_id,
                                            max_result_per_page=int(event["queryStringParameters"]['page_size']),
                                            next_token=next_token, skip_rows=0)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(
                    {
                        "nextToken": next_id,
                        "executionId": execution_id,
                        "usage": usage
                    },
                    default=str
                )
            }

    query_id = get_execution_id()

    if check_request_status(execution_id=query_id, wait_time=20):
        data, next_id = get_query_data(header=fields, execution_id=query_id,
                                       max_result_per_page=1000)
        return data,next_id


def get_execution_id():
    # get the entire Athena query parameters
    params = {
        "region": "us-east-1",
        "database": athena_database_name,
        "bucket": athena_query_log_bucket,
        "path": "inventory-query-results",
        "query": query
    }
    # call athena api using boto client
    response = client.start_query_execution(
        QueryString=params["query"],
        QueryExecutionContext={'Database': params['database']},
        ResultConfiguration={'OutputLocation': f"""s3://{params['bucket']}/{params['path']}/"""}
    )
    # first api call does not return data but id of the athena job
    return response['QueryExecutionId']


def handler(event, context):
    """
    This is the lambda function that call our main function process_athena_data
    :param event: carries input or request parameters
    :param context: provides information about the invocation,function adn execution environment
    :return: return data
    """
    return process_athena_data(event)
