import google.generativeai as genai

import os
api_key = os.getenv("GOOGLE_API_KEY")

if api_key is None:
    raise ValueError("No Google API found as environment variabl")

genai.configure(api_key=api_key)

def get_embeddings(texts: str | list[str]):
    if isinstance(texts, str):
        texts = [texts,]

    result = genai.embed_content(
        content=texts,
        model="models/text-embedding-004")

    # for embedding in result['embedding']:
    #     print(str(embedding)[:50], '... TRIMMED]')

    return result['embedding']