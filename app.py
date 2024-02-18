# %%
import gradio as gr
from IPython.display import Markdown, display

from youtube_comments import main as get_comments
from summarizer import summarize

# %%
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


# %%
def convert_youtube_url_to_embeddable_iframe(url):
    # Extract video id from URL
    video_id = re.search(r'(?:v=|/)([0-9A-Za-z_-]{10}[048AEIMQUYcgkosw])', url)
    if video_id:
        url = f'https://www.youtube.com/embed/{video_id.group(1)}'

        embed_html = f'<iframe width="863" height="480" src={url} title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        return embed_html
    
    else:
        print("Invalid YouTube URL")
        return None
    
convert_youtube_url_to_embeddable_iframe("https://www.youtube.com/watch/EngW7tLk6R8")

# %%
def get_full_comment_data(url):
    """Avail all youtube comments text for a given video id. Meant to ensure this is exectuted only once"""
    video_id = extract_video_id(url)
    return get_comments(video_id)

# %%
def chatter(query, history, comment_text):
    """Make the summarize function compatible with a gr.ChatInterface element."""

    user_instructions = f"""
        This is a chat conversation between you, the AI and a user \
        You will be be provided with a history of the coversation thus far \
        as follows

        History: {history}

        and the current user query, also as follows,

        User Query: {query}

        Please answer the user query as truthfully as you can.

    """
    return summarize(docs=comment_text, user_instructions=user_instructions)

# %%
def issue_disclaimer():
    return """
    <h2 align="center"> Disclaimer </h2>
    Before using **Summary** or **Chat with Your Videos**, please click Get all Comments. This will ensure there will be content to summarize
    Otherwise Errors will result.
    """

# %%


with gr.Blocks(title="Youtube Video Comment Summarizer") as app:
    with gr.Tab("Upload Video"):
        video_link = gr.Textbox(
            label="Youtube Video URL",
            placeholder="Please input the video URL to summarize "
            )

        video_iframe = gr.HTML()
        disclaimer = gr.Markdown(issue_disclaimer())
        comments = gr.Button("Get all Comments")
        video_comments = gr.Markdown()

        video_link.change(
            fn=convert_youtube_url_to_embeddable_iframe,
            inputs=video_link,
            outputs=video_iframe
            )
        
        comments.click(fn=get_full_comment_data, inputs=video_link, outputs=video_comments)

    with gr.Tab("Summary"):
        video_summary = gr.Markdown(
            label="Video Comment Summary"
        )

        summary = gr.Button("Summarize")
        summary.click(fn=summarize, inputs=video_comments, outputs=video_summary)

    with gr.Tab("Chat with Your Videos"):
        gr.ChatInterface(
            fn=chatter,
            additional_inputs=video_comments
        )


app.launch()

# %%



