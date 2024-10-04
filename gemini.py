import google.generativeai as genai
import os

api_key = os.getenv("GOOGLE_API_KEY")
# print(api_key)
genai.configure(api_key=api_key)

def call_llm(query):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)
    return response.text

if __name__ == '__main__':
    print(call_llm("The opposite of hot is"))