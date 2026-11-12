import os
from src.rag_engine import RAGEngine

def main():
    print("=" * 60)
    print("  Enterprise Financial AI Assistant — Milestone 1 (RAG Core)")
    print("=" * 60)
    sample_file = os.path.join(os.path.dirname(__file__), "..", "data", "sample_invoice.txt")
    rag = RAGEngine()
    rag.ingest_document(sample_file)
    queries = [
        "What is the total amount due on Invoice INV-9942?",
        "Are there any penalty terms for late payments mentioned?",
        "What line items are included under cloud service charges?"
    ]
    for q in queries:
        response = rag.query(q)
        print(f"\n💡 Answer:\n{response}")
        print("-" * 60)

if __name__ == "__main__":
    main()
