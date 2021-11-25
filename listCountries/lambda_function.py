import os
import json
from boto3.dynamodb.types import Decimal
import boto3
from logger import get_logger

logger = get_logger()
TABLE = os.environ['TABLE']


def to_serializable(val):
    if isinstance(val, Decimal):
        return str(val)
    return val


def lambda_handler(event, context):
    logger.info('Request', event)
    dynamodb = boto3.resource('dynamodb')
    countries_table = dynamodb.Table(TABLE)
    query_params = event.get('queryStringParameters', {})
    query_params = query_params if query_params else {}
    limit = query_params.get('limit', 10)

    try:
        items = countries_table.scan(Limit=limit)['Items']

    except Exception as e:
        logger.exception(e)
        return {
            'statusCode': 500,
            'body': 'Failed to List Countries'
        }

    response = {
        'statusCode': 200,
        'body': json.dumps(items, default=to_serializable)
    }
    logger.info('Response', response)
    return response
