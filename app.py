import streamlit as st
import streamlit.components.v1 as components
import time

# 1. SETUP & BRANDING
st.set_page_config(page_title="Pronto | Practice Revenue Autopsy", page_icon="📈", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #001e36; color: #ffffff; }
    .stNumberInput label { color: #ffffff !important; font-weight: 600; }
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
    </style>
    """, unsafe_allow_html=True)

st.image("https://assets.cdn.filesafe.space/MCcnQ0ytnakrb0FwnYIM/media/69ea1f539fe87a999456bbe3.png", width=220)
st.title("Practice Revenue Autopsy™")

# 2. INPUT SECTION
with st.container():
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
        
        # 7-SECOND DELAY
        with st.status("Analyzing Practice Vitals...", expanded=True) as status:
            time.sleep(2)
            st.write("Reviewing clinical benchmarks...")
            time.sleep(2)
            st.write("Isolating financial leaks...")
            time.sleep(3)
            status.update(label="Autopsy Complete!", state="complete", expanded=False)

        # 1) NEW MISSING FIELDS MESSAGE
        if any(v is None for v in inputs.values()):
            st.warning("Looks like some fields were skipped. That’s exactly how blind spots happen. Pronto eliminates the guesswork by giving you complete, real-time access to every metric that drives your practice...daily...automatically.")

        # 3. THE SILO ENGINE
        FINAL_RESULTS = {}
        REV_BASE = 1200000

        # EBITDA Silo
        if inputs['ebitda'] is not None:
            loss = ((22 - inputs['ebitda']) / 100 * REV_BASE) if inputs['ebitda'] < 22 else 0
            FINAL_RESULTS['EBITDA'] = {'loss': loss, 'status': "red" if inputs['ebitda'] < 22 else "green"}

        # NO SHOWS Silo
        if inputs['noshow'] is not None:
            loss = ((inputs['noshow'] - 5) / 100 * REV_BASE) if inputs['noshow'] > 5 else 0
            FINAL_RESULTS['No Shows'] = {'loss': loss, 'status': "red" if inputs['noshow'] > 5 else "green"}

        # INSURANCE Silo
        if inputs['ins'] is not None:
            loss = ((inputs['ins'] - 25) / 365 * 0.07 * REV_BASE) if inputs['ins'] > 25 else 0
            FINAL_RESULTS['Insurance'] = {'loss': loss, 'status': "red" if inputs['ins'] > 25 else "green"}

        # HIRING Silo
        if inputs['hire'] is not None:
            raw = ((inputs['hire'] - 4) * 5120) - 10000 if inputs['hire'] > 4 else 0
            FINAL_RESULTS['Hiring'] = {'loss': max(0, raw), 'status': "red" if inputs['hire'] > 4 else "green"}

        # PATIENT CONVERSION Silo
        if inputs['np'] is not None or inputs['conv'] is not None:
            curr_np = inputs['np'] if inputs['np'] is not None else 30
            curr_conv = inputs['conv'] if inputs['conv'] is not None else 80
            loss = ((80 - curr_conv) / 100 * curr_np * 1000 * 12) if curr_conv < 80 else 0
            FINAL_RESULTS['Patient Conversion'] = {'loss': loss, 'status': "red" if curr_conv < 80 else "green"}

        # HYGIENE SYSTEM Silo
        if inputs['hprod'] is not None or inputs['hperio'] is not None:
            curr_hprod = inputs['hprod'] if inputs['hprod'] is not None else 30
            hp_loss = ((30 - curr_hprod) / 100 * REV_BASE) if curr_hprod < 30 else 0
            curr_perio = inputs['hperio'] if inputs['hperio'] is not None else 40
            h_base = (curr_hprod / 100 * REV_BASE) if curr_hprod >= 30 else (0.30 * REV_BASE)
            perio_loss = ((40 - curr_perio) / 100 * h_base) if curr_perio < 40 else 0
            FINAL_RESULTS['Hygiene System'] = {'loss': hp_loss + perio_loss, 'status': "red" if (curr_hprod < 30 or curr_perio < 40) else "green"}

        # --- THE VERDICT ---
        if FINAL_RESULTS:
            failing = {k: v for k, v in FINAL_RESULTS.items() if v['status'] == "red"}
            
            if failing:
                winner_key = max(failing, key=lambda k: failing[k]['loss'])
                winner_loss = failing[winner_key]['loss']
            else:
                winner_key = "Practice Efficiency"
                winner_loss = 0

            st.markdown(f"""
            <div class="report-card">
                <h1 style="color: #ffffff; margin-top:0; font-size: 2.2rem;">The Verdict</h1>
                <p style="font-size: 1.3rem; margin-bottom: 20px;">Pronto discovered that your low hanging fruit is in <b>"{winner_key}"</b></p>
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

            # 3) NEW CTA FOR FULL AUTOPSY
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

            # 2) NEW DISCLAIMER (Right before form)
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
