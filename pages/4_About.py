import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.navbar import render_navbar

st.set_page_config(
    page_title="MediRAG — About Platform",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_navbar("About")

# ── Sidebar ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size:3rem;'>ℹ️</div>
        <div style='font-family:Outfit,sans-serif; font-size:1.3rem; font-weight:800;
                    background:linear-gradient(135deg,#059669,#0891b2);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;'>About</div>
        <div style='font-size:0.75rem; color:#475569; font-weight:600; margin-top:3px;'>MediRAG Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='background:linear-gradient(135deg,#ecfdf5,#e0f2fe); border-radius:12px;
                padding:1rem; border:1px solid #a7f3d0; margin-bottom:0.8rem;'>
        <h4 style='margin:0 0 0.6rem; font-size:0.8rem; font-weight:700;
                   text-transform:uppercase; letter-spacing:0.08em; color:#065f46 !important;'>
            🛠️ Tech Stack
        </h4>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>🧠 Gemini 2.5 Pro (LLM)</div>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>🔍 ChromaDB (Vector Store)</div>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>⚡ FastAPI (Backend)</div>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>🌐 Streamlit (Frontend)</div>
        <div style='font-size:0.82rem; color:#1e293b !important; font-weight:600; padding:4px 0;'>🔗 LangChain (RAG Pipeline)</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding:0.8rem 0; font-size:0.75rem; color:#64748b;'>
        <strong style='color:#059669;'>BH Venture</strong> &mdash; 2025
    </div>
    """, unsafe_allow_html=True)

# ── Custom CSS for About Page ──
st.markdown("""
<style>
    .about-header {
        background: linear-gradient(135deg, #ffffff 0%, #ecfdf5 60%, #e0f2fe 100%);
        border-radius: 20px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.8rem;
        border: 1px solid #a7f3d0;
        box-shadow: 0 4px 20px rgba(16,185,129,.1);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .about-header-icon {
        font-size: 3rem;
        background: linear-gradient(135deg, #d1fae5, #cff4fc);
        border-radius: 18px;
        padding: 0.7rem 1rem;
        border: 1px solid #a7f3d0;
    }
    .about-header-text h1 {
        font-family: 'Outfit', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #059669, #0891b2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .about-header-text p {
        font-size: 1.05rem;
        color: #0f172a !important;
        margin: 0.3rem 0 0;
        font-weight: 500;
    }

    .info-card {
        background: white;
        border-radius: 18px;
        padding: 1.8rem;
        border: 1px solid #a7f3d0;
        box-shadow: 0 4px 20px rgba(16,185,129,.08);
        height: 100%;
    }
    .info-card h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #065f46 !important;
        margin-top: 0;
        font-size: 1.25rem;
        margin-bottom: 1rem;
    }
    .info-list {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }
    .info-list li {
        font-size: 0.95rem;
        font-weight: 500;
        color: #0f172a !important;
        margin-bottom: 0.8rem;
        line-height: 1.5;
    }
    .info-list strong {
        color: #065f46 !important;
        font-weight: 700;
    }

    .use-case-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.2rem;
        margin-top: 1.5rem;
    }
    .use-case-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.4rem;
        border: 1px solid #d1fae5;
        box-shadow: 0 2px 10px rgba(16,185,129,.05);
    }
    .use-case-card h4 {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #047857 !important;
        margin: 0 0 0.4rem;
    }
    .use-case-card p {
        font-size: 0.88rem;
        color: #0f172a !important;
        margin: 0;
        line-height: 1.45;
    }

    .venture-badge-container {
        margin-top: 2rem;
        background: linear-gradient(135deg, #059669, #0891b2);
        border-radius: 18px;
        padding: 1.5rem 2rem;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 6px 24px rgba(16,185,129,.2);
    }
    .venture-badge-container * {
        color: white !important;
    }
    .venture-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
    }
    .venture-desc {
        font-size: 0.95rem;
        margin: 0.3rem 0 0;
        opacity: 0.95;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="about-header">
    <div class="about-header-icon">🩺</div>
    <div class="about-header-text">
        <h1>MediRAG Intelligence Platform</h1>
        <p>An enterprise-grade Retrieval-Augmented Generation (RAG) platform engineered by <strong>BH Venture</strong> for grounded, verifiable medical document intelligence.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Core Columns ──
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🚀 Technical Architecture</h3>
        <ul class="info-list">
            <li>🔬 <strong>Retrieval-Augmented Generation (RAG):</strong> Restricts AI answers strictly to uploaded clinical guidelines and medical literature.</li>
            <li>⚡ <strong>FastAPI Backend Service:</strong> Decoupled high-speed RESTful microservice providing OpenAPI (Swagger) document querying endpoints.</li>
            <li>📚 <strong>Chroma Vector Database:</strong> Embedded vector store providing sub-second semantic retrieval across thousands of text chunks.</li>
            <li>🧠 <strong>Local Transformer Embeddings:</strong> Utilizes HuggingFace <code>sentence-transformers</code> for zero-cost, privacy-focused offline indexing.</li>
            <li>🛡️ <strong>Clinical Safety Filters:</strong> Automated medical disclaimers and multi-layer query validation guardrails.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>💡 Key Business Innovations</h3>
        <ul class="info-list">
            <li>📄 <strong>Page-Level Source Citations:</strong> Automatically references exact document names and page numbers for complete auditability.</li>
            <li>🔒 <strong>Data Privacy & Security:</strong> Local document chunking ensures confidential medical data never leaves the secure environment.</li>
            <li>💬 <strong>Context-Aware Session Memory:</strong> Maintains multi-turn conversation context while adhering to safety protocols.</li>
            <li>📊 <strong>Knowledge Health Monitoring:</strong> Real-time indexing telemetry to track vector storage growth and system health.</li>
            <li>🌐 <strong>Modern Modular Frontend:</strong> Responsive Streamlit UI decoupled from the core inference microservice.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ── Use Cases Section ──
st.markdown("<h3 style='font-family: Outfit, sans-serif; font-weight: 700; color: #065f46 !important; margin-top: 2rem; margin-bottom: 0.5rem;'>🎯 Enterprise Use Cases</h3>", unsafe_allow_html=True)

st.markdown("""
<div class="use-case-grid">
    <div class="use-case-card">
        <h4>📋 Clinical Guideline QA</h4>
        <p>Instant search and query resolution across hospital protocols, drug formularies, and clinical treatment manuals.</p>
    </div>
    <div class="use-case-card">
        <h4>🔬 Medical Literature Review</h4>
        <p>Accelerates medical research synthesis by extracting grounded insights directly from clinical study PDFs.</p>
    </div>
    <div class="use-case-card">
        <h4>🏥 Patient Education & Support</h4>
        <p>Generates verifiable, citation-backed answers to assist health education teams with strict safety guardrails.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── BH Venture Footer Banner ──
st.markdown("""
<div class="venture-badge-container">
    <div>
        <div class="venture-title">BH Venture Innovation Project</div>
        <div class="venture-desc">Pioneering safe, verifiable, and transparent Artificial Intelligence solutions for enterprise healthcare.</div>
    </div>
    <div style="font-size: 2rem;">⚡</div>
</div>
""", unsafe_allow_html=True)