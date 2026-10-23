from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

# load_dotenv()
load_dotenv(override=True)

pdf_path = Path(__file__).parent / "spring-boot-reference.pdf"

# Load this file in python program
loader = PyPDFLoader(file_path=pdf_path)

document = loader.load()

# Split the text into Smaller chunks 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents=document)

# print(chunks[15])

# Vector Embedding
embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name = "learning_rag_SpringBoot",# Mern
    batch_size=10
    
)
print("Indexing of document is Done....")
