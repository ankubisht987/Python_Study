from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv(override=True)



openai_create = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url='https://openrouter.ai/api/v1'
)


embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name = "learning_rag_SpringBoot", # MERN 
    embedding=embedding_model,
)

def process_query(query : str):
    print("Searching Chunks ", query)
    # Return revelent chunks from the VB
    search_results = vector_db.similarity_search(query=query)
    
    # print(f"\nRetrieved {len(search_results)} chunks for: {query}")
    
    # for i, result in enumerate(search_results, start=1):
    #     print(f"\n--- Chunk {i} ---")
    #     print("Source:", result.metadata.get("source", "Unknown"))
    #     print("Page:", result.metadata.get("page_label", "Unknown"))
    #     print("Content:", result.page_content[:500])
        
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
    for result in search_results])
    
    SYSTEM_PROMPT= f""" 
    You are a helpful AI Assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page_number.
    
    You should only answer the user based on the following context and navigate the user to open the right page number to know more.
    
    Context:
    {context}
    """
    
    response = openai_create.chat.completions.create(
            # model='openrouter/free',  # CHANGED (formatting only): was `model= 'openrouter/free'`
            model="nvidia/nemotron-3.5-super-vl:free",
            extra_body={
                "models": [
                    "recursive/flint-v1.0:free",
                    "minimax/minimax-m3.1-flash:free",
                ]
            },
            messages=[
                {"role":"system", "content":SYSTEM_PROMPT},
                {"role":"user", "content":query}
            ]
        )
    
    print(f"🤖:{response.choices[0].message.content}")
    return response.choices[0].message.content