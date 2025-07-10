import streamlit as st
from modules.youtube_comments import fetch_youtube_comments as get_comments
from modules.custom import extract_video_id

st.set_page_config(
    page_title="YouTube Video Comment Explorer",
    page_icon="💬",
    layout="centered"
)

st.title("YouTube Video Comment Explorer")
st.markdown("""
#### Instantly get all comments from a video without the need for infinite scrolling.
""")

if "comments" not in st.session_state:
    st.session_state["comments"] = list()
if "summary" not in st.session_state:
    st.session_state["summary"] = ""

@st.cache_data
def extract_comments(url):
    video_id = extract_video_id(url)
    return get_comments(video_id)


url_input = st.text_input('Enter your youtube url and press ENTER')


with st.expander("Raw Comments"):
    if url_input:
        st.session_state.comments = extract_comments(url_input)

        for comment in st.session_state.comments:
            with st.container():
                col1, col2 = st.columns([1, 12])
                with col1:
                    if comment['profile_image']:
                        st.image(comment['profile_image'], width=40)
                with col2:
                    st.markdown(f"**{comment['author']}**  ")
                    st.markdown(f"<span style='color:gray;font-size:12px'>{comment['published_at'][:10]}</span>", unsafe_allow_html=True)
                    st.markdown(f"{comment['text']}")
                    if comment['like_count']:
                        st.markdown(f"<span style='color:#888;font-size:11px'>👍 {comment['like_count']}</span>", unsafe_allow_html=True)
                st.markdown("---")

