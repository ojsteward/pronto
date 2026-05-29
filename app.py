import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components
import pandas as pd
import time
from datetime import datetime

# 1. SETUP & BRANDING
st.set_page_config(page_title="Pronto | Practice Revenue Autopsy", page_icon="📈", layout="centered")

# Establish Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("""
    <style>
    .stApp { background-color: #001e36; color: #ffffff; }
    .stNumberInput label, .stTextInput label { color: #ffffff !important; font-weight: 600; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff8c00 0%, #ff4500 100%);
        color: white; border: none; padding: 18px 30px; border-radius: 8px;
        font-weight: 800; width: 100%; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .report-card { background: rgba(255, 255, 255, 0.05); padding: 35px; border-radius: 15px; border: 2px solid #00d2ff; text-align: center; margin-bottom: 30px; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
    .status-box { padding: 15px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.8rem; border: 2px solid transparent; text-transform: uppercase; }
    .status-green { border-color: #28a745; background: rgba(40, 167, 69, 0.1); color: #28a745; }
    .status-red { border-color: #dc3545; background: rgba(220, 53, 69, 0.1); color: #dc3545; }
    .disclaimer-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 8px; border-left: 4px solid #ff8c00; margin-top: 20px; font-style: italic; font-size: 0.9rem; }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Strips system colors from internal notification caches and forces white text */
    div[data-testid="stNotification"], 
    div[data-testid="stNotification"] *,
    div[data-testid="stNotification"] p,
    div[data-testid="stNotification"] div { 
        color: #ffffff !important;
        background-color: transparent !important;
    }
    
    /* Re-establishes a clean subtle background for the warning alert box itself */
    div[data-testid="stNotification"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 140, 0, 0.3) !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.image("https://assets.cdn.filesafe.space/MCcnQ0ytnakrb0FwnYIM/media/69ea1f539fe87a999456bbe3.png", width=220)
st.title("Practice Revenue Autopsy™")

# 2. INPUT SECTION
with st.container():
    practice_name = st.text_input("Practice Name", placeholder="Enter the name of your practice...")
    
    col1, col2 = st.columns(2)
    inputs = {}
    with col1:
        inputs['ebitda'] = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1)
        inputs['noshow'] = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1)
        inputs['ins'] = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1)
        inputs['hire'] = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1)
    with col2:
        inputs['hprod'] = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1)
        inputs['hperio'] = st.number_input("Hygiene Perio %", min_value=0, max_value=100, value=None, step=1)
        inputs['np'] = st.number_input("# New Patients per Month", min_value=0, value=None, step=1)
        inputs['conv'] = st.number_input("% of Calls Converted to NP", min_value=0, max_value=100, value=None, step=1)

    if st.button("Generate Autopsy Results"):
        
        with st.status("Analyzing Practice Vitals...", expanded=True) as status:
            time.sleep(2)
            st.write("Reviewing clinical benchmarks...")
            time.sleep(2)
            st.write("Isolating financial leaks...")
            time.sleep(3)
            status.update(label="Autopsy Complete!", state="complete", expanded=False)

        if any(v is None for v in inputs.values()):
            st.warning("Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.")

        # 3. THE SILO ENGINE
        FINAL_RESULTS = {}
        REV_BASE = 1200000

        if inputs['ebitda'] is not None:
            loss = ((22 - inputs['ebitda']) / 100 * REV_BASE) if inputs['ebitda'] < 22 else 0
            FINAL_RESULTS['EBITDA'] = {'loss': loss, 'status': "red" if inputs['ebitda'] < 22 else "green"}

        if inputs['noshow'] is not None:
            loss = ((inputs['noshow'] - 5) / 100 * REV_BASE) if inputs['noshow'] > 5 else 0
            FINAL_RESULTS['No Shows'] = {'loss': loss, 'status': "red" if inputs['noshow'] > 5 else "green"}

        if inputs['ins'] is not None:
            loss = ((inputs['ins'] - 25) / 365 * 0.07 * REV_BASE) if inputs['ins'] > 2
