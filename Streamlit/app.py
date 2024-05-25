import streamlit as st
from youtube_comments import main as get_comments
from custom import extract_video_id

if 'comments' not in st.session_state:
    st.session_state['youtube_url'] = None
    st.session_state['comments'] = None

url_input = st.text_input('Youtube Video URL', placeholder='Please input the video URL to summarize ', key='video_link')
button = st.button('Get Comments')

if button:
    video_id = extract_video_id(url_input)
    st.session_state.comments = get_comments(video_id)
    st.write(st.session_state.comments)