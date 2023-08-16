import boto3
import random
from datetime import datetime, date


class CRUDOperations:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb', region_name='ap-south-1',
                                     aws_access_key_id='AKIAUOI7KOJQV4THC3K7',
                                     aws_secret_access_key='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')
        self.s3 = boto3.client('s3', region_name='ap-south-1',
                               aws_access_key_id='AKIAUOI7KOJQV4THC3K7',
                               aws_secret_access_key='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')
        self.bucket_name = 'cms-multimedia'
        self.table_name = None

    def add_item(self, item):
        if self.table_name is None:
            raise ValueError("Table name is not set.")


        response = self.dynamodb.put_item(TableName=self.table_name, Item=item)
        return response

    def get_all_items(self, table_name):  # Add the table_name parameter
        response = self.dynamodb.scan(TableName=table_name)
        items = response['Items']
        processed_items = []
        for item in items:
            processed_item = {}
            for key, value in item.items():
                attr_name = key
                attr_type = list(value.keys())[0]
                attr_value = value[attr_type]
                processed_item[attr_name] = attr_value

            processed_items.append(processed_item)
        return processed_items

    def delete_all_items(self):
        if self.table_name is None:
            raise ValueError("Table name is not set.")

        items = self.get_all_items(self.table_name)
        for item in items:
            item_id = item.get('id')
            if item_id:
                self.delete_item(item_id)

    #
    def delete_item(self, id):
        self.dynamodb.delete_item(
            TableName=self.table_name,
            Key={
                'id': {'N': id}
            }
        )

    def delete_itemm(self, id):
        self.dynamodb.delete_item(
            TableName=self.table_name,
            Key={
                'id': {'S': id}
            }
        )

    # def delete_table(self, table_name):
    #     try:
    #         self.dynamodb.delete_table(TableName=table_name)
    #         print("Table deleted successfully:", table_name)
    #     except Exception as e:
    #         print("Error deleting table:", str(e))
    def upload_image_to_s3(self, file_stream, filename):
        # Generate random letters
        random_letters = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))

        # Get current date
        current_date = date.today().strftime('%d%m%Y')

        # Combine random letters and current date to create the unique ID
        unique_id = f"{random_letters}{current_date}"

        # Create the unique filename with the generated ID
        unique_filename = f"{unique_id}_{filename}"

        # Upload the image to S3 with the unique filename
        try:
            self.s3.upload_fileobj(file_stream, self.bucket_name, unique_filename)
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return None

        # Generate the URL for the uploaded image
        image_url = f"https://{self.bucket_name}.s3.amazonaws.com/{unique_filename}"
        print("Image URL:", image_url)

        # Return the image URL
        return image_url

    #
    # def update_item(self, item):
    #     item = {
    #         'id': {'S': item['id']},
    #         'title': {'S': item['title']},
    #         'desc': {'S': item['desc']},
    #         # 'image_url': {'S': f"https://cms-multimedia.s3.amazonaws.com/s3_images/{item['image_filename']}"},
    #         'timestamp': {'S': str(datetime.now())}
    #     }
    #     self.dynamodb.put_item(TableName=self.table_name, Item=item)
    #
    # def upload_image_to_s3(self, file_stream, filename):
    #     # Generate random letters
    #     random_letters = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))
    #
    #     # Get current date
    #     current_date = date.today().strftime('%d%m%Y')
    #
    #     # Combine random letters and current date to create the unique ID
    #     unique_id = f"{random_letters}{current_date}"
    #
    #     # Create the unique filename with the generated ID
    #     unique_filename = f"{unique_id}_{filename}"
    #
    #     # Upload the image to S3 with the unique filename
    #     try:
    #         self.s3.upload_fileobj(file_stream, self.bucket_name, unique_filename)
    #     except Exception as e:
    #         print(f"Error uploading file to S3: {e}")
    #         return
    #
    #     # Generate the URL for the uploaded image
    #     image_url = f"https://{self.bucket_name}.s3.amazonaws.com/{unique_filename}"
    #     print("Image URL:", image_url)
    #
    #     # Return the image URL
    #     return image_url
    #
    # def store_uploaded_image_url(self, item_id, image_url):
    #     response = self.dynamodb.update_item(
    #         TableName=self.table_name,
    #         Key={'id': {'S': item_id}},
    #         UpdateExpression='SET image_url = :url',
    #         ExpressionAttributeValues={':url': {'S': image_url}}
    #     )
    #     print("DynamoDB update response:", response)

        # return response


