from flask import Flask
import boto3
from botocore.exceptions import ClientError
from time import sleep

app = Flask(__name__)
dynamodb = boto3.client('dynamodb', region_name='ap-south-1',
                                     aws_access_key_id='AKIAUOI7KOJQV4THC3K7',
                                     aws_secret_access_key='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')
# dynamodb = boto3.resource('dynamodb')

def create_table(table_name):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        return table
    except ClientError as e:
        print(e)
        return None

@app.route('/create-table')
def create_table_route():
    table_name = 'Count'  # Replace with your desired table name
    table = create_table(table_name)
    if table:
        return f'Table {table_name} created successfully'
    else:
        return 'Error creating table'


if __name__ == '__main__':
    app.run(debug=True)
