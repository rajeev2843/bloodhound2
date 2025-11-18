import streamlit as st
from auth import signin_user, signup_user, login_user
from utils.styling import inject_custom_css

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered", initial_sidebar_state="collapsed")
inject_custom_css()

# HIDE SIDEBAR CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.title("🔐 Authentication")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    email = st.text_input("Email", key="l_email")
    password = st.text_input("Password", type="password", key="l_pass")
    
    if st.button("Login", use_container_width=True):
        # Ensure auth.py returns 5 values as per previous code
        success, uid, role, eid, msg = signin_user(email, password)
        
        if success:
            login_user(uid, role, eid)
            st.success("Success! Redirecting...")
            
            # REDIRECT LOGIC
            if role == 'client':
                st.switch_page("pages/03_Client_Dashboard.py")
            else:
                st.switch_page("pages/04_CA_Dashboard.py")
        else:
            st.error(msg)

with tab2:
    # ... (Keep your existing Signup logic, just ensure no st.switch_page calls are broken)
    st.write("Sign up form here...") 
