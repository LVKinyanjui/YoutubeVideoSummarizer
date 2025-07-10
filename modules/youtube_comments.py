import os
from pathlib import Path
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env if it exists
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

youtube = build("youtube", "v3", developerKey=os.getenv('YOUTUBE_API_KEY'))

def extract_key_from_json(json_data, target_key):
    "Safely extract key values from nested json data"
    result = []

    def search_nested(json_obj, key):
        if isinstance(json_obj, dict):
            for k, v in json_obj.items():
                if k == key:
                    result.append(v)
                elif isinstance(v, (dict, list)):
                    search_nested(v, key)
        elif isinstance(json_obj, list):
            for item in json_obj:
                search_nested(item, key)

    search_nested(json_data, target_key)
    return result


def get_comment_count(video_id):
    
    response = youtube.videos().list(
        part="statistics",
        id=video_id
    ).execute()

    counts = response['items'][0]['statistics']['commentCount']
    
    return int(counts)


def get_comment_threads(video_id):
    
    #Looping over pages
    comments = []
    next_page_token = None
    max_results = get_comment_count(video_id)

    while 1:
        res = youtube.commentThreads().list(part = 'snippet', 
                                            videoId = video_id,
                                            pageToken = next_page_token,
                                            maxResults = max_results
                                        ).execute()
        comments += res['items']
        next_page_token = res.get('nextPageToken')
        
        # If token is none then we have reached the end so break
        if  next_page_token == None:
            break
            
    return comments


def fetch_youtube_comments(video_id):
    res = get_comment_threads(video_id)
    # Extract relevant metadata for each comment
    comments = []
    for item in res:
        snippet = item['snippet']['topLevelComment']['snippet']
        comment = {
            'text': snippet.get('textOriginal', ''),
            'author': snippet.get('authorDisplayName', ''),
            'published_at': snippet.get('publishedAt', ''),
            'profile_image': snippet.get('authorProfileImageUrl', ''),
            'like_count': snippet.get('likeCount', 0)
        }
        comments.append(comment)
    return comments
    


if __name__ == '__main__':
    print(fetch_youtube_comments('-wlZY4tfGMY'))


