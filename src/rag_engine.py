import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from src.llm_factory import get_embeddings
from src.config import Config

class RAGEngine:
    def __init__(self):
        self.embeddings = get_embeddings()
        # Ensure absolute path for Chroma DB persistence across modules
        self.persist_directory = os.path.abspath(Config.CHROMA_PERSIST_DIR)
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.vector_store = Chroma(
            collection_name="financial_docs",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def ingest_document(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found at: {file_path}")
        
        print(f"📄 Loading document: {file_path}")
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
            
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)
        print(f"🧩 Split document into {len(docs)} chunks.")

        print("💾 Generating embeddings and storing in Chroma Vector DB...")
        self.vector_store.add_documents(docs)
        print("✅ Document ingestion complete.")

    def query(self, query_text: str, k: int = 3) -> str:
        # Check if collection has documents by doing a similarity search
        results = self.vector_store.similarity_search(query_text, k=k)
        if not results:
            return "No documents ingested yet. Call ingest_document() first."
        
        context = "\n---\n".join([doc.page_content for doc in results])
        return context
