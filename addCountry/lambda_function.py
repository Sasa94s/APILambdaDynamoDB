import os
import json
import boto3
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


TABLE = os.environ.get('TABLE')


def lambda_handler(event, context):
    logger.info('Request', event)
    dynamodb = boto3.resource('dynamodb')
    countries_table = dynamodb.Table(TABLE)

    body = json.loads(event.get('body', '{}'))
    if 'ID' not in body or 'Name' not in body:
        logger.error('Failed to Add Country Item')
        return {
            'statusCode': 400,
            'body': 'Required field(s) missing'
        }

    try:
        country_item = {
            'ID': body['ID'],
            'Name': body['Name']
        }
        countries_table.put_item(Item=country_item)
        logger.info('Added Country Item Successfully', country_item)
    except Exception as e:
        logger.exception(e)
        return {
            'statusCode': 500,
            'body': 'Failed to Add Country Item'
        }

    response = {
        'statusCode': 200,
        'body': json.dumps(country_item),
    }
    logger.info('Response', response)
    return response
