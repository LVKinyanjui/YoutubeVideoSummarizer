import re

def extract_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube url. This function supports the following patterns:
    - https://youtube.com/watch?v={video_id}
    - https://youtube.com/embed/{video_id}
    - https://youtu.be/{video_id}
    :param str url: A YouTube url containing a video id.
    :return: The video id as a string.
    """
    # Regular expression pattern to match YouTube video IDs
    pattern = re.compile(r"(?:(?:youtube\.com\/(?:watch\?v=|embed\/))|(?:youtu\.be\/))([\w\-]+)")
    match = pattern.search(url)
    if match:
        return match.group(1)
    else:
        print("Error: Invalid YouTube video link.")
        return ""
