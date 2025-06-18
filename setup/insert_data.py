from botocore.exceptions import ClientError
import requests
import json

from aws_cred import AWS

def read_json_file(file_path):
    """
    Reads a JSON file and returns the parsed data.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict or list: The parsed JSON data.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['songs']
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None

def upload_git_img_to_s3(s3_client, file_key, data, contentType='image/jpg'):
    """
    Uploads an image to an S3 bucket from a stream.
    """
    s3_client.upload_fileobj(
        Fileobj=data,
        Bucket=AWS.AWS_S3,
        Key=file_key,
        ExtraArgs={"ContentType": contentType}
    )

def setup_s3():
    """
    Sets up the S3 bucket by creating it if it doesn't exist.
    """
    s3_client = AWS.aws_connect('s3')
    
    try:
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        if any(bucket['Name'] == AWS.AWS_S3 for bucket in buckets):
            print(f"Bucket {AWS.AWS_S3} already exists.")
            return
        s3_client.create_bucket(
            Bucket=AWS.AWS_S3
        )
        print(f"Bucket {AWS.AWS_S3} created successfully.")
    except Exception as e:
        print(f"Error creating bucket {AWS.AWS_S3}: {e}")

def insert_data_to_s3(data):
    s3_client = AWS.aws_connect('s3')
    setup_s3()

    for music_info in data:
        url = music_info.get('img_url', '')
        if not url:
            continue
        
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_key = f'{music_info["artist"].replace(" ", "_")}.jpg'
            upload_git_img_to_s3(s3_client, file_key, response.raw)
        else:
            print(f"Failed to download image from {url}")


def insert_music_batch(music_list):
    dynamodb = AWS.aws_connect("dynamodb")
    
    try:
        # Prepare batch list
        batch = []
        for song in music_list:
            item = {
                'PutRequest': {
                    'Item': {
                        'artist': {'S': song['artist']},
                        'title': {'S': song['title']},
                        'year': {'N': str(song['year'])},
                        'album': {'S': song['album']},
                        'img_url': {'S': f"{song['artist'].replace(' ', '_')}.jpg"}
                    }
                }
            }
            batch.append(item)

            # If batch has 25 items, write and reset
            if len(batch) == 25:
                write_batch(dynamodb, AWS.MUSIC_TABLE, batch)
                batch = []

        # Final leftover
        if batch:
            write_batch(dynamodb, AWS.MUSIC_TABLE, batch)

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading JSON: {e}")
    except ClientError as e:
        print(f"AWS error: {e.response['Error']['Message']}")

def write_batch(dynamodb, table_name, batch):
    """
    Writes a batch of up to 25 items and retries unprocessed items if needed.
    """
    while True:
        response = dynamodb.batch_write_item(RequestItems={table_name: batch})
        unprocessed = response.get("UnprocessedItems", {}).get(table_name, [])
        if not unprocessed:
            print(f"Batch of {len(batch)} inserted successfully.")
            break
        print(f"Retrying {len(unprocessed)} unprocessed items...")
        batch = unprocessed

if __name__ == "__main__":
    data = read_json_file('2025a1.json')

    # insert_data_to_s3(data)
    insert_music_batch(data)
