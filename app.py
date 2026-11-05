import streamlit as st
import os
import json
from pathlib import Path
from datetime import datetime
import zoneinfo

# --- FOOLPROOF PRODUCTION AUTHENTICATION ENGINE ---
if "SERVICE_ACCOUNT_JSON" in os.environ:
    try:
        creds = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
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
        Path(".streamlit").mkdir(exist_ok=True)
        with open(".streamlit/secrets.toml", "w") as f:
            f.write(secrets_content)
    except Exception as e:
        st.error(f"Failed to generate runtime credentials file: {e}")

from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components
import pandas as pd
import time

# 1. SETUP & BRANDING
st.set_page_config(page_title="Pronto | Profit Diagnostic Report", page_icon="📈", layout="centered")

conn = st.connection("gsheets", type=GSheetsConnection)

# --- DAILY EST REFRESH SEQUENCE ---
@st.cache_data(ttl=3600)  
def trigger_daily_startup_est():
    est_tz = zoneinfo.ZoneInfo("America/New_York")
    now_est = datetime.now(est_tz)
    return now_est.strftime("%Y-%m-%d")

current_day_est = trigger_daily_startup_est()

st.markdown("""
    <style>
    .stApp { background-color: #001e36; color: #ffffff; }
    .stNumberInput label, .stTextInput label { color: #ffffff !important; font-weight: 600; }
    
    /* Clean White Text Legend Layout Dividers */
    .app-section-legend {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 45px;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff8c00 0%, #ff4500 100%);
        color: white; border: none; padding: 18px 30px; border-radius: 8px;
        font-weight: 800; width: 100%; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .report-card { background: rgba(255, 255, 255, 0.05); padding: 35px; border-radius: 15px; border: 2px solid #00d2ff; text-align: center; margin-bottom: 30px; }
    
    /* Grid Box Styling Update for Inline Support */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 35px; }
    .status-box { padding: 20px; border-radius: 8px; text-align: center; border: 2px solid transparent; }
    .status-title { font-weight: bold; font-size: 1rem; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px; }
    .status-desc { font-size: 0.85rem; font-weight: normal; line-height: 1.4; opacity: 0.95; }
    
    .status-green { border-color: #28a745; background: rgba(40, 167, 69, 0.15); color: #4ade80; }
    .status-red { border-color: #dc3545; background: rgba(220, 53, 69, 0.15); color: #fca5a5; }
    .status-yellow { border-color: #eab308; background: rgba(234, 179, 8, 0.15); color: #fde047; }

    /* Book a meeting call to action */
    .book-cta-wrap { text-align: center; margin: 20px 0 30px 0; }
    .book-cta {
        display: inline-block;
        background: linear-gradient(90deg, #ff8c00 0%, #ff4500 100%);
        color: #ffffff !important; text-decoration: none !important;
        padding: 16px 34px; border-radius: 8px;
        font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
    }
    .book-cta:hover { opacity: 0.9; }
    
    /* Color Meaning Legend Above Matrix */
    .color-legend { display: flex; justify-content: center; gap: 30px; margin-bottom: 15px; font-size: 0.95rem; }
    .legend-item { display: flex; align-items: center; gap: 8px; }
    
    .disclaimer-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 8px; border-left: 4px solid #ff8c00; margin-top: 20px; font-style: italic; font-size: 0.9rem; }
    
    .custom-warning-box {
        background-color: rgba(255, 140, 0, 0.1) !important;
        border: 1px solid rgba(255, 140, 0, 0.4) !important;
        border-left: 5px solid #ff8c00 !important;
        padding: 15px 20px !important;
        border-radius: 6px !important;
        margin-bottom: 25px !important;
    }
    .custom-warning-box p { color: #ffffff !important; margin: 0 !important; font-size: 0.95rem !important; line-height: 1.5 !important; }
    
    .ghl-divider { border: 0; height: 2px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent); margin: 40px 0; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Updated Logo Link
st.image("https://assets.cdn.filesafe.space/2TCpScjx7MU1ZqFgoQKY/media/6a45138ddc5f2c22a2815e0c.png", width=220)
st.title("Profit Diagnostic Report")

# --- REPORT VERSION ---
# ?v=1 : short version (category benchmarks first, verdict second, booking is the only call to action)
# ?v=2 : original full report with a "Book a Meeting" button at the top (default)
BOOKING_URL = "https://b.prontodental.com/widget/booking/sisg5S7Kz2VOsXHU4aAr"
REPORT_VERSION = str(st.query_params.get("v", "2")).strip()
if REPORT_VERSION not in ("1", "2"):
    REPORT_VERSION = "2"

def book_button(label="Book a Meeting"):
    st.markdown(f"""
        <div class="book-cta-wrap">
            <a class="book-cta" href="{BOOKING_URL}" target="_blank">{label}</a>
        </div>
    """, unsafe_allow_html=True)

if REPORT_VERSION == "2":
    book_button("Book a Meeting")

# 2. INPUT SECTION (Original layout untouched)
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

    if st.button("Generate Diagnostic Results"):
        
        # Animated Loading Sequence
        with st.status("Initializing Systems...", expanded=True) as status:
            with st.spinner("Reviewing clinical benchmarks..."):
                time.sleep(1.5)
            with st.spinner("Isolating financial leaks..."):
                time.sleep(1.5)
            with st.spinner("Crunching final diagnostics..."):
                time.sleep(1.5)
            status.update(label="Diagnostic Complete! Rendering Layout Visuals...", state="running", expanded=True)
            
            # Additional loading animation step while interface components are constructed below
            with st.spinner("Compiling report analytics database elements..."):
                time.sleep(2.0)
            status.update(label="Complete!", state="complete", expanded=False)

        if any(v is None for v in inputs.values()):
            st.markdown("""
                <div class="custom-warning-box">
                    <p>⚠️ Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.</p>
                </div>
            """, unsafe_allow_html=True)

        # 3. THE SILO ENGINE
        # green = at or better than benchmark, yellow = close to benchmark (not too good), red = well below benchmark
        def band(is_green, is_yellow):
            return "green" if is_green else ("yellow" if is_yellow else "red")

        FINAL_RESULTS = {}
        REV_BASE = 1200000

        if inputs['ebitda'] is not None:
            loss = ((22 - inputs['ebitda']) / 100 * REV_BASE) if inputs['ebitda'] < 22 else 0
            FINAL_RESULTS['EBITDA'] = {'loss': loss, 'status': band(inputs['ebitda'] >= 22, inputs['ebitda'] >= 18)}

        if inputs['noshow'] is not None:
            loss = ((inputs['noshow'] - 5) / 100 * REV_BASE) if inputs['noshow'] > 5 else 0
            FINAL_RESULTS['No Shows'] = {'loss': loss, 'status': band(inputs['noshow'] <= 5, inputs['noshow'] <= 8)}

        if inputs['ins'] is not None:
            loss = ((inputs['ins'] - 25) / 365 * 0.07 * REV_BASE) if inputs['ins'] > 25 else 0
            FINAL_RESULTS['Insurance'] = {'loss': loss, 'status': band(inputs['ins'] <= 25, inputs['ins'] <= 35)}

        if inputs['hire'] is not None:
            raw = ((inputs['hire'] - 4) * 5120) - 10000 if inputs['hire'] > 4 else 0
            FINAL_RESULTS['Hiring'] = {'loss': max(0, raw), 'status': band(inputs['hire'] <= 4, inputs['hire'] <= 6)}

        if inputs['np'] is not None or inputs['conv'] is not None:
            curr_np = inputs['np'] if inputs['np'] is not None else 30
            curr_conv = inputs['conv'] if inputs['conv'] is not None else 80
            loss = ((80 - curr_conv) / 100 * curr_np * 1000 * 12) if curr_conv < 80 else 0
            FINAL_RESULTS['Patient Conversion'] = {'loss': loss, 'status': band(curr_conv >= 80, curr_conv >= 70)}

        if inputs['hprod'] is not None or inputs['hperio'] is not None:
            curr_hprod = inputs['hprod'] if inputs['hprod'] is not None else 30
            hp_loss = ((30 - curr_hprod) / 100 * REV_BASE) if curr_hprod < 30 else 0
            curr_perio = inputs['hperio'] if inputs['hperio'] is not None else 40
            h_base = (curr_hprod / 100 * REV_BASE) if curr_hprod >= 30 else (0.30 * REV_BASE)
            perio_loss = ((40 - curr_perio) / 100 * h_base) if curr_perio < 40 else 0
            FINAL_RESULTS['Hygiene System'] = {'loss': hp_loss + perio_loss, 'status': band(curr_hprod >= 30 and curr_perio >= 40, curr_hprod >= 25 and curr_perio >= 35)}

        if FINAL_RESULTS:
            failing = {k: v for k, v in FINAL_RESULTS.items() if v['status'] != "green"}
            if failing:
                winner_key = max(failing, key=lambda k: failing[k]['loss'])
                winner_loss = failing[winner_key]['loss']
            else:
                winner_key = "Practice Efficiency"
                winner_loss = 0

            # --- DATA LOGGING (EXACT ORIGINAL FORMAT MATCH) ---
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
                spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Md6YCNDA3arJy2jVRunjOySjxNK9_FHtcGRtqoVe5J4/edit?gid=0#gid=0"
                existing_df = conn.read(spreadsheet=spreadsheet_url, ttl=0)
                existing_df = existing_df.dropna(how='all')
                updated_df = pd.concat([existing_df, new_data], ignore_index=True)
                conn.update(data=updated_df, spreadsheet=spreadsheet_url)
            except Exception as e:
                st.error(f"Spreadsheet log failed: {e}")

            # --- CATEGORY STATUS (green / yellow / red) ---
            CATEGORY_INPUTS = {
                'EBITDA': ['ebitda'],
                'No Shows': ['noshow'],
                'Insurance': ['ins'],
                'Hiring': ['hire'],
                'Patient Conversion': ['np', 'conv'],
                'Hygiene System': ['hprod', 'hperio'],
            }

            def render_verdict(v1=False):
                st.markdown('<div class="app-section-legend">Primary Diagnostic</div>', unsafe_allow_html=True)
                if v1:
                    closing = """
                        <p style="font-size: 1rem; line-height: 1.6; color: #cccccc;">
                            Book a call with our team and we will walk you through these numbers and what can be done about them.
                        </p>
                    """
                else:
                    closing = f"""
                        <p style="font-size: 1rem; line-height: 1.6; color: #cccccc;">
                            To get a more detailed diagnostic, please set up a discovery call and we will elaborate on the numbers and let you know what can be done about it.
                        </p>
                        <p style="font-size: 1.1rem; margin-top: 15px;">
                            <a href="{BOOKING_URL}" target="_blank" style="color: #00d2ff; font-weight: bold;">Click Here</a>
                        </p>
                    """
                st.markdown(f"""
                <div class="report-card">
                    <h1 style="color: #ffffff; margin-top:0; font-size: 2.2rem;">The Verdict</h1>
                    <p style="font-size: 1.3rem; margin-bottom: 20px;">Pronto discovered that <b>{practice_name if practice_name else 'your practice'}'s</b> low hanging fruit is in <b>"{winner_key}"</b></p>
                    <p style="font-size: 1.2rem; color: #00d2ff; font-weight: bold; margin-bottom: 25px;">
                        Based on 1.2 million in production, your practice is leaving <span style="color: #ff4500;">${winner_loss:,.0f}</span> on the table annually.
                    </p>
                    {closing}
                </div>
                """, unsafe_allow_html=True)
                if v1:
                    book_button("Book Your Appointment")

            def render_benchmarks():
                st.markdown('<div class="app-section-legend">Category Benchmarks</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="color-legend" style="flex-wrap: wrap;">
                    <div class="legend-item"><span style="color: #4ade80; font-weight: bold;">🟢 Green:</span> Meeting or exceeding healthy industry benchmarks.</div>
                    <div class="legend-item"><span style="color: #fde047; font-weight: bold;">🟡 Yellow:</span> Close to benchmark, but not where it should be; money is slipping through.</div>
                    <div class="legend-item"><span style="color: #fca5a5; font-weight: bold;">🔴 Red:</span> Below benchmark; hidden operational revenue leaks present.</div>
                </div>
                """, unsafe_allow_html=True)

                boxes = {
                    "green": ("status-green", "🟢", "Congratulations, your numbers are Great"),
                    "yellow": ("status-yellow", "🟡", "Not bad, but not great either. There is still money to recover here"),
                    "red": ("status-red", "🔴", "Urgent attention needed. This is a tremendous opportunity to fix this"),
                }
                st.markdown('<div class="status-container">', unsafe_allow_html=True)
                for label, data in FINAL_RESULTS.items():
                    css, icon, desc = boxes[data["status"]]
                    st.markdown(f"""
                    <div class="status-box {css}">
                        <div class="status-title">{icon} {label}</div>
                        <div class="status-desc">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if REPORT_VERSION == "1":
                # VERSION 1: benchmarks first, then the verdict, booking is the only call to action
                render_benchmarks()
                render_verdict(v1=True)
            else:
                # VERSION 2: original full report (Book a Meeting button is shown at the top of the page)
                render_verdict(v1=False)
                render_benchmarks()

                # --- LEGEND: PERFORMANCE INSIGHTS ---
                st.markdown('<div class="app-section-legend">Performance Insights</div>', unsafe_allow_html=True)

                st.markdown(f"""
                <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                    <h2 style="color: #ff8c00;">“You just got a glimpse.</h2>
                    <p style="font-size: 1.2rem; font-weight: bold;">Now let’s find what you’re actually missing.</p>
                    <p style="font-size: 1.1rem; line-height: 1.5;">
                        Fill out the form below to unlock your full Practice Diagnostic—breaking down exactly where revenue is leaking across all 6 categories.<br><br>
                        <b>Because if this much showed up from a few inputs…</b><br>
                        what do you think happens when you’re tracking 140+ metrics in real time?
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # --- LEGEND: STRUCTURAL LIMITATIONS ---
                st.markdown('<div class="app-section-legend">Data Statement</div>', unsafe_allow_html=True)

                st.markdown("""
                <div class="disclaimer-box">
                    These results aren’t meant to be perfect—they’re meant to be revealing. 
                    We’ve taken your inputs and applied industry benchmarks to surface likely gaps. 
                    But without real-time data integration, there are variables we simply can’t see. 
                    Pronto doesn’t guess. It knows. This is the preview… not the movie.
                </div>
                """, unsafe_allow_html=True)

                # Divider line element
                st.markdown('<hr class="ghl-divider">', unsafe_allow_html=True)

                # --- LEGEND: APPLICATION FORM ---
                st.markdown('<div class="app-section-legend">Deep-Dive Access</div>', unsafe_allow_html=True)

                # 5. GHL FORM
                components.html("""
                    <iframe src="https://api.leadconnectorhq.com/widget/form/iVFg0wteKeXMSEXviPvh" style="width:100%;height:600px;border:none;border-radius:8px"></iframe>
                    <script src="https://link.msgsndr.com/js/form_embed.js"></script>
                """, height=650)
