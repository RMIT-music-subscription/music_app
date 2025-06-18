import json
import base64
import datetime
from boto3.dynamodb.conditions import Key, Attr
from typing import Optional, List, Dict, Any

from aws_cred import AWS
dynamodb = AWS.aws_connect('dynamodb', resource=True)
table = dynamodb.Table("music")
s3_client = AWS.aws_connect('s3')

# import boto3

def query_music(
    title: Optional[str] = None,
    album: Optional[str] = None,
    artist: Optional[str] = None,
    year: Optional[int] = None,
    table_name: str = 'music'
) -> List[Dict[str, Any]]:
    """
    Query music table with any combination of attributes.
    Uses the most efficient access pattern based on provided parameters.
    
    Schema:
    - Main table: title (PK), album (SK)
    - ArtistIndex: artist (PK)
    - TitleIndex: title (PK)
    - AlbumIndex: album (PK)
    - YearIndex: year (PK)
    
    Args:
        title: Song title
        album: Album name
        artist: Artist name
        year: Release year
        table_name: DynamoDB table name
    
    Returns:
        List of matching items
    """
    
    # Type validation and conversion
    if year is not None:
        try:
            year = int(year)  # Ensure year is an integer
        except (ValueError, TypeError):
            print(f"Error: Invalid year value '{year}'. Year must be a number.")
            return []
    
    try:
        # Strategy 1: Main table query (most efficient for exact title+album match)
        if title and album:
            print(f"Querying main table with title: {title}, album: {album}, artist: {artist}, year: {year}")
            return _query_main_table(table, title, album, artist, year)
        
        # Strategy 2: Single attribute GSI queries (most efficient for single attribute)
        elif artist and not any([title, album, year]):
            return _query_artist_index(table, artist)
        elif title and not any([album, artist, year]):
            return _query_title_index(table, title)
        elif album and not any([title, artist, year]):
            return _query_album_index(table, album)
        elif year and not any([title, album, artist]):
            return _query_year_index(table, year)
        
        # Strategy 3: GSI query with filters (when one attribute is primary, others are filters)
        elif artist:
            return _query_artist_index_with_filters(table, artist, title, album, year)
        elif title:
            return _query_title_index_with_filters(table, title, album, artist, year)
        elif album:
            return _query_album_index_with_filters(table, album, title, artist, year)
        elif year:
            return _query_year_index_with_filters(table, year, title, album, artist)
        
        # Strategy 4: Full table scan (least efficient - when no attributes provided)
        else:
            print("Warning: No query parameters provided. Returning empty list to avoid full table scan.")
            return []
            
    except Exception as e:
        print(f"Error querying music table: {str(e)}")
        return []

def _query_main_table(table, title: str, album: str, artist: Optional[str], year: Optional[int]) -> List[Dict]:
    """Query main table using title (PK) and album (SK)"""
    key_condition = Key('title').eq(title) & Key('album').eq(album)
    filter_expr = _build_filter_expression(artist=artist, year=year)
    print(f"KeyCondition: {key_condition}, FilterExpression: {filter_expr}")
    if filter_expr:
        response = table.query(
            KeyConditionExpression=key_condition,
            FilterExpression=filter_expr
        )
    else:
        response = table.query(KeyConditionExpression=key_condition)
    
    return response.get('Items', [])

def _query_artist_index(table, artist: str) -> List[Dict]:
    """Query ArtistIndex using artist (PK) only"""
    key_condition = Key('artist').eq(artist)
    
    response = table.query(
        IndexName='ArtistIndex',
        KeyConditionExpression=key_condition
    )
    return response.get('Items', [])

def _query_artist_index_with_filters(table, artist: str, title: Optional[str], 
                                   album: Optional[str], year: Optional[int]) -> List[Dict]:
    """Query ArtistIndex with additional filters"""
    key_condition = Key('artist').eq(artist)
    filter_expr = _build_filter_expression(title=title, album=album, year=year)
    
    if filter_expr:
        response = table.query(
            IndexName='ArtistIndex',
            KeyConditionExpression=key_condition,
            FilterExpression=filter_expr
        )
    else:
        response = table.query(
            IndexName='ArtistIndex',
            KeyConditionExpression=key_condition
        )
    
    return response.get('Items', [])

def _query_title_index(table, title: str) -> List[Dict]:
    """Query TitleIndex using title (PK) only"""
    key_condition = Key('title').eq(title)
    
    response = table.query(
        IndexName='TitleIndex',
        KeyConditionExpression=key_condition
    )
    return response.get('Items', [])

def _query_title_index_with_filters(table, title: str, album: Optional[str], 
                                  artist: Optional[str], year: Optional[int]) -> List[Dict]:
    """Query TitleIndex with additional filters"""
    key_condition = Key('title').eq(title)
    filter_expr = _build_filter_expression(album=album, artist=artist, year=year)
    
    if filter_expr:
        response = table.query(
            IndexName='TitleIndex',
            KeyConditionExpression=key_condition,
            FilterExpression=filter_expr
        )
    else:
        response = table.query(
            IndexName='TitleIndex',
            KeyConditionExpression=key_condition
        )
    
    return response.get('Items', [])

def _query_album_index(table, album: str) -> List[Dict]:
    """Query AlbumIndex using album (PK) only"""
    key_condition = Key('album').eq(album)
    
    response = table.query(
        IndexName='AlbumIndex',
        KeyConditionExpression=key_condition
    )
    return response.get('Items', [])

def _query_album_index_with_filters(table, album: str, title: Optional[str], 
                                  artist: Optional[str], year: Optional[int]) -> List[Dict]:
    """Query AlbumIndex with additional filters"""
    key_condition = Key('album').eq(album)
    filter_expr = _build_filter_expression(title=title, artist=artist, year=year)
    
    if filter_expr:
        response = table.query(
            IndexName='AlbumIndex',
            KeyConditionExpression=key_condition,
            FilterExpression=filter_expr
        )
    else:
        response = table.query(
            IndexName='AlbumIndex',
            KeyConditionExpression=key_condition
        )
    
    return response.get('Items', [])

def _query_year_index(table, year: int) -> List[Dict]:
    """Query YearIndex using year (PK) only"""
    try:
        year_int = int(year)
        key_condition = Key('year').eq(year_int)
        
        response = table.query(
            IndexName='YearIndex',
            KeyConditionExpression=key_condition
        )
        return response.get('Items', [])
    except (ValueError, TypeError):
        print(f"Error: Invalid year value '{year}'. Year must be a number.")
        return []

def _query_year_index_with_filters(table, year: int, title: Optional[str], 
                                 album: Optional[str], artist: Optional[str]) -> List[Dict]:
    """Query YearIndex with additional filters"""
    try:
        year_int = int(year)
        key_condition = Key('year').eq(year_int)
        filter_expr = _build_filter_expression(title=title, album=album, artist=artist)
        
        if filter_expr:
            response = table.query(
                IndexName='YearIndex',
                KeyConditionExpression=key_condition,
                FilterExpression=filter_expr
            )
        else:
            response = table.query(
                IndexName='YearIndex',
                KeyConditionExpression=key_condition
            )
        
        return response.get('Items', [])
    except (ValueError, TypeError):
        print(f"Error: Invalid year value '{year}'. Year must be a number.")
        return []

def _build_filter_expression(title: Optional[str] = None, album: Optional[str] = None, 
                           artist: Optional[str] = None, year: Optional[int] = None):
    """Build filter expression from provided attributes with proper type handling"""
    filters = []
    
    if title:
        filters.append(Attr('title').eq(title))
    if album:
        filters.append(Attr('album').eq(album))
    if artist:
        filters.append(Attr('artist').eq(artist))
    if year is not None:  # Changed from 'if year:' to handle year=0
        try:
            year_int = int(year)
            filters.append(Attr('year').eq(year_int))
        except (ValueError, TypeError):
            print(f"Warning: Invalid year value '{year}' ignored in filter")
    
    if not filters:
        return None
    
    # Combine all filters with AND
    filter_expr = filters[0]
    for f in filters[1:]:
        filter_expr = filter_expr & f
    
    return filter_expr

def generate_presigned_url(item, bucket="music-rmit-asv", expiration=3600):
    
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': item.get('img_url', '')
            },
            ExpiresIn=expiration
        )
        item['img_url'] = url  # Update item with the presigned URL
        return item
    except Exception as e:
        return f"Error generating URL: {str(e)}"
       
def lambda_handler(event, context):
    try:
        token = event.get("token")
        if not token:
            raise Exception("Token is required", 400)

        # result = verify_token(token)
        # if not result["valid"]:
        #     raise Exception(result["error"], 401)

        filter = event.get("filter", {})
        if not isinstance(filter, dict):
            raise Exception("Filter must be a dictionary", 400)

        filtered = query_music(filter.get("title",None),
                               filter.get("album",None),
                               filter.get("artist",None),
                               filter.get("year",None))
        filtered = [ generate_presigned_url(item) for item in filtered]
        print(f"Filtered results: {filtered}")
        return {
            "statusCode": 200,
            "body": filtered
        }

    except Exception as e:
        print(f"Error: {e}")
        print(f"Error querying music table: {str(e)}")
        return {
            "statusCode": e.args[1] if len(e.args) > 1 else 500,
            "body": {"error": str(e.args[0] if len(e.args) > 0 else 'Internal error. Try again')}
        }

lambda_handler({
    "token": "eyJlbWFpbCI6ICJhc3dpbkt1bWFyQGdtYWlsLmNvbSIsICJ1c2VybmFtZSI6ICJhc3dpbkt1bWFyIiwgImV4cCI6ICIyMDI1LTA2LTIwVDAxOjQwOjU3LjUyNzI2MCJ9",
    "filter": {
        "artist": "The White Stripes",
    }
}, None)  # Example usage for testing purposes