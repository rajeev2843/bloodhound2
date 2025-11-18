import streamlit as st
from utils.styling import inject_custom_css, metric_card, risk_badge
from auth import logout_user
from database import get_session, Vendor, RiskLevel

st.set_page_config(page_title="Client Dashboard", page_icon="📊", layout="wide")
inject_custom_css()

# Protect Page
if not st.session_state.get('authenticated', False) or st.session_state.role != 'client':
    st.warning("Please login as a Client to view this page.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header(f"Welcome, Client")
    if st.button("Logout"):
        logout_user()

st.title("📊 Client Compliance Dashboard")

# Fetch Data (Mock logic for now - connect to DB in production)
db = get_session()
# In real app: vendors = db.query(Vendor).filter(Vendor.entity_id == st.session_state.entity_id).all()
# For demo, we'll just show UI
total_vendors = 12
critical_vendors = 2
high_risk = 3
total_itc = 1500000

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Total Vendors", total_vendors, icon="👥")
with col2:
    metric_card("Critical Risks", critical_vendors, delta="-1", icon="🚨")
with col3:
    metric_card("High Risks", high_risk, delta="+2", icon="⚠️")
with col4:
    metric_card("ITC at Risk", "₹15.0 L", icon="💰")

st.divider()

st.subheader("📡 Real-Time Risk Monitor")
# Placeholder for table
st.info("Connect Tally or Upload CSV to see live vendor data.")
