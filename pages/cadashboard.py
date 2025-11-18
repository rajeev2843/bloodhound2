import streamlit as st
from utils.styling import inject_custom_css, metric_card
from auth import logout_user

st.set_page_config(page_title="CA Console", page_icon="⚖️", layout="wide")
inject_custom_css()

# Protect Page
if not st.session_state.get('authenticated', False) or st.session_state.role != 'ca':
    st.warning("Please login as a CA to view this page.")
    st.stop()

with st.sidebar:
    st.header("CA Console")
    if st.button("Logout"):
        logout_user()

st.title("⚖️ CA Practice 'God View'")

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Total Clients", "15", icon="🏢")
with col2:
    metric_card("Pending Alerts", "8", icon="🔔")
with col3:
    metric_card("Total Billable Hours", "42.5", icon="⏱️")

st.divider()

st.subheader("📋 Client Portfolio Status")

# Mock Table
client_data = [
    {"Client": "ABC Pvt Ltd", "Risk": "Critical", "ITC Risk": "₹12L", "Last Audit": "2 Days ago"},
    {"Client": "XYZ Traders", "Risk": "Low", "ITC Risk": "₹0", "Last Audit": "Today"},
]

st.table(client_data)
