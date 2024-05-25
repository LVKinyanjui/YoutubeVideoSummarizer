import os, time
from tqdm import tqdm
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize(docs, user_instructions=None, chunk_size=30000, chunk_overlap=100, api_call_limit=20, verbose=True):
    
    llm_calls = 0
    while True:

        if llm_calls > api_call_limit:
            break

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        contexts = text_splitter.split_text(docs)

        responses = []
        for context in tqdm(contexts):

            if user_instructions is None:
                user_instructions = f"""
                    I will provide you with text enclosed in triple quote marks (```)
                    Your goal is to summarize but with a key to detail\
                    It is going to be text from online forums \
                    Meaning there may be no coherent narrative but only disjointed information \
                    I would like you to express the diversity of this information as best as you can \
                    The emphasis is on adequately representing different viewpoints, not necessarily brevity \
                    You will inform the user:
                        What the text is about in general
                        The sentiments contained in the text
                        The key points of contention or agreement between conversants
                        Some key words and terminology, if they stand out

                    Here is the text:
                    """

            prompt = f"""
            {user_instructions}

            ```
            {context}
            ```
            """

            model = genai.GenerativeModel('gemini-pro')
            result = model.generate_content(prompt)
            try:
                responses.append(result.text)
            except ValueError:
                # responses.append(result.parts[0])
                print("Prompt response probably blocked")
                pass

            llm_calls += 1
            if verbose:
                print(f"LLM called {llm_calls} times")

            time.sleep(2.5)

        docs = "\n\n".join(responses)

        # Simulates do while loop
        # Critical. If contexts have only one chunk end the inference.
        if len(contexts) <= 1:
            break

    return docs


