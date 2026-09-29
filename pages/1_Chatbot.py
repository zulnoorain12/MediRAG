# pages/1_Chatbot.py
import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.navbar import render_navbar

API_URL = "http://127.0.0.1:8000/api/v1/chat"

st.set_page_config(
    page_title="MediRAG — Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_navbar("Chatbot")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

    [data-testid="stSidebarNav"] { display: none !important; }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
        color: #0f172a !important;
    }
    .stApp { background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 40%, #f0f9ff 100%); }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2.5rem 2rem; max-width: 1000px; }

    /* ── Sidebar & Nav Styling (FORCE DARK CRISP TEXT) ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%) !important;
        border-right: 1px solid #d1fae5 !important;
    }
    [data-testid="stSidebarNav"] * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebarNav"] a {
        background-color: transparent !important;
        border-radius: 12px !important;
        margin: 2px 8px !important;
        padding: 8px 12px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background-color: #d1fae5 !important;
        color: #047857 !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(135deg, #10b981, #06b6d4) !important;
        box-shadow: 0 4px 12px rgba(16,185,129,.3) !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Page header */
    .chat-header {
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
    .chat-header-icon {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #ecfdf5, #e0f2fe);
        border-radius: 16px;
        padding: 0.6rem;
        border: 1px solid #a7f3d0;
    }
    .chat-header-text h1 {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #059669, #0891b2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .chat-header-text p { color: #475569 !important; font-size: 0.88rem; margin: 0.2rem 0 0; }

    /* Status bar */
    .status-bar {
        display: flex;
        gap: 0.8rem;
        margin-bottom: 1.2rem;
        flex-wrap: wrap;
    }
    .status-chip {
        background: white;
        border: 1px solid #d1fae5;
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #059669 !important;
        box-shadow: 0 1px 4px rgba(16,185,129,.08);
    }

    /* Chat messages override */
    [data-testid="stChatMessage"] {
        background: white !important;
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,.04) !important;
        margin-bottom: 0.8rem !important;
        padding: 0.8rem 1rem !important;
        color: #0f172a !important;
    }
    [data-testid="stChatMessage"] * {
        color: #0f172a !important;
    }
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #ecfdf5, #e0f2fe) !important;
        border-color: #a7f3d0 !important;
    }

    /* ── Chat Input Styling (BLACK CRISP TYPING TEXT) ── */
    [data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 2px solid #a7f3d0 !important;
        background: white !important;
    }
    [data-testid="stChatInput"] input, [data-testid="stChatInput"] textarea {
        color: #0f172a !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16,185,129,.15) !important;
    }

    /* Source expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0fdf4, #e0f2fe) !important;
        border-radius: 10px !important;
        font-size: 0.82rem !important;
        color: #065f46 !important;
        font-weight: 700 !important;
        border: 1px solid #a7f3d0 !important;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background: white;
        border-radius: 20px;
        border: 2px dashed #a7f3d0;
        margin: 1rem 0;
    }
    .empty-state .icon { font-size: 3rem; margin-bottom: 0.8rem; }
    .empty-state h3 { color: #0f172a !important; font-family: 'Outfit', sans-serif; font-weight: 700; margin-bottom: 0.4rem; }
    .empty-state p { font-size: 0.88rem; color: #475569 !important; }

    /* Suggested questions */
    .suggest-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin-top: 1rem;
    }
    .suggest-chip {
        background: linear-gradient(135deg, #ecfdf5, #e0f2fe);
        border: 1px solid #a7f3d0;
        border-radius: 999px;
        padding: 5px 16px;
        font-size: 0.78rem;
        color: #065f46 !important;
        font-weight: 600;
    }

    /* Sidebar labels */
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
        color: #065f46 !important;
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

    # Session controls
    st.markdown("""<div class='sidebar-section'><h4>🗂️ Session</h4></div>""", unsafe_allow_html=True)

    msg_count = len(st.session_state.get("messages", []))
    st.metric("Messages in session", msg_count)

    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div class='sidebar-section' style='margin-top:1rem;'>
        <h4>💡 Sample Questions</h4>
        <div style='font-size:0.8rem; color:#1e293b; font-weight:500; line-height:2;'>
            • What are symptoms of COVID-19?<br>
            • Explain type 2 diabetes management<br>
            • What medications treat hypertension?<br>
            • Describe the cardiac cycle
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size:0.75rem; color:#64748b; text-align:center; margin-top:1rem;'>
        🔌 Backend: <code style='background:#f0fdf4; padding:1px 5px; border-radius:4px; color:#059669; font-weight:600;'>127.0.0.1:8000</code>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ──────────────────────────────────────────────────────────────
st.markdown("""
<div class='chat-header'>
    <div class='chat-header-icon'>💬</div>
    <div class='chat-header-text'>
        <h1>Medical Chatbot</h1>
        <p>Powered by Gemini LLM + Retrieval-Augmented Generation · Citations included</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='status-bar'>
    <div class='status-chip'>🟢 RAG Active</div>
    <div class='status-chip'>🔬 Source Grounded</div>
    <div class='status-chip'>🧠 Memory On</div>
    <div class='status-chip'>🛡️ Safety Filters</div>
</div>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Empty state ────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class='empty-state'>
        <div class='icon'>🩺</div>
        <h3>Ask your medical question</h3>
        <p>I'll search your uploaded documents and give a cited, grounded answer.</p>
        <div class='suggest-wrap'>
            <span class='suggest-chip'>COVID-19 symptoms</span>
            <span class='suggest-chip'>Diabetes management</span>
            <span class='suggest-chip'>Heart disease risk factors</span>
            <span class='suggest-chip'>Drug interactions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Display history ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📎 View Sources"):
                for s in msg["sources"]:
                    page_info = f" — Page {s['page']}" if s.get("page") else ""
                    st.caption(f"📄 {s.get('file', 'Unknown file')}{page_info}")

# ── Chat Input ─────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a medical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔬 Searching medical knowledge base..."):
            try:
                response = requests.post(API_URL, json={"question": prompt}, timeout=60)
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                sources = data.get("sources", [])

                st.markdown(answer)

                if sources:
                    with st.expander("📎 View Sources"):
                        for s in sources:
                            page_info = f" — Page {s['page']}" if s.get("page") else ""
                            st.caption(f"📄 {s.get('file', 'Unknown file')}{page_info}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI backend. Is it running on port 8000?")
                st.info("💡 Run in terminal: `uvicorn api.main:app --reload --port 8000`")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"🔴 API Error: {e}")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")