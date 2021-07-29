import json
import boto3

def lambda_handler(event, context):
    bits = (event['bits'])

    number_x = bits[0:7]
    print(number_x)
    number_y = bits[7:14]
    print(number_y)


    x = int(number_x, 2)
    y = int(number_y, 2)


    response = put_data(x, y)

    return {
        'statusCode': response,
        'x': x,
        'y': y
    }

def put_data(x, y, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

    table = dynamodb.Table('DataPointsStorage')
    response = table.put_item(
       Item={
            'x': x,
            'y': y
        }
    )
    return response