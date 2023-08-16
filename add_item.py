import boto3
import random
dynamodb = boto3.client('dynamodb')

from flask import Flask, request

app = Flask(__name__)

dynamodb = boto3.client('dynamodb', region_name='ap-south-1',
                                     aws_access_key_id='AKIAUOI7KOJQV4THC3K7',
                                     aws_secret_access_key='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')
table_name = 'section'




@app.route('/addd', methods=['POST'])
def add_entry():
    data = request.get_json()  # Assuming you're sending JSON data in the request body

    item = {
        'id': {'S': data['id']},  # Assuming 'id' is the value for your primary key
        'section_name': {'S': data['A']},  # Replace 'Attribute1' with your attribute name
        # Add more attributes as needed
    }

    response = dynamodb.put_item(TableName=table_name, Item=item)

    return 'Entry added successfully'
