import streamlit as st

def render_navbar(active_page="Home"):
    """
    Renders a unified top navigation bar for MediRAG:
    - DESKTOP (> 768px): Full horizontal navbar with pill tabs (Home, Chatbot, Upload Docs, Analytics, About).
    - MOBILE (<= 768px): Switches to brand header + Mobile Hamburger Popover Menu ("☰ Menu").
    - 100% UNIFIED COLOR PALETTE & DESIGN SYSTEM across iPhone, Android, and Desktop.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

        /* ── Global Theme & Dark Black Text Enforcement ── */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif !important;
            color: #0f172a !important;
        }

        .stApp {
            background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 40%, #f0f9ff 100%) !important;
        }

        p, span, label, h1, h2, h3, h4, h5, h6, li, td, th {
            color: #0f172a !important;
        }
        /* Only force text color on content divs, NOT layout/container divs */
        .stMarkdown div:not(.nav-brand-title),
        .stText div,
        .element-container div:not(.nav-brand-title):not([class*="popover"]):not([data-baseweb]) {
            color: #0f172a !important;
        }

        /* ── Hide Streamlit Chrome & Default Sidebar Navigation ── */
        #MainMenu, footer, header { visibility: hidden !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        
        .block-container { 
            padding: 1.2rem 1.8rem 2rem !important; 
            max-width: 1100px !important; 
        }

        /* ── 1. UNIFIED NAVBAR CONTAINER STYLING (SAME ON DESKTOP & MOBILE) ── */
        [data-testid="stHorizontalBlock"]:has(.desktop-nav-tag),
        [data-testid="stHorizontalBlock"]:has(.mobile-nav-tag) {
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            justify-content: space-between !important;
            flex-wrap: nowrap !important;
            background: rgba(255, 255, 255, 0.96) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid #d1fae5 !important;
            border-radius: 999px !important;
            padding: 0.55rem 1.4rem !important;
            margin-bottom: 1.6rem !important;
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.09) !important;
        }

        [data-testid="stHorizontalBlock"]:has(.desktop-nav-tag) > [data-testid="column"] {
            min-width: max-content !important;
            width: auto !important;
            flex: 0 0 auto !important;
        }

        /* ── 2. UNIFIED BRAND LOGO & BADGE (SAME ON ALL DEVICES) ── */
        .nav-brand-title,
        .stMarkdown div.nav-brand-title,
        .element-container div.nav-brand-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
            color: #059669 !important;
            text-decoration: none;
            white-space: nowrap;
        }

        /* ── GLOBAL SIDEBAR BACKGROUND (applies on ALL pages) ── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%) !important;
            border-right: 1px solid #d1fae5 !important;
            box-shadow: 4px 0 20px rgba(16,185,129,.06) !important;
        }
        [data-testid="stSidebar"] * {
            color: #0f172a !important;
        }
        [data-testid="stSidebar"] a {
            background-color: transparent !important;
            border-radius: 12px !important;
            margin: 2px 8px !important;
            padding: 8px 12px !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stSidebar"] a:hover {
            background-color: #d1fae5 !important;
        }

        /* ── 3. UNIFIED ACTION BUTTONS & HAMBURGER POPOVER BUTTON (TEAL-GREEN GRADIENT) ── */
        div.stButton > button,
        div.stFormSubmitButton > button,
        [data-testid="stPopover"] > button,
        [data-testid="stPopover"] button,
        [data-testid="stFileUploader"] button,
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%) !important;
            background-color: #10b981 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 999px !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
            padding: 0.45rem 1.25rem !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.28) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            text-decoration: none !important;
        }

        /* Force white text/icons on ALL button children */
        div.stButton > button *,
        div.stFormSubmitButton > button *,
        [data-testid="stPopover"] > button *,
        [data-testid="stPopover"] button * {
            color: #ffffff !important;
            fill: #ffffff !important;
            stroke: #ffffff !important;
            font-weight: 700 !important;
            background-color: transparent !important;
        }

        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover,
        [data-testid="stPopover"] > button:hover,
        [data-testid="stFileUploader"] button:hover,
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #059669 0%, #0891b2 100%) !important;
            background-color: #059669 !important;
            color: #ffffff !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.38) !important;
        }

        /* ── 3b. STREAMLIT SIDEBAR HAMBURGER / COLLAPSE TOGGLE (MATCH NAVBAR COLOR) ── */
        [data-testid="stBaseButton-headerNoPadding"],
        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="collapsedControl"] button,
        button[kind="header"],
        [data-testid="stHeader"] button {
            background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%) !important;
            background-color: #10b981 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 50% !important;
            width: 2.2rem !important;
            height: 2.2rem !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.28) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        [data-testid="stBaseButton-headerNoPadding"] svg,
        [data-testid="stSidebarCollapsedControl"] button svg,
        [data-testid="collapsedControl"] button svg,
        button[kind="header"] svg,
        [data-testid="stHeader"] button svg {
            color: #ffffff !important;
            fill: #ffffff !important;
            stroke: #ffffff !important;
        }

        [data-testid="stBaseButton-headerNoPadding"]:hover,
        [data-testid="stSidebarCollapsedControl"] button:hover,
        [data-testid="collapsedControl"] button:hover,
        button[kind="header"]:hover,
        [data-testid="stHeader"] button:hover {
            background: linear-gradient(135deg, #059669 0%, #0891b2 100%) !important;
            background-color: #059669 !important;
            transform: scale(1.08) !important;
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.38) !important;
        }

        /* ── 4. UNIFIED NAVIGATION PAGE LINKS (SAME ON DESKTOP & MOBILE) ── */
        .stPageLink > a {
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 999px !important;
            padding: 0.45rem 1.15rem !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
            color: #0f172a !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
            white-space: nowrap !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-decoration: none !important;
        }

        .stPageLink > a * {
            color: #0f172a !important;
            font-weight: 700 !important;
        }

        .stPageLink > a:hover {
            background: #d1fae5 !important;
            border-color: #34d399 !important;
            color: #064e3b !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(16,185,129,0.18) !important;
        }

        /* Active Page Link Highlight (Same Emerald Gradient on All Devices) */
        .stPageLink > a[aria-current="page"] {
            background: linear-gradient(135deg, #10b981, #06b6d4) !important;
            border-color: transparent !important;
            box-shadow: 0 4px 14px rgba(16,185,129,0.35) !important;
        }

        .stPageLink > a[aria-current="page"] * {
            color: #ffffff !important;
            font-weight: 800 !important;
        }

        /* ── 5. UNIFIED POPOVER DROPDOWN CONTAINER (CLEAN WHITE CARD) ── */
        /* Streamlit 1.38 renders popovers in a portal at body level — must target broadly */
        [data-testid="stPopoverBody"],
        [data-testid="stPopoverContent"],
        [data-baseweb="popover"],
        [data-baseweb="popover"] > div,
        [data-baseweb="popover"] > div > div,
        [data-baseweb="menu"],
        ul[role="menu"] {
            background: #ffffff !important;
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #a7f3d0 !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.18) !important;
            padding: 0.5rem !important;
        }

        /* Force text dark inside popover body — but do NOT reset background-color
           (that would nuke any button gradients rendered inside the popover) */
        [data-testid="stPopoverBody"] p,
        [data-testid="stPopoverBody"] span,
        [data-testid="stPopoverBody"] label,
        [data-testid="stPopoverBody"] div,
        [data-testid="stPopoverContent"] p,
        [data-testid="stPopoverContent"] span,
        [data-testid="stPopoverContent"] label,
        [data-testid="stPopoverContent"] div,
        [data-baseweb="popover"] p,
        [data-baseweb="popover"] span,
        [data-baseweb="popover"] label {
            color: #0f172a !important;
        }

        /* Restore page link styling INSIDE popover */
        [data-testid="stPopoverBody"] .stPageLink > a,
        [data-testid="stPopoverContent"] .stPageLink > a,
        [data-baseweb="popover"] .stPageLink > a {
            background: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            padding: 0.5rem 1rem !important;
            color: #0f172a !important;
            display: flex !important;
            align-items: center !important;
            margin-bottom: 4px !important;
            font-weight: 600 !important;
            transition: all 0.15s ease !important;
        }

        [data-testid="stPopoverBody"] .stPageLink > a:hover,
        [data-testid="stPopoverContent"] .stPageLink > a:hover,
        [data-baseweb="popover"] .stPageLink > a:hover {
            background: #d1fae5 !important;
            border-color: #34d399 !important;
            color: #064e3b !important;
        }

        [data-testid="stPopoverBody"] .stPageLink > a[aria-current="page"],
        [data-testid="stPopoverContent"] .stPageLink > a[aria-current="page"],
        [data-baseweb="popover"] .stPageLink > a[aria-current="page"] {
            background: linear-gradient(135deg, #10b981, #06b6d4) !important;
            color: #ffffff !important;
            border-color: transparent !important;
        }

        [data-testid="stPopoverBody"] .stPageLink > a[aria-current="page"] *,
        [data-testid="stPopoverContent"] .stPageLink > a[aria-current="page"] *,
        [data-baseweb="popover"] .stPageLink > a[aria-current="page"] * {
            color: #ffffff !important;
        }

        /* ── DEVICE MEDIA QUERIES (DESKTOP VS MOBILE TOGGLING) ── */

        /* DESKTOP SCREENS (> 768px): Show Horizontal Navbar, Hide Hamburger Button */
        @media (min-width: 769px) {
            [data-testid="stHorizontalBlock"]:has(.mobile-nav-tag) {
                display: none !important;
            }
            [data-testid="stHorizontalBlock"]:has(.desktop-nav-tag) {
                display: flex !important;
            }
        }

        /* MOBILE SCREENS (<= 768px): Hide Horizontal Navbar, Show Hamburger Button */
        @media (max-width: 768px) {
            [data-testid="stHorizontalBlock"]:has(.desktop-nav-tag) {
                display: none !important;
            }
            [data-testid="stHorizontalBlock"]:has(.mobile-nav-tag) {
                display: flex !important;
            }

            .block-container {
                padding: 0.8rem 0.8rem 1.5rem !important;
            }

            .feat-grid, .use-case-grid {
                grid-template-columns: 1fr !important;
                gap: 0.8rem !important;
            }

            [data-testid="stHorizontalBlock"]:not(:has(.mobile-nav-tag)) [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }

            .hero-title {
                font-size: 2.2rem !important;
            }
            .hero-sub {
                font-size: 0.95rem !important;
            }
        }

        .nav-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #a7f3d0, transparent);
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # ── 1. DESKTOP HORIZONTAL NAVBAR (> 768px) ──
    d_col1, d_col2, d_col3, d_col4, d_col5, d_col6 = st.columns([2.2, 1, 1, 1, 1, 1])

    with d_col1:
        st.markdown("""
        <div class="desktop-nav-tag nav-brand-title">
            <span>🩺</span> MediRAG
            <span style="font-size:0.72rem; background:#d1fae5; color:#047857 !important; font-weight:700; padding:2px 8px; border-radius:99px; margin-left:4px;">BH Venture</span>
        </div>
        """, unsafe_allow_html=True)

    with d_col2:
        st.page_link("app.py", label="Home", icon="🏠")

    with d_col3:
        st.page_link("pages/1_Chatbot.py", label="Chatbot", icon="💬")

    with d_col4:
        st.page_link("pages/2_Upload_Documents.py", label="Upload Docs", icon="📤")

    with d_col5:
        st.page_link("pages/3_Analytics_&_Feedback.py", label="Analytics", icon="📊")

    with d_col6:
        st.page_link("pages/4_About.py", label="About", icon="ℹ️")

    # ── 2. MOBILE HAMBURGER MENU (<= 768px) ──
    m_col1, m_col2 = st.columns([1.6, 1])

    with m_col1:
        st.markdown("""
        <div class="mobile-nav-tag nav-brand-title" style="padding-top: 4px;">
            <span>🩺</span> MediRAG
            <span style="font-size:0.7rem; background:#d1fae5; color:#047857 !important; font-weight:700; padding:2px 8px; border-radius:99px; margin-left:4px;">BH Venture</span>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        with st.popover("☰ Menu", use_container_width=True):
            st.markdown("<div style='font-weight:700; color:#059669; font-size:0.82rem; margin-bottom:8px; text-transform:uppercase;'>Select Page:</div>", unsafe_allow_html=True)
            st.page_link("app.py", label="Home", icon="🏠", use_container_width=True)
            st.page_link("pages/1_Chatbot.py", label="Chatbot", icon="💬", use_container_width=True)
            st.page_link("pages/2_Upload_Documents.py", label="Upload Docs", icon="📤", use_container_width=True)
            st.page_link("pages/3_Analytics_&_Feedback.py", label="Analytics", icon="📊", use_container_width=True)
            st.page_link("pages/4_About.py", label="About Platform", icon="ℹ️", use_container_width=True)

    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
