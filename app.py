import streamlit as st
import os
import json
from pathlib import Path

# --- FOOLPROOF PRODUCTION AUTHENTICATION ENGINE ---
# This automatically converts your raw Render JSON string into a secure Streamlit file before the app initializes
if "SERVICE_ACCOUNT_JSON" in os.environ:
    try:
        # Parse the raw JSON to ensure validity
        creds = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
        
        # Format the values exactly as the Streamlit connection expectations require
        secrets_content = f"""
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/1Md6YCNDA3arJy2jVRunjOySjxNK9_FHtcGRtqoVe5J4/edit?gid=0#gid=0"
type = "{creds.get('type', 'service_account')}"
project_id = "{creds.get('project_id', '')}"
private_key_id = "{creds.get('private_key_id', '')}"
private_key = "{creds.get('private_key', '').replace('\n', '\\n')}"
client_email = "{creds.get('client_email', '')}"
client_id = "{creds.get('client_id', '')}"
auth_uri = "{creds.get('auth_uri', 'https://accounts.google.com/o/oauth2/auth')}"
token_uri = "{creds.get('token_uri', 'https://oauth2.googleapis.com/token')}"
auth_provider_x509_cert_url = "{creds.get('auth_provider_x509_cert_url', 'https://www.googleapis.com/oauth2/v1/certs')}"
client_x509_cert_url = "{creds.get('client_x509_cert_url', '')}"
"""
        # Ensure the .streamlit folder exists on Render and write the file
        Path(".streamlit").mkdir(exist_ok=True)
        with open(".streamlit/secrets.toml", "w") as f:
            f.write(secrets_content)
    except Exception as e:
        st.error(f"Failed to generate runtime credentials file: {e}")

# Now import the connection engine securely
from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components
import pandas as pd
import time
from datetime import datetime

# 1. SETUP & BRANDING
st.set_page_config(page_title="Pronto | Practice Revenue Autopsy", page_icon="📈", layout="centered")

# Establish Google Sheets Connection (Reads the file generated above natively)
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
    
    /* Custom White Text Warning Box Style */
    .custom-warning-box {
        background-color: rgba(255, 140, 0, 0.1) !important;
        border: 1px solid rgba(255, 140, 0, 0.4) !important;
        border-left: 5px solid #ff8c00 !important;
        padding: 15px 20px !important;
        border-radius: 6px !important;
        margin-bottom: 25px !important;
    }
    .custom-warning-box p {
        color: #ffffff !important;
        margin: 0 !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Swapped with your new logo URL here:
st.image("https://assets.cdn.filesafe.space/2TCpScjx7MU1ZqFgoQKY/media/6a45138ddc5f2c22a2815e0c.png", width=220)
st.title("Practice Revenue Autopsy™")

# 2. INPUT SECTION
with st.container():
    practice_name = st.text_input("Practice Name", placeholder="Enter the name of your practice...")
    
    col1, col2 = st.columns(2)
    inputs = {}
    with col1:
        inputs['ebitda'] = st.number_input("Current EBITDA %", min_value=0, max_value=100, value=None, step=1)
        inputs['hprod'] = st.number_input("Hygiene Production %", min_value=0, max_value=100, value=None, step=1)
        inputs['ins'] = st.number_input("Days to Collect from Ins", min_value=0, value=None, step=1)
        inputs['hire'] = st.number_input("Avg Weeks to Hire a Hygienist", min_value=0, value=None, step=1)
    with col2:
        inputs['noshow'] = st.number_input("No Show %", min_value=0, max_value=100, value=None, step=1)
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

        # Replaced native st.warning with custom HTML warning container to force white text
        if any(v is None for v in inputs.values()):
            st.markdown("""
                <div class="custom-warning-box">
                    <p>⚠️ Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.</p>
                </div>
            """, unsafe_allow_html=True)

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
            loss = ((inputs['ins'] - 25) / 365 * 0.07 * REV_BASE) if inputs['ins'] > 25 else 0
            FINAL_RESULTS['Insurance'] = {'loss': loss, 'status': "red" if inputs['ins'] > 25 else "green"}

        if inputs['hire'] is not None:
            raw = ((inputs['hire'] - 4) * 5120) - 10000 if inputs['hire'] > 4 else 0
            FINAL_RESULTS['Hiring'] = {'loss': max(0, raw), 'status': "red" if inputs['hire'] > 4 else "green"}

        if inputs['np'] is not None or inputs['conv'] is not None:
            curr_np = inputs['np'] if inputs['np'] is not None else 30
            curr_conv = inputs['conv'] if inputs['conv'] is not None else 80
            loss = ((80 - curr_conv) / 100 * curr_np * 1000 * 12) if curr_conv < 80 else 0
            FINAL_RESULTS['Patient Conversion'] = {'loss': loss, 'status': "red" if curr_conv < 80 else "green"}

        if inputs['hprod'] is not None or inputs['hperio'] is not None:
            curr_hprod = inputs['hprod'] if inputs['hprod'] is not None else 30
            hp_loss = ((30 - curr_hprod) / 100 * REV_BASE) if curr_hprod < 30 else 0
            curr_perio = inputs['hperio'] if inputs['hperio'] is not None else 40
            h_base = (curr_hprod / 100 * REV_BASE) if curr_hprod >= 30 else (0.30 * REV_BASE)
            perio_loss = ((40 - curr_perio) / 100 * h_base) if curr_perio < 40 else 0
            FINAL_RESULTS['Hygiene System'] = {'loss': hp_loss + perio_loss, 'status': "red" if (curr_hprod < 30 or curr_perio < 40) else "green"}

        if FINAL_RESULTS:
            failing = {k: v for k, v in FINAL_RESULTS.items() if v['status'] == "red"}
            if failing:
                winner_key = max(failing, key=lambda k: failing[k]['loss'])
                winner_loss = failing[winner_key]['loss']
            else:
                winner_key = "Practice Efficiency"
                winner_loss = 0

            # --- DATA LOGGING ---
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Practice Name": practice_name if practice_name else "N/A",
                "Winner Key": winner_key,
                "Winner Loss": winner_loss,
                "EBITDA": inputs['ebitda'],
                "No Shows": inputs['noshow'],
                "Insurance": inputs['ins'],
                "Hiring": inputs['hire'],
                "Hygiene Prod": inputs['hprod'],
                "Hygiene Perio": inputs['hperio'],
                "NP Month": inputs['np'],
                "NP Conv": inputs['conv']
            }])

            try:
                # Target the spreadsheet explicitly by its URL
                spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Md6YCNDA3arJy2jVRunjOySjxNK9_FHtcGRtqoVe5J4/edit?gid=0#gid=0"
                existing_df = conn.read(spreadsheet=spreadsheet_url, ttl=0)
                existing_df = existing_df.dropna(how='all')
                updated_df = pd.concat([existing_df, new_data], ignore_index=True)
                conn.update(data=updated_df, spreadsheet=spreadsheet_url)
            except Exception as e:
                st.error(f"Spreadsheet log failed: {e}")

            # --- THE VERDICT UI ---
            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0; font-size: 2.2rem;">The Verdict</h1>
                <p style="font-size: 1.3rem; margin-bottom: 20px;">Pronto discovered that <b>{practice_name if practice_name else 'your practice'}'s</b> low hanging fruit is in <b>"{winner_key}"</b></p>
                <p style="font-size: 1.2rem; color: #00d2ff; font-weight: bold; margin-bottom: 25px;">
                    Based on 1.2 million in production, your practice is leaving <span style="color: #ff4500;">${winner_loss:,.0f}</span> on the table annually.
                </p>
                <p style="font-size: 1rem; line-height: 1.6; color: #cccccc;">
                    To get a more detailed analysis and autopsy of your personal results, please fill out the following 
                    and we will elaborate on the "{winner_key}" results as well as the others and let you know what can be done about it.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="status-container">', unsafe_allow_html=True)
            for label, data in FINAL_RESULTS.items():
                st.markdown(f'<div class="status-box status-{data["status"]}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
                <h2 style="color: #ff8c00;">“You just got a glimpse.</h2>
                <p style="font-size: 1.2rem; font-weight: bold;">Now let’s find what you’re actually missing.</p>
                <p style="font-size: 1.1rem; line-height: 1.5;">
                    Fill out the form below to unlock your full Practice Autopsy—breaking down exactly where revenue is leaking across all 6 categories.<br><br>
                    <b>Because if this much showed up from a few inputs…</b><br>
                    what do you think happens when you’re tracking 140+ metrics in real time?
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="disclaimer-box">
                These results aren’t meant to be perfect—they’re meant to be revealing. 
                We’ve taken your inputs and applied industry benchmarks to surface likely gaps. 
                But without real-time data integration, there are variables we simply can’t see. 
                Pronto doesn’t guess. It knows. This is the preview… not the movie.
            </div>
            """, unsafe_allow_html=True)

            # 5. GHL FORM
            components.html("""
                <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
                <script src="https://link.msgsndr.com/js/form_embed.js"></script>
            """, height=650)
