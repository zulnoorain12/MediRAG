import streamlit as st
import os

st.title("Analytics & Feedback")

st.write("Knowledge Base Status")
db_path = "data/vector_db/medi_chromadb"
if os.path.exists(db_path):
    import chromadb
    client = chromadb.PersistentClient(path=db_path)
    collections = client.list_collections()
    total = sum(c.count() for c in collections) if collections else 0
    st.success(f"Active Knowledge Base: {total} chunks")
else:
    st.warning("No documents uploaded yet")

st.write("### Give Feedback")
feedback = st.text_area("Help us improve:")
if st.button("Submit Feedback"):
    with open("logs/feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{feedback}\n---\n")
    st.success("Thank you!")