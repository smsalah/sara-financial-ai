import os
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from src.core.llm_factory import get_llm
from src.tools.agent_tools import search_invoice_records, calculate_late_penalty, query_erp_ledger, export_audit_report
from src.rag.vector_store import RAGEngine

def start_interactive_cli():
    print("=" * 70)
    print("  Sara Financial AI — Interactive Enterprise Audit Terminal (Streaming)")
    print("=" * 70)
    print("Type your financial audit requests below. Type 'exit' or 'quit' to end.\n")

    sample_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_invoice.txt"))
    rag = RAGEngine()
    if os.path.exists(sample_file):
        rag.ingest_document(sample_file)

    llm = get_llm()
    tools = [search_invoice_records, calculate_late_penalty, query_erp_ledger, export_audit_report]

    system_prompt = (
        "You are an expert Enterprise Financial Audit & Reconciliation Agent. "
        "Cross-reference RAG vector store invoice records and SQLite ERP ledger databases before compiling audit reports."
    )

    db_checkpoint_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "checkpoints.sqlite"))

    with SqliteSaver.from_conn_string(db_checkpoint_path) as checkpointer:
        agent_executor = create_agent(model=llm, tools=tools, system_prompt=system_prompt, checkpointer=checkpointer)
        thread_config = {"configurable": {"thread_id": "interactive_audit_session"}}

        while True:
            try:
                user_input = input("\n👤 Auditor Query: ").strip()
                if user_input.lower() in ("exit", "quit"):
                    print("\nExiting Sara Financial AI. Audit session saved to persistent checkpointer.")
                    break
                if not user_input:
                    continue

                print("\n🤖 Agent Execution Trace:")
                print("-" * 65)

                # Stream events using 'messages' mode to catch token chunks and tool calls live
                for msg, metadata in agent_executor.stream(
                    {"messages": [HumanMessage(content=user_input)]}, 
                    config=thread_config, 
                    stream_mode="messages"
                ):
                    if msg.type == "ai":
                        if msg.tool_calls:
                            print(f"\n🛠️ Tool Call Requested: {msg.tool_calls}")
                        elif msg.content:
                            print(msg.content, end="", flush=True)
                    elif msg.type == "tool":
                        print(f"\n📥 Tool Output [{msg.name}]: Completed.")
                print("\n")

            except KeyboardInterrupt:
                print("\nSession interrupted. Exiting...")
                break
            except Exception as e:
                print(f"\n❌ Error during execution: {str(e)}")

if __name__ == "__main__":
    start_interactive_cli()
