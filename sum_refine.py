from langchain.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from langchain_google_genai import ChatGoogleGenerativeAI
import os
google_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=google_api_key)

def refine(text: str, prompt=None, refine_prompt=None) -> str:
    """
        use the refine method to summarize text. More can be learned here: 
            https://python.langchain.com/v0.1/docs/use_cases/summarization/#option-3-refine
    """
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n\n", "\n\n", "\n"], 
                                                #    chunk_size=128, chunk_overlap=0
                                                   )
    split_texts = text_splitter.split_text(text)

    # Convert into langchain docs for downstream chain
    split_docs =  []
    for text in split_texts:
        page = Document(page_content=text,
                        metadata = {"source": "local"})
        split_docs.append(page)

    output_key = "output_text"

    if prompt is None:
        prompt = """
                        Please provide a very comprehensive summary of the following text.
                        WHile maintaining lower level detail
                        
                        TEXT: {text}
                        SUMMARY:
                        """

    question_prompt = PromptTemplate(
        template=prompt, input_variables=["text"]
    )

    if refine_prompt is None:
        refine_prompt = """
                    Write a comprehensive summary of the following text delimited by triple backquotes.
                    Your goal will be to give a high level overview while also expounding on some finer details of the text

                    ```{text}```
                    
                    Have your answer in about 1500 words
                    """


    refine_template = PromptTemplate(
        template=refine_prompt, input_variables=["text"]
    )

    # Load refine chain
    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_template,
        return_intermediate_steps=True,
        input_key="input_documents",
        output_key=output_key,
    )
    result = chain({"input_documents": split_docs}, return_only_outputs=True)
    return result[output_key]

if __name__ == "__main__":
    long_text = """
        And Hector quickly reached for his son. But the boy
        recoiled, crying out to his nurse,
        terrified by his father’s bronze-encased appearance—
        the crest of the horsehair helmet
        shone so bright it frightened him.
        At that, Hector and his wife both burst out laughing,
        and from his head Hector lifted off the helmet,
        and set it on the ground, all shimmering with light.
        Then he kissed his dear son, tossing him in his arms,
        lifting a prayer to Zeus and the other gods:
        'Zeus, and all gods, grant this boy of mine
        to be, like me, preeminent in Troy,
        strong and brave, and ruling Ilium with might.
        Then one day men will say of him,
        as he returns from war, bearing the bloodstained gear of slaughtered foes,
        "A far better man than his father!"'
        And Hector placed his son in his wife's arms,
        and she embraced him, smiling through her tears.
    """

    print(refine(long_text))

