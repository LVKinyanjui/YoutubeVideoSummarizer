import streamlit as st
from modules.youtube_comments import main as get_comments
from modules.custom import extract_video_id
# from modules.sum_refine import refine
from modules.clustering import show_text_clusters

st.write("## Youtube Comment Summaries 💭")

st.write("""
### TODO
- Better comment space separation
- Display commenter's username alongside comment
""")

if "comments" not in st.session_state:
    st.session_state["comments"] = list()
if "summary" not in st.session_state:
    st.session_state["summary"] = ""

# @st.cache_data
# def summarize(comments):
#     if len(comments) == 0:
#         st.warning("Press ENTER to get comments before attempting to summarize")
#         return ""
#     comments = "\n\n".join(comments)
#     st.session_state.summary = refine(comments)

@st.cache_data
def extract_comments(url):
    video_id = extract_video_id(url)
    return get_comments(video_id)

@st.cache_data
def visualize_comments(comments):
    return show_text_clusters(comments)

url_input = st.text_input('Enter your youtube url and press ENTER')

# if st.button("Summarize"):
#     summarize(st.session_state.comments)
#     st.markdown(st.session_state.summary)

with st.expander("Raw Comments"):
    if url_input:
        st.session_state.comments = extract_comments(url_input)

        # if summary_button:
        #     st.session_state.summary = summarize(comments)

        text = "\n\n".join(st.session_state.comments)
        st.markdown(text)

        # if st.session_state.comments != "":
        #     if st.button("Visualize Comments"):

with st.expander("Plots"):
    if len(st.session_state.comments) > 0:
        if st.button("Visualize"):
            fig = visualize_comments(st.session_state.comments)
            st.pyplot(fig)
