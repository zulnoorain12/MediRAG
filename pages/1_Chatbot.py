# pages/1_Chatbot.py   ← 100% WORKING FINAL VERSION
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/v1/chat"

st.title("MediRAG Chat (Powered by FastAPI)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("View Sources"):
                for s in msg["sources"]:
                    page_info = f" — Page {s['page']}" if s.get('page') else ""
                    st.caption(f"• {s.get('file', 'Unknown file')}{page_info}")

# User input
if prompt := st.chat_input("Ask a medical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching medical knowledge base..."):
            try:
                response = requests.post(API_URL, json={"question": prompt}, timeout=30)
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                sources = data.get("sources", [])

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI backend. Is it running on port 8000?")
                st.info("Run in terminal: `uvicorn api.main:app --reload --port 8000`")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"API Error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")