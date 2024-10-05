import streamlit as st
from modules.youtube_comments import main as get_comments
from modules.custom import extract_video_id
from modules.sum_refine import refine

st.write("## Youtube Comment Summaries 💭")

@st.cache_data
def summarize(comments):
    return refine(comments)

@st.cache_data
def extract_comments(url):
    video_id = extract_video_id(url)
    return get_comments(video_id)

url_input = st.text_input('Enter your youtube url and press ENTER')
summary_button = st.button("Summarize")

if "summary" not in st.session_state:
    st.session_state["summary"] = ""

st.markdown(st.session_state.summary)

with st.expander("Raw Comments"):
    if url_input:
        comments = extract_comments(url_input)

        if summary_button:
            st.session_state.summary = summarize(comments)

        st.markdown(comments)
