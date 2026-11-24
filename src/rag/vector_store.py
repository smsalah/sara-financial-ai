import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.llm_factory import get_embeddings


class RAGEngine:
    def __init__(self, persist_directory: str = None):
        if persist_directory is None:
            persist_directory = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db")
            )
        self.persist_directory = persist_directory
        self.embeddings = get_embeddings()
        self.vector_store = Chroma(
            persist_directory=self.persist_directory, embedding_function=self.embeddings
        )

    def ingest_document(
        self, file_path: str, vendor: str = "Nexus Cloud Technologies LLC"
    ):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found at {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)

        documents = [
            Document(
                page_content=chunk,
                metadata={
                    "vendor": vendor,
                    "source": os.path.basename(file_path),
                    "chunk_id": i,
                },
            )
            for i, chunk in enumerate(chunks)
        ]

        self.vector_store.add_documents(documents)
        print(f"✅ Ingested {len(documents)} chunks with metadata (Vendor: {vendor}).")

    def query(self, query_text: str, vendor_filter: str = None, k: int = 3) -> str:
        search_kwargs = {"k": k}
        if vendor_filter:
            search_kwargs["filter"] = {"vendor": vendor_filter}

        retriever = self.vector_store.as_retriever(search_kwargs=search_kwargs)
        docs = retriever.invoke(query_text)

        if not docs:
            return "No matching invoice records found in vector store."

        return "\n---\n".join([doc.page_content for doc in docs])
