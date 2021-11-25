import os
import json
from boto3.dynamodb.types import Decimal
import boto3
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

TABLE = os.environ.get('TABLE')


def to_serializable(val):
    if isinstance(val, Decimal):
        return str(val)
    return val


def lambda_handler(event, context):
    print('Request', event)
    dynamodb = boto3.resource('dynamodb')
    countries_table = dynamodb.Table(TABLE)

    try:
        path_params = event.get('pathParameters', {})
        path_params = path_params if path_params else {}
        country_id = path_params.get('id', 1)

        item = countries_table.get_item(
            Key={
                'ID': Decimal(str(country_id))
            }
        )['Item']
    except Exception as e:
        logger.exception(e)
        return {
            'statusCode': 500,
            'body': 'Failed to List Countries'
        }

    response = {
        'statusCode': 200,
        'body': json.dumps(item, default=to_serializable)
    }
    print('Response', response)
    return response
