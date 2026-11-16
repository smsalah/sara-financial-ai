import os
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from src.core.llm_factory import get_llm
from src.tools.agent_tools import search_invoice_records, calculate_late_penalty, query_erp_ledger, export_audit_report
from src.rag.vector_store import RAGEngine

def run_reconciliation_agent():
    print("=" * 70)
    print("  Sara Financial AI — Enterprise Modular Workflow")
    print("=" * 70)

    sample_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_invoice.txt"))
    rag = RAGEngine()
    if os.path.exists(sample_file):
        rag.ingest_document(sample_file)

    llm = get_llm()
    tools = [search_invoice_records, calculate_late_penalty, query_erp_ledger, export_audit_report]

    system_prompt = (
        "You are an expert Enterprise Financial Audit & Reconciliation Agent. "
        "CRITICAL INSTRUCTIONS:\n"
        "- Call 'search_invoice_records' to retrieve exact invoice details from the vector store.\n"
        "- Call 'query_erp_ledger' to check the client's account status and credit limit in the ERP database.\n"
        "- Call 'calculate_late_penalty' to compute late fees.\n"
        "- Call 'export_audit_report' to save the finalized executive audit report to disk.\n"
        "- Always cross-reference vector store and ERP records before compiling your final report."
    )

    db_checkpoint_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "checkpoints.sqlite"))
    
    with SqliteSaver.from_conn_string(db_checkpoint_path) as checkpointer:
        agent_executor = create_agent(model=llm, tools=tools, system_prompt=system_prompt, checkpointer=checkpointer)
        thread_config = {"configurable": {"thread_id": "audit_session_inv_9942"}}

        query_1 = (
            "Audit Invoice INV-9942 for Zumzum Enterprise Solutions UK. "
            "Find the total amount due from RAG, check their account status in the ERP ledger, "
            "calculate the total payable amount if 3 months overdue, and export the final executive audit report using export_audit_report."
        )

        print(f"\n📋 Turn 1 Prompt:\n{query_1}\n")
        print("🤖 Agent Execution Trace:")
        print("-" * 70)

        for event in agent_executor.stream({"messages": [HumanMessage(content=query_1)]}, config=thread_config, stream_mode="values"):
            latest_message = event["messages"][-1]
            if latest_message.type == "ai":
                if latest_message.tool_calls:
                    print(f"\n🛠️ Model Requesting Tool Call: {latest_message.tool_calls}")
                elif latest_message.content:
                    print(f"\n🤖 AI Response (Turn 1):\n{latest_message.content}")
            elif latest_message.type == "tool":
                print(f"\n📥 Tool Output [{latest_message.name}]: Completed.")

        query_2 = "Based on that audit, does their outstanding balance exceed their ERP credit limit?"
        print(f"\n\n📋 Turn 2 Prompt (Testing Persistent SqliteSaver Memory):\n{query_2}\n")
        print("🤖 Agent Execution Trace (Turn 2):")
        print("-" * 70)

        for event in agent_executor.stream({"messages": [HumanMessage(content=query_2)]}, config=thread_config, stream_mode="values"):
            latest_message = event["messages"][-1]
            if latest_message.type == "ai":
                if latest_message.content and not latest_message.tool_calls:
                    print(f"\n🤖 AI Response (Turn 2 - Persistent Memory Retained):\n{latest_message.content}")

if __name__ == "__main__":
    run_reconciliation_agent()
