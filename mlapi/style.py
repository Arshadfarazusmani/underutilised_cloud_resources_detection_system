# style.py
import streamlit as st

def inject_tailwind_style():
    st.markdown("""
    <style>

    /* ==== FONT (inter) ==== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* ==== MAIN LAYOUT ==== */
    .main {
        background: linear-gradient(135deg, #f9fafb, #eef2ff);
    }

    /* ==== TITLE ==== */
    h1, h2, h3, h4 {
        font-weight: 600;
        color: #1e293b;
    }

    /* ==== GLASS CARD ==== */
    .glass-card {
        background: rgba(255,255,255,0.55);
        padding: 25px;
        border-radius: 18px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* ==== BUTTONS (Tailwind-like) ==== */
    .stButton > button {
        background: #6366f1;
        color: white;
        padding: 10px 18px;
        border-radius: 12px;
        border: none;
        font-weight: 500;
        transition: 0.2s ease-in-out;
        font-size: 16px;
    }

    .stButton > button:hover {
        background: #4f46e5;
        transform: scale(1.03);
    }

    /* ==== INPUT FIELDS ==== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 12px !important;
        border: 1px solid #d1d5db !important;
        padding: 8px 12px !important;
    }

    /* ==== METRIC BOXES ==== */
    .stMetric {
        background: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* ==== DATAFRAME ==== */
    .dataframe {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }

    </style>
    """, unsafe_allow_html=True)
