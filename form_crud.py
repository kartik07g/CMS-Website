import boto3
import random
from datetime import datetime, date


class form_crud:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb', region_name='ap-south-1',
                                     aws_access_key_id='AKIAUOI7KOJQV4THC3K7',
                                     aws_secret_access_key='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')
        self.s3 = boto3.client('s3', region_name='ap-south-1',
                               aws_access_key_id='AKIAUOI7KOJQV4THC3K7',
                               aws_secret_access_key='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')
        self.table_name = 'registration-data'

    def add_item(self, item):
        # item['timestamp'] = str(datetime.now())

        response = self.dynamodb.put_item(TableName=self.table_name, Item=item)
        return response

    def get_all_items(self):
        response = self.dynamodb.scan(TableName=self.table_name)
        items = response['Items']
        processed_items = []
        for item in items:
            processed_item = {
                'Section_name': item['Section_name']['S'],

            }
            processed_items.append(processed_item)
        return processed_items