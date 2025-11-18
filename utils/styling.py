import streamlit as st

# Custom CSS for modern look
def inject_custom_css():
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Main container */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* Card styling */
        .stCard {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            margin-bottom: 20px;
            border: 1px solid #e0e0e0;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(30, 136, 229, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(30, 136, 229, 0.4);
        }
        
        /* Metric cards */
        [data-testid="stMetric"] {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
        }
        
        /* Alert boxes */
        .stAlert {
            border-radius: 8px;
            border-left: 4px solid;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            padding: 10px;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus {
            border-color: #1E88E5;
            box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        
        /* Success/Error/Warning boxes */
        .stSuccess {
            background: #E8F5E9;
            border-left-color: #4CAF50;
        }
        
        .stError {
            background: #FFEBEE;
            border-left-color: #F44336;
        }
        
        .stWarning {
            background: #FFF3E0;
            border-left-color: #FF9800;
        }
        
        .stInfo {
            background: #E3F2FD;
            border-left-color: #2196F3;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        </style>
    """, unsafe_allow_html=True)

# Modern metric card (Fixed to prevent crashes)
def metric_card(label, value, delta=None, icon="📊"):
    delta_html = ""
    if delta:
        # Safe check for string vs number
        is_positive = False
        try:
            if isinstance(delta, str):
                # If it has a "+", it's positive/green
                is_positive = "+" in delta
            elif isinstance(delta, (int, float)):
                # If it's a number > 0, it's positive/green
                is_positive = delta > 0
        except:
            is_positive = False # Fallback

        # Green for positive, Red for negative
        color = "#4CAF50" if is_positive else "#F44336"
        
        delta_html = f'<div style="color: {color}; font-size: 14px; margin-top: 5px;">{delta}</div>'
    
    st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
            <div style="color: #666; font-size: 14px; margin-bottom: 5px;">{label}</div>
            <div style="font-size: 28px; font-weight: 700; color: #1E88E5;">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

# Modern button
def custom_button(label, key=None, icon="🔘", button_type="primary"):
    colors = {
        "primary": ("linear-gradient(90deg, #1E88E5 0%, #1565C0 100%)", "white"),
        "success": ("linear-gradient(90deg, #4CAF50 0%, #388E3C 100%)", "white"),
        "danger": ("linear-gradient(90deg, #F44336 0%, #D32F2F 100%)", "white"),
        "secondary": ("#f5f5f5", "#333")
    }
    
    bg, color = colors.get(button_type, colors["primary"])
    
    button_html = f"""
        <style>
        .custom-btn-{key} {{
            background: {bg};
            color: {color};
            padding: 12px 24px;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-block;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .custom-btn-{key}:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        </style>
        <button class="custom-btn-{key}">{icon} {label}</button>
    """
    
    return st.markdown(button_html, unsafe_allow_html=True)

# Section header
def section_header(title, subtitle=None, icon="📌"):
    subtitle_html = f'<p style="color: #666; font-size: 16px; margin-top: 5px;">{subtitle}</p>' if subtitle else ""
    
    st.markdown(f"""
        <div style="margin-bottom: 30px;">
            <h2 style="color: #1E88E5; margin-bottom: 5px;">
                <span style="font-size: 32px; margin-right: 10px;">{icon}</span>
                {title}
            </h2>
            {subtitle_html}
            <div style="height: 3px; width: 60px; background: linear-gradient(90deg, #1E88E5, #1565C0); border-radius: 2px; margin-top: 10px;"></div>
        </div>
    """, unsafe_allow_html=True)

# Info card
def info_card(title, content, icon="ℹ️", color="#1E88E5"):
    st.markdown(f"""
        <div style="background: white; border-left: 4px solid {color}; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); margin-bottom: 20px;">
            <div style="font-size: 24px; margin-bottom: 10px;">{icon}</div>
            <h3 style="color: {color}; margin-bottom: 10px;">{title}</h3>
            <p style="color: #666; line-height: 1.6;">{content}</p>
        </div>
    """, unsafe_allow_html=True)

# Risk badge
def risk_badge(risk_level):
    colors = {
        "Critical": ("#FF4444", "#FFE5E5"),
        "High Risk": ("#FFA500", "#FFF3E0"),
        "Medium Risk": ("#FFD700", "#FFFACD"),
        "Low Risk": ("#4CAF50", "#E8F5E9")
    }
    
    color, bg = colors.get(risk_level, ("#666", "#f5f5f5"))
    
    return f"""
        <span style="
            background: {bg};
            color: {color};
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
            display: inline-block;
            border: 2px solid {color};
        ">{risk_level}</span>
    """
    
