import os
import pandas as pd
from googleapiclient.discovery import build


def main(video_id):
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


    def get_comment_text(video_id):
        res = get_comment_threads(video_id)
        comments = extract_key_from_json(res, 'textOriginal')
        return '\n'.join(comments)
    
   
    return get_comment_text(video_id)



if __name__ == '__main__':
    main('-wlZY4tfGMY')


