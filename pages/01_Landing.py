import streamlit as st
from utils.styling import inject_custom_css

st.set_page_config(page_title="Welcome", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")
inject_custom_css()

# HIDE SIDEBAR CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div style='text-align: center; padding: 40px 20px;'>
        <h1 style='font-size: 4rem; color: #1E88E5; margin-bottom: 10px;'>Transaction Bloodhound</h1>
        <p style='font-size: 1.5rem; color: #555;'>The Future of Supply Chain Assurance & GST Compliance</p>
    </div>
""", unsafe_allow_html=True)

# Value Props (Top)
c1, c2, c3 = st.columns(3)
with c1:
    st.info("🚀 **For Entities**\n\nAutomated ITC protection & Shell company detection.")
with c2:
    st.info("⚖️ **For CAs**\n\n'God View' Dashboard & Automated Reconciliation.")
with c3:
    st.info("⚡ **Live Data**\n\nReal-time GSTN, MCA, and IBBI checks.")

st.divider()

# Feature Details (Scrollable content)
st.markdown("### 🔍 Why Choose Bloodhound?")
st.write("We integrate directly with government portals to ensure you never claim ITC from a fraudulent vendor.")
# (You can add more text here to make the page longer so they have to scroll)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Sign In Button (Bottom)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### Ready to secure your supply chain?")
    if st.button("🔐 Login / Sign Up Now", type="primary", use_container_width=True):
        st.switch_page("pages/02_Login.py")
        
