import streamlit as st
from youtube_comments import main as get_comments
from custom import extract_video_id

st.write("## Youtube Comment Extractor")

url_input = st.text_input('Enter your youtube url and press ENTER')

if url_input:
    video_id = extract_video_id(url_input)
    st.session_state.comments = get_comments(video_id)
    st.write(st.session_state.comments) 