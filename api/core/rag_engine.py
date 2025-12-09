import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "vector_db", "medi_chromadb")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

def get_retriever():
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 6})

def get_rag_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Stable Dec 2025 model
        temperature=0.1,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a cautious medical assistant.
Use ONLY the context. If no info, say "I don't have information on this."
Always end with: "Please consult a qualified doctor."

Context: {context}"""),
        ("human", "{input}")
    ])

    question_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(get_retriever(), question_chain)
    return rag_chain

_rag_chain = None
def get_chain():
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = get_rag_chain()
    return _rag_chain