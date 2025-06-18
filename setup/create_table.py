from aws_cred import AWS

def get_table_names(client):
    """
    Get the names of all DynamoDB tables in the AWS account.
    
    :param client: Boto3 DynamoDB client
    :return: List of table names
    """
    try:
        response = client.list_tables()
        return response.get('TableNames', [])
    except Exception as e:
        print(f"Error retrieving table names: {e}")
        return []

def create_login_table(client):
    """
    Create the login table in DynamoDB.
    
    :param client: Boto3 DynamoDB client
    """
    try:
        client.create_table(
            TableName=AWS.LOGIN_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'emailAddress',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'emailAddress',
                    'AttributeType': 'S'  # String type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {AWS.LOGIN_TABLE} created successfully.")
    except Exception as e:
        print(f"Error creating table {AWS.LOGIN_TABLE}: {e}")

def create_music_table(client):
    """
    Create the music table in DynamoDB.
    
    :param client: Boto3 DynamoDB client
    """
    try:
        client.create_table(
            TableName=AWS.MUSIC_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'title',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'album',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'  # String type
                },
                {
                    'AttributeName': 'artist',
                    'AttributeType': 'S'  # String type
                },
                {
                    'AttributeName': 'album',
                    'AttributeType': 'S'  # String type
                },
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N'  # String type
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'ArtistIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'artist',
                            'KeyType': 'HASH'  # Partition key
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'TitleIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'title',
                            'KeyType': 'HASH'  # Partition key
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'AlbumIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'album',
                            'KeyType': 'HASH'  # Partition key
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'YearIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'year',
                            'KeyType': 'HASH'  # Partition key
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {AWS.MUSIC_TABLE} created successfully.")
    except Exception as e:
        print(f"Error creating table {AWS.MUSIC_TABLE}: {e}")

def create_subscribe_table(client):
    """
    Create the subscribe table in DynamoDB.
    
    :param client: Boto3 DynamoDB client
    """
    try:
        client.create_table(
            TableName=AWS.SUBSCRIBE_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'emailAddress',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'title#album',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'emailAddress',
                    'AttributeType': 'S'  # String type
                },
                {
                    'AttributeName': 'title#album',
                    'AttributeType': 'S'  # String type
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'userIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'emailAddress',
                            'KeyType': 'HASH'  # Partition key
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        print(f"Table {AWS.SUBSCRIBE_TABLE} created successfully.")
    except Exception as e:
        print(f"Error creating table {AWS.SUBSCRIBE_TABLE}: {e}")

if __name__ == "__main__":
    client = AWS.aws_connect('dynamodb')
    table_names = get_table_names(client)
    print("DynamoDB Tables:")

    create_table_names = {
        AWS.LOGIN_TABLE:create_login_table,
        AWS.MUSIC_TABLE:create_music_table,
        AWS.SUBSCRIBE_TABLE:create_subscribe_table
        }
    
    for table_name, create_function in create_table_names.items():
        if table_name not in table_names:
            create_function(client)