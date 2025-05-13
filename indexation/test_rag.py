from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os
import chromadb

print("debut")


embedding_fn = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="CrewAi-RAG/src/projet/chromadb",
    embedding_function=embedding_fn
    )

retriever = vectorstore.as_retriever()

def rag_query(query: str):
    results = retriever.get_relevant_documents(query)
    return "\n\n".join([
        f"Source: {doc.metadata.get('source', 'inconnu')}\n{doc.page_content}"
        for doc in results
    ])

print(rag_query("qu'est-ce que JADE"))
