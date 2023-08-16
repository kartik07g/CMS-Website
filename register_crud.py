import boto3
import random
from datetime import datetime, date


class regist_operations:
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
                'id': item['id']['S'],
                'title': item.get('title', {}).get('S', ''),
                'desc': item.get('desc', {}).get('S', ''),
                'image_url': item.get('image_url', {}).get('S', ''),  # Add the image URL column
                # 'timestamp': item.get('timestamp', {}).get('S', str(datetime.now()))
            }
            processed_items.append(processed_item)
            print("Image URL:", item.get('image_url', {}).get('S', ''))
        # processed_items.sort(key=lambda x: x['timestamp'], reverse=True)
        return processed_items