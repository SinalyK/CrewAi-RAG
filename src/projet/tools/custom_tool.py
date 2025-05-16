import sys
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules["pysqlite3"]
except ImportError:
    pass

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."



## vecstore: chargement

class RAGToolInput(BaseModel):
    query: str

class RAGPDFTool(BaseTool):
    name: str = "PDF Knowledge Base"
    description: str = "Utilise des documents PDF vectorisés pour répondre à des questions via recherche sémantique."
    args_schema: Type[BaseModel] = RAGToolInput

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        embedding_fn = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(
            persist_directory="chromadb",
            embedding_function=embedding_fn
        )
        self.retriever = self.vectorstore.as_retriever()

    def _run(self, query: str) -> str:
        docs = self.retriever.get_relevant_documents(query)
        if not docs:
            return "Aucun document pertinent trouvé."
        
        return "\n\n".join([
            f"[{doc.metadata.get('source', 'inconnu')}] {doc.page_content}"
            for doc in docs
        ])
