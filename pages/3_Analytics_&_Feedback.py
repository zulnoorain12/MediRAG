import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.navbar import render_navbar

st.set_page_config(
    page_title="MediRAG — Analytics & Feedback",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_navbar("Analytics")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size:3rem;'>📊</div>
        <div style='font-family:Outfit,sans-serif; font-size:1.3rem; font-weight:800;
                    background:linear-gradient(135deg,#059669,#0891b2);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;'>Analytics</div>
        <div style='font-size:0.75rem; color:#475569; font-weight:600; margin-top:3px;'>System Health Monitor</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='background:linear-gradient(135deg,#ecfdf5,#e0f2fe); border-radius:12px;
                padding:1rem; border:1px solid #a7f3d0; margin-bottom:0.8rem;'>
        <h4 style='margin:0 0 0.6rem; font-size:0.8rem; font-weight:700;
                   text-transform:uppercase; letter-spacing:0.08em; color:#065f46 !important;'>
            📈 What's Tracked
        </h4>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>🗄️ Vector DB Chunk Count</div>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>🤖 Active AI Model</div>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>🔍 Embedding Engine</div>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>💬 User Feedback Logs</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding:0.8rem 0; font-size:0.75rem; color:#64748b;'>
        <strong style='color:#059669;'>BH Venture</strong> &mdash; 2025
    </div>
    """, unsafe_allow_html=True)

# ── Custom CSS for Analytics Page ──
st.markdown("""
<style>
    .analytics-header {
        background: linear-gradient(135deg, #ffffff 0%, #ecfdf5 60%, #e0f2fe 100%);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.8rem;
        border: 1px solid #a7f3d0;
        box-shadow: 0 4px 20px rgba(16,185,129,.1);
        display: flex;
        align-items: center;
        gap: 1.2rem;
    }
    .analytics-header-icon {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #d1fae5, #cff4fc);
        border-radius: 16px;
        padding: 0.6rem 0.9rem;
        border: 1px solid #a7f3d0;
    }
    .analytics-header-text h1 {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #059669, #0891b2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .analytics-header-text p {
        font-size: 0.95rem;
        color: #0f172a !important;
        margin: 0.2rem 0 0;
        font-weight: 500;
    }

    .stat-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #d1fae5;
        box-shadow: 0 4px 16px rgba(16,185,129,.06);
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stat-number {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        color: #059669 !important;
    }
    .stat-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #0f172a !important;
    }

    .feedback-card {
        background: white;
        border-radius: 18px;
        padding: 1.8rem;
        border: 1px solid #a7f3d0;
        box-shadow: 0 4px 20px rgba(16,185,129,.08);
    }
    .feedback-card h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #065f46 !important;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="analytics-header">
    <div class="analytics-header-icon">📊</div>
    <div class="analytics-header-text">
        <h1>Analytics & System Health</h1>
        <p>Monitor vector database indices, system logs, and user feedback.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Knowledge Base Status ──
db_path = "data/vector_db/medi_chromadb"
total_chunks = 0
if os.path.exists(db_path):
    try:
        import chromadb
        client = chromadb.PersistentClient(path=db_path)
        collections = client.list_collections()
        total_chunks = sum(c.count() for c in collections) if collections else 0
    except Exception:
        total_chunks = 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_chunks}</div>
        <div class="stat-label">Indexed Knowledge Chunks</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">Gemini 2.5</div>
        <div class="stat-label">Active Generation Model</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">MiniLM-L6</div>
        <div class="stat-label">Local Embedding Engine</div>
    </div>
    """, unsafe_allow_html=True)

# ── Feedback Form ──
st.markdown('<div class="feedback-card">', unsafe_allow_html=True)
st.markdown("### 💬 User Feedback")
st.write("Share your experiences or suggest improvements for the MediRAG system:")

feedback = st.text_area("", placeholder="Type your feedback here...", height=120)

if st.button("📤 Submit Feedback", use_container_width=False):
    if feedback.strip():
        os.makedirs("logs", exist_ok=True)
        with open("logs/feedback.txt", "a", encoding="utf-8") as f:
            f.write(f"{feedback}\n---\n")
        st.success("✅ Thank you! Your feedback has been recorded.")
    else:
        st.warning("Please enter some text before submitting.")
st.markdown('</div>', unsafe_allow_html=True)