import streamlit as st
from utils.styling import inject_custom_css, custom_button

st.set_page_config(page_title="Transaction Bloodhound", page_icon="🔍", layout="wide")
inject_custom_css()

# Hero Section
st.markdown("""
    <div style='text-align: center; padding: 50px 20px;'>
        <h1 style='font-size: 3.5rem; color: #1E88E5; margin-bottom: 10px;'>🔍 Transaction Bloodhound</h1>
        <p style='font-size: 1.5rem; color: #555;'>The Future of Supply Chain Assurance & GST Compliance</p>
        <br>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ### 🛑 Stop GST Fraud Before It Happens
    Transaction Bloodhound connects **Tally**, **GSTN**, and **MCA** data to give you a 360-degree live view of your vendor compliance.
    """)
    
    st.markdown("---")
    
    if st.button("🔐 Login / Sign Up", type="primary", use_container_width=True):
        st.switch_page("pages/2_🔐_Login.py")

# Features Grid
st.markdown("<br><br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🚀 For Entities")
    st.info("""
    - Automated ITC protection
    - Shell company detection
    - Real-time Vendor Risk Scores
    """)

with c2:
    st.markdown("### ⚖️ For CAs")
    st.info("""
    - 'God View' Dashboard for all clients
    - Automated GSTR-2B Reconciliation
    - Service Billing & Time Tracking
    """)

with c3:
    st.markdown("### ⚡ Live Data")
    st.info("""
    - Live GSTN Status Checks
    - MCA Director Network Analysis
    - IBBI Insolvency Checks
    """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>Built for ICAI Aurathon 2025</div>", unsafe_allow_html=True)
