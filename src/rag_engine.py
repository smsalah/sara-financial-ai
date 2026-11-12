import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.llm_factory import get_llm, get_embeddings
from src.config import Config

class RAGEngine:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.llm = get_llm()
        self.vector_store = None
        self.retriever = None
        self.chain = None

    def ingest_document(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        print(f"📄 Loading document: {file_path}")
        loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        print(f"🧩 Split document into {len(chunks)} chunks.")
        print("💾 Generating embeddings and storing in Chroma Vector DB...")
        self.vector_store = Chroma.from_documents(documents=chunks, embedding=self.embeddings, persist_directory=Config.CHROMA_PERSIST_DIR)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        self._build_chain()
        print("✅ Document ingestion complete.")

    def _build_chain(self):
        prompt_template = """You are an Enterprise Financial Assistant specializing in audit and reconciliation.
Use ONLY the provided context below to answer the query accurately. If you do not know the answer based on context, state that clearly.

Context:
{context}

Question:
{question}

Detailed Audit Response:"""
        prompt = ChatPromptTemplate.from_template(prompt_template)
        format_docs = lambda docs: "\n\n".join(doc.page_content for doc in docs)
        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, question: str) -> str:
        if not self.chain:
            raise ValueError("No document ingested yet. Call ingest_document() first.")
        print(f"\n🔍 Querying RAG System: '{question}'")
        return self.chain.invoke(question)
