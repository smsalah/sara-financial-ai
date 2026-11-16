import streamlit as st
import requests

st.set_page_config(page_title="Sara Financial AI", page_icon="💼", layout="centered")

st.title("💼 Sara Financial AI")
st.markdown("Enterprise Autonomous Financial Auditing & RAG Reconciliation Agent")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User chat input
if prompt := st.chat_input("Ask about invoices, credit limits, or audit reports..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing ERP ledger and RAG records..."):
            try:
                response = requests.post(
                    "http://sara-financial-ai:8000/audit",
                    json={"query": prompt, "thread_id": "streamlit_user_session"}
                )
                if response.status_code == 200:
                    data = response.json()
                    agent_reply = data.get("response", "Audit completed.")
                else:
                    agent_reply = f"Error: Received status code {response.status_code}"
            except Exception as e:
                agent_reply = f"Connection error: Could not reach FastAPI backend. ({str(e)})"
            
            st.markdown(agent_reply)
            st.session_state.messages.append({"role": "assistant", "content": agent_reply})
