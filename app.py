import streamlit as st
from dotenv import load_dotenv
import os
from utils.navbar import render_navbar

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="MediRAG — Intelligent Medical Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_navbar("Home")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

    /* ── Hide Default Sidebar Navigation Menu ── */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* ── Global Reset ── */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
        color: #0f172a !important;
    }
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 40%, #f0f9ff 100%);
    }

    /* ── Sidebar Navigation Styling (FORCE DARK CRISP TEXT) ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%) !important;
        border-right: 1px solid #d1fae5 !important;
        box-shadow: 4px 0 20px rgba(16,185,129,.06) !important;
    }
    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
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
        transform: translateX(4px);
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(135deg, #10b981, #06b6d4) !important;
        box-shadow: 0 4px 12px rgba(16,185,129,.3) !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* ── Hide Streamlit Header Chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 3rem 3rem; max-width: 1100px; }

    /* ── General Text & Input Visibility ── */
    p, span, label, h1, h2, h3, h4, h5, h6, div {
        color: #0f172a;
    }

    /* ── Hero Header ── */
    .hero-wrap {
        text-align: center;
        padding: 3.5rem 2rem 2rem;
        background: linear-gradient(135deg, #ffffff 0%, #ecfdf5 60%, #e0f2fe 100%);
        border-radius: 24px;
        border: 1px solid #a7f3d0;
        box-shadow: 0 8px 40px rgba(16,185,129,.12), 0 2px 8px rgba(14,165,233,.08);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-wrap::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        background: radial-gradient(circle, rgba(52,211,153,.18) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-wrap::after {
        content: '';
        position: absolute;
        bottom: -50px; left: -50px;
        width: 180px; height: 180px;
        background: radial-gradient(circle, rgba(56,189,248,.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981, #06b6d4);
        color: white !important;
        font-family: 'Outfit', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 5px 16px;
        border-radius: 999px;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #059669, #0891b2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        margin: 0 0 0.6rem;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #475569 !important;
        font-weight: 500;
        margin: 0 0 1.8rem;
        max-width: 540px;
        margin-left: auto;
        margin-right: auto;
    }

    /* ── Feature Cards ── */
    .feat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }
    .feat-card {
        background: white;
        border-radius: 16px;
        padding: 1.4rem 1rem;
        text-align: center;
        border: 1px solid #d1fae5;
        box-shadow: 0 2px 12px rgba(16,185,129,.07);
        transition: transform .2s, box-shadow .2s;
    }
    .feat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(16,185,129,.15);
    }
    .feat-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .feat-title { font-weight: 700; color: #064e3b !important; font-size: 0.9rem; margin-bottom: 0.3rem; }
    .feat-desc { color: #475569 !important; font-size: 0.78rem; line-height: 1.4; }

    /* ── Disclaimer ── */
    .disclaimer-box {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border: 1px solid #fcd34d;
        border-left: 5px solid #f59e0b;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-top: 1.5rem;
    }
    .disclaimer-box strong { color: #92400e !important; font-size: 0.95rem; }
    .disclaimer-box p { color: #78350f !important; font-size: 0.88rem; margin: 0.4rem 0 0; line-height: 1.6; }

    /* ── Sidebar labels ── */
    .sidebar-section {
        background: linear-gradient(135deg, #ecfdf5, #e0f2fe);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        border: 1px solid #a7f3d0;
    }
    .sidebar-section h4 {
        margin: 0 0 0.6rem;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #065f46 !important;
    }
    .sidebar-feat-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 5px 0;
        font-size: 0.83rem;
        color: #1e293b !important;
        font-weight: 600;
    }

    /* ── Status pill ── */
    .status-ok {
        display: inline-block;
        background: #d1fae5;
        color: #065f46 !important;
        border-radius: 999px;
        padding: 3px 12px;
        font-size: 0.78rem;
        font-weight: 700;
        border: 1px solid #6ee7b7;
    }
    .status-warn {
        display: inline-block;
        background: #fef3c7;
        color: #92400e !important;
        border-radius: 999px;
        padding: 3px 12px;
        font-size: 0.78rem;
        font-weight: 700;
        border: 1px solid #fcd34d;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        font-size: 0.8rem;
        color: #64748b !important;
        border-top: 1px solid #d1fae5;
    }
    .footer span { color: #10b981 !important; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size:3rem;'>🩺</div>
        <div style='font-family:Outfit,sans-serif; font-size:1.4rem; font-weight:800;
                    background:linear-gradient(135deg,#059669,#0891b2);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;'>MediRAG</div>
        <div style='font-size:0.75rem; color:#475569; font-weight:600; margin-top:3px;'>AI Medical Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # API status
    if API_KEY:
        st.markdown("<div class='status-ok'>✅ API Key Active</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-warn'>⚠️ No API Key Found</div>", unsafe_allow_html=True)
        st.caption("Add GEMINI_API_KEY to your .env file")

    # Features
    st.markdown("""
    <div class='sidebar-section'>
        <h4>⚡ Capabilities</h4>
        <div class='sidebar-feat-item'>🔬 RAG-powered — No hallucinations</div>
        <div class='sidebar-feat-item'>📚 Cites medical sources</div>
        <div class='sidebar-feat-item'>🧠 Remembers patient history</div>
        <div class='sidebar-feat-item'>🛡️ Strict safety filters</div>
        <div class='sidebar-feat-item'>📄 PDF & TXT ingestion</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding: 0.8rem 0; font-size:0.75rem; color:#64748b;'>
        <strong style='color:#059669;'>BH Venture</strong> &mdash; 2025
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap'>
    <div class='hero-badge'>🧬 Powered by Gemini + RAG</div>
    <div class='hero-title'>🩺 MediRAG</div>
    <div class='hero-sub'>Your intelligent medical knowledge assistant — grounded in real documents, never guessing.</div>
</div>
""", unsafe_allow_html=True)

# Feature cards
st.markdown("""
<div class='feat-grid'>
    <div class='feat-card'>
        <div class='feat-icon'>🔬</div>
        <div class='feat-title'>RAG Architecture</div>
        <div class='feat-desc'>Retrieves from your uploaded docs — zero hallucinations</div>
    </div>
    <div class='feat-card'>
        <div class='feat-icon'>📚</div>
        <div class='feat-title'>Source Citations</div>
        <div class='feat-desc'>Every answer cites the exact document & page</div>
    </div>
    <div class='feat-card'>
        <div class='feat-icon'>🧠</div>
        <div class='feat-title'>Conversation Memory</div>
        <div class='feat-desc'>Remembers full session context like a real doctor</div>
    </div>
    <div class='feat-card'>
        <div class='feat-icon'>🛡️</div>
        <div class='feat-title'>Safety First</div>
        <div class='feat-desc'>Built-in guardrails — always recommends professionals</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class='disclaimer-box'>
    <strong>⚠️ Medical Disclaimer</strong>
    <p>
        This tool is for <u>educational and informational purposes only</u>. It is <strong>NOT</strong> a substitute
        for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare
        professional. Never disregard professional medical advice based on information from this tool.
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    Developed for <span>Generative AI & LLMs</span> — Semester Project 2025 &nbsp;|&nbsp;
    MediRAG v1.0
</div>
""", unsafe_allow_html=True)