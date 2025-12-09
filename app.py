import streamlit as st
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="MediRAG - Medical Assistant",
    layout="centered",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #1E88E5; text-align: center; font-weight: bold;}
    .disclaimer {background-color: #FFEBEE; padding: 15px; border-radius: 10px; border-left: 6px solid #F44336;}
    .footer {text-align: center; margin-top: 50px; color: #666;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🩺 MediRAG</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.2rem;'>Intelligent Medical Assistant with RAG, Memory & Safety</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/100/000000/artificial-intelligence.png")
    st.header("Configuration")
    
    if API_KEY:
        st.success("API Key loaded securely")
    else:
        st.warning("Please add your GEMINI_API_KEY to .env file")
    
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("- No hallucinations (RAG)")
    st.markdown("- Cites medical sources")
    st.markdown("- Remembers patient history")
    st.markdown("- Strict safety filters")
    st.markdown("---")
    st.markdown("### Team")
    st.write("Abdur Rehman + 2 Members")
    st.markdown("[GitHub Repo](https://github.com)")

# Disclaimer
st.markdown("""
<div class='disclaimer'>
<strong>⚠️ MEDICAL DISCLAIMER</strong><br>
This tool is for <u>educational and informational purposes only</u>. 
It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
Always consult a qualified doctor. Never disregard professional medical advice because of something you read here.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='footer'>Developed for Generative AI & LLMs Semester Project 2025</div>", unsafe_allow_html=True)