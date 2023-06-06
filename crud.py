import boto3
from datetime import datetime


class CRUDOperations:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb', region_name='ap-south-1',
                                     aws_access_key_id='AKIAUOI7KOJQV4THC3K7',
                                     aws_secret_access_key='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')

    def add_item(self, item):
        item = {
            'id': {'S': item['id']},
            'title': {'S': item['title']},
            'desc': {'S': item['desc']},
            'timestamp': {'S': str(datetime.now())}
        }
        self.dynamodb.put_item(TableName='CMS-data', Item=item)

    def get_all_items(self):
        response = self.dynamodb.scan(TableName='CMS-data')
        items = response['Items']
        processed_items = []
        for item in items:
            processed_item = {
                'id': item['id']['S'],
                'title': item.get('title', {}).get('S', ''),
                'desc': item.get('desc', {}).get('S', ''),
                'timestamp': item.get('timestamp', {}).get('S', '')
            }
            processed_items.append(processed_item)
        processed_items.sort(key=lambda x: x['timestamp'], reverse=True)
        return processed_items

    def delete_item(self, id):
        self.dynamodb.delete_item(
            TableName='CMS-data',
            Key={
                'id': {'S': id}
            }
        )

    def update_item(self, item):
        item = {
            'id': {'S': item['id']},
            'title': {'S': item['title']},
            'desc': {'S': item['desc']},
            'timestamp': {'S': str(datetime.now())}
        }
        self.dynamodb.put_item(TableName='CMS-data', Item=item)
