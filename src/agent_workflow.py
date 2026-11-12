import os
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from src.llm_factory import get_llm
from src.agent_tools import search_invoice_records, calculate_late_penalty
from src.rag_engine import RAGEngine

def run_reconciliation_agent():
    print("=" * 70)
    print("  Sara Financial AI — Milestone 2 (DeepSeek-R1 32B Bound Agent)")
    print("=" * 70)

    # 1. Ensure sample document is ingested into Chroma DB first
    sample_file = os.path.join(os.path.dirname(__file__), "..", "data", "sample_invoice.txt")
    rag = RAGEngine()
    rag.ingest_document(sample_file)

    # 2. Get LLM via Factory and explicitly bind tools for Ollama
    llm = get_llm()
    tools = [search_invoice_records, calculate_late_penalty]
    llm_with_tools = llm.bind_tools(tools)

    # 3. Create ReAct agent using LangGraph prebuilt
    system_prompt = (
        "You are an expert Enterprise Financial Audit & Reconciliation Agent. "
        "You MUST use the 'search_invoice_records' tool to retrieve exact invoice details from the vector database. "
        "Do NOT guess or hallucinate invoice totals or penalty rates. "
        "After retrieving the facts, use the 'calculate_late_penalty' tool to compute the exact overdue totals."
    )
    
    agent_executor = create_react_agent(model=llm_with_tools, tools=tools, prompt=system_prompt)

    # 4. Complex Multi-Step Query test
    query = (
        "Audit Invoice INV-9942. Find the total amount due and late payment terms from the documents, "
        "then calculate what the total payable amount would be if the invoice is 3 months overdue."
    )

    print(f"\n📋 Agent Prompt:\n{query}\n")
    print("🤖 Agent Execution Trace (Watching Tool Invocations):")
    print("-" * 70)

    # Execute and stream agent response steps
    for step in agent_executor.stream({"messages": [HumanMessage(content=query)]}, stream_mode="values"):
        latest_message = step["messages"][-1]
        if isinstance(latest_message, AIMessage) and latest_message.content:
            # Filter out internal think tags if desired, or print reasoning
            content = latest_message.content
            print(f"\n🤖 AI / Reasoning:\n{content}")
        elif latest_message.type == "tool":
            print(f"\n🛠️ Tool Executed [{latest_message.name}]:\n{latest_message.content}")

if __name__ == "__main__":
    run_reconciliation_agent()
