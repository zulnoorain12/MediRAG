import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.navbar import render_navbar

st.set_page_config(
    page_title="MediRAG — Upload Documents",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_navbar("Upload Docs")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

    [data-testid="stSidebarNav"] { display: none !important; }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 40%, #f0f9ff 100%); }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2.5rem 2rem; max-width: 1000px; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%);
        border-right: 1px solid #d1fae5;
    }

    /* Page header */
    .upload-header {
        background: linear-gradient(135deg, #ffffff, #ecfdf5);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #a7f3d0;
        box-shadow: 0 4px 20px rgba(16,185,129,.1);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .upload-header-icon {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #ecfdf5, #e0f2fe);
        border-radius: 16px;
        padding: 0.6rem;
        border: 1px solid #a7f3d0;
    }
    .upload-header-text h1 {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #059669, #0891b2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .upload-header-text p { color: #6b7280; font-size: 0.88rem; margin: 0.2rem 0 0; }

    /* Upload zone */
    .upload-zone {
        background: white;
        border: 2px dashed #6ee7b7;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: border-color .2s, background .2s;
        margin-bottom: 1.2rem;
    }
    .upload-zone:hover {
        border-color: #10b981;
        background: #f0fdf4;
    }

    /* Info cards row */
    .info-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .info-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem 1rem;
        text-align: center;
        border: 1px solid #d1fae5;
        box-shadow: 0 2px 8px rgba(16,185,129,.07);
    }
    .info-card .ic-icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
    .info-card .ic-label { font-size: 0.78rem; color: #6b7280; }
    .info-card .ic-value { font-size: 1rem; font-weight: 700; color: #065f46; }

    /* Process button */
    .stButton > button {
        background: linear-gradient(135deg, #10b981, #06b6d4) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 15px rgba(16,185,129,.35) !important;
        transition: transform .15s, box-shadow .15s !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(16,185,129,.45) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* Progress steps */
    .step-box {
        background: white;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0;
        border: 1px solid #d1fae5;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 2px 6px rgba(16,185,129,.06);
    }
    .step-num {
        background: linear-gradient(135deg, #10b981, #06b6d4);
        color: white;
        border-radius: 999px;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.8rem;
        flex-shrink: 0;
    }
    .step-text { font-size: 0.88rem; color: #374151; }
    .step-text strong { color: #065f46; }

    /* Sidebar */
    .sidebar-section {
        background: linear-gradient(135deg, #ecfdf5, #e0f2fe);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        border: 1px solid #a7f3d0;
    }
    .sidebar-section h4 {
        margin: 0 0 0.6rem;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #065f46;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white !important;
        border-radius: 16px !important;
        border: 2px dashed #6ee7b7 !important;
        padding: 1rem !important;
    }
    [data-testid="stFileUploader"]:hover { border-color: #10b981 !important; }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0fdf4, #e0f2fe) !important;
        border-radius: 10px !important;
        font-size: 0.82rem !important;
        color: #065f46 !important;
        font-weight: 600 !important;
        border: 1px solid #a7f3d0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size:3rem;'>🩺</div>
        <div style='font-family:Outfit,sans-serif; font-size:1.4rem; font-weight:800;
                    background:linear-gradient(135deg,#059669,#0891b2);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;'>MediRAG</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div class='sidebar-section'>
        <h4>📋 How it works</h4>
        <div style='font-size:0.78rem; color:#374151; line-height:2.2;'>
            1️⃣ Upload PDF or TXT files<br>
            2️⃣ Click <strong>Process & Index</strong><br>
            3️⃣ Docs split into chunks<br>
            4️⃣ Embeddings stored in ChromaDB<br>
            5️⃣ Chatbot can now cite them ✅
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='sidebar-section'>
        <h4>📁 Supported Formats</h4>
        <div style='font-size:0.78rem; color:#374151; line-height:2;'>
            📄 <strong>PDF</strong> — Medical journals, reports<br>
            📝 <strong>TXT</strong> — Clinical notes, protocols
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ──────────────────────────────────────────────────────────────
st.markdown("""
<div class='upload-header'>
    <div class='upload-header-icon'>📤</div>
    <div class='upload-header-text'>
        <h1>Upload Medical Documents</h1>
        <p>Index PDF & TXT files into the RAG knowledge base · ChromaDB vector store</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Info cards
st.markdown("""
<div class='info-row'>
    <div class='info-card'>
        <div class='ic-icon'>📄</div>
        <div class='ic-value'>PDF + TXT</div>
        <div class='ic-label'>Supported formats</div>
    </div>
    <div class='info-card'>
        <div class='ic-icon'>✂️</div>
        <div class='ic-value'>1000 chars</div>
        <div class='ic-label'>Chunk size</div>
    </div>
    <div class='info-card'>
        <div class='ic-icon'>🗄️</div>
        <div class='ic-value'>ChromaDB</div>
        <div class='ic-label'>Vector store</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Process logic ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

embeddings = get_embeddings()

def process_uploaded_files(uploaded_files):
    if not uploaded_files:
        st.warning("⚠️ No files uploaded.")
        return 0

    docs = []
    temp_dir = "data/raw_docs/temp"
    os.makedirs(temp_dir, exist_ok=True)

    for file in uploaded_files:
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        st.info(f"⏳ Processing: **{file.name}**")
        try:
            if file.name.lower().endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding="utf-8")

            loaded_docs = loader.load()
            st.success(f"✅ Extracted **{len(loaded_docs)} pages** from `{file.name}`")

            if loaded_docs:
                with st.expander(f"👁️ Preview — {file.name}"):
                    st.code(loaded_docs[0].page_content[:600] + "...", language=None)

            docs.extend(loaded_docs)
        except Exception as e:
            st.error(f"❌ Failed to read `{file.name}`: {e}")

    if not docs:
        st.error("No text could be extracted from the uploaded files.")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return 0

    with st.status("🔄 Chunking & indexing documents…", expanded=True) as status:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        st.write(f"📦 Created **{len(chunks)} chunks**")

        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="data/vector_db/medi_chromadb"
        )
        st.write("🗄️ Stored in **ChromaDB** vector database")
        status.update(label=f"✅ Done — {len(chunks)} chunks indexed!", state="complete")

    st.balloons()
    shutil.rmtree(temp_dir, ignore_errors=True)
    return len(chunks)

# ── Upload widget ──────────────────────────────────────────────────────────────
st.markdown("### 📂 Select Files to Upload")
uploaded_files = st.file_uploader(
    "Drop your PDF or TXT medical documents here",
    accept_multiple_files=True,
    type=["pdf", "txt"],
    help="You can upload multiple files at once. Large PDFs may take a few seconds."
)

if uploaded_files:
    file_count = len(uploaded_files)
    total_size = sum(f.size for f in uploaded_files)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#ecfdf5,#e0f2fe); border:1px solid #a7f3d0;
                border-radius:12px; padding:0.8rem 1.2rem; margin:0.8rem 0;
                font-size:0.85rem; color:#065f46;'>
        📎 <strong>{file_count} file{'s' if file_count > 1 else ''}</strong> selected
        &nbsp;·&nbsp; Total size: <strong>{total_size / 1024:.1f} KB</strong>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Process & Index Documents"):
        with st.spinner("🔬 Indexing your medical documents..."):
            count = process_uploaded_files(uploaded_files)
            if count:
                st.success(f"🎉 Successfully indexed **{count} chunks** into the knowledge base!")
                st.markdown("""
                <div style='background:linear-gradient(135deg,#ecfdf5,#e0f2fe); border:1px solid #a7f3d0;
                            border-radius:14px; padding:1rem 1.4rem; margin-top:0.8rem;'>
                    <strong style='color:#065f46;'>✅ What's next?</strong><br>
                    <span style='font-size:0.85rem; color:#374151;'>
                        Head to the <strong>💬 Chatbot</strong> page and start asking questions about your documents!
                    </span>
                </div>
                """, unsafe_allow_html=True)
else:
    # Pipeline steps
    st.markdown("### 🔄 Processing Pipeline")
    st.markdown("""
    <div class='step-box'><div class='step-num'>1</div><div class='step-text'>Upload <strong>PDF or TXT</strong> medical documents above</div></div>
    <div class='step-box'><div class='step-num'>2</div><div class='step-text'>Documents are <strong>loaded & parsed</strong> page by page</div></div>
    <div class='step-box'><div class='step-num'>3</div><div class='step-text'>Text is split into <strong>1000-char chunks</strong> with 200-char overlap</div></div>
    <div class='step-box'><div class='step-num'>4</div><div class='step-text'><strong>MiniLM embeddings</strong> computed for each chunk</div></div>
    <div class='step-box'><div class='step-num'>5</div><div class='step-text'>Chunks stored in <strong>ChromaDB</strong> — ready for RAG retrieval</div></div>
    """, unsafe_allow_html=True)