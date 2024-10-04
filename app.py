import streamlit as st
from youtube_comments import main as get_comments
from custom import extract_video_id
from sum_refine import refine

st.write("## Youtube Comment Summaries 💭")

@st.cache_data
def summarize(comments):
    return refine(comments)

url_input = st.text_input('Enter your youtube url and press ENTER')
summarize = st.button("Summarize")

if "summary" not in st.session_state:
    st.session_state["summary"] = ""

st.markdown(st.session_state.summary)

with st.expander("Raw Comments"):
    if url_input:
        video_id = extract_video_id(url_input)
        comments = get_comments(video_id)

        if summarize:
            st.session_state.summary = summarize(comments)

        comments
