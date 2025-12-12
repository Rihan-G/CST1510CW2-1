"""
Theme configuration module for the Intelligence Platform.
Provides consistent styling across all dashboards.
"""

import streamlit as st

def apply_modern_theme(dark_mode: bool = True):
    """
    Apply modern theme styling to the Streamlit application.
    
    Args:
        dark_mode (bool): Whether to apply dark mode styling (default: True)
    """
    if dark_mode:
        st.markdown("""
        <style>
            /* Apply dark theme to entire app */
            html, body, [class*="st-"], .stApp, .main {
                background: linear-gradient(135deg, #0f172a 0%, #1a202c 100%) !important;
                color: #e2e8f0 !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            }
            
            /* Override Streamlit's default styles */
            .stApp {
                background: linear-gradient(135deg, #0f172a 0%, #1a202c 100%) !important;
            }
            
            .main .block-container {
                background: transparent !important;
                color: #e2e8f0 !important;
            }
            
            /* Text colors */
            h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stText, .stTitle {
                color: #e2e8f0 !important;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background: linear-gradient(135deg, #0f172a 0%, #1a202c 100%) !important;
                border-right: 1px solid #334155 !important;
            }
            
            [data-testid="stSidebar"] * {
                color: #e2e8f0 !important;
            }
            
            /* Buttons */
            .stButton > button {
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 20px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
            }
            
            .stButton > button:active {
                background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%) !important;
            }
            
            button[kind="secondary"] {
                background: linear-gradient(135deg, #475569 0%, #64748b 100%) !important;
            }
            
            button[kind="secondary"]:hover {
                background: linear-gradient(135deg, #64748b 0%, #94a3b8 100%) !important;
            }
            
            /* Input fields */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select,
            .stNumberInput > div > div > input,
            .stSlider > div > div > input {
                background-color: #1e293b !important;
                color: #e2e8f0 !important;
                border-color: #4b5563 !important;
                border-radius: 6px !important;
            }
            
            /* Metric cards */
            .metric-card {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
                padding: 20px !important;
                border-radius: 12px !important;
                border-left: 4px solid #6366f1 !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
                margin-bottom: 10px !important;
                color: #e2e8f0 !important;
            }
            
            /* Dataframes and tables */
            .dataframe {
                background-color: #1e293b !important;
                color: #e2e8f0 !important;
            }
            
            table {
                background-color: #1e293b !important;
                color: #e2e8f0 !important;
            }
            
            th, td {
                background-color: #1e293b !important;
                color: #e2e8f0 !important;
                border-color: #4b5563 !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px !important;
                background-color: #1e293b !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #1e293b !important;
                border-radius: 4px 4px 0px 0px !important;
                padding: 10px 16px !important;
                color: #94a3b8 !important;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #0f172a !important;
                color: #6366f1 !important;
                border-bottom: 2px solid #6366f1 !important;
            }
            
            /* Expanders */
            .streamlit-expanderHeader {
                background-color: #1e293b !important;
                color: #e2e8f0 !important;
                border: 1px solid #334155 !important;
            }
            
            /* Alerts */
            .stAlert {
                background-color: #1e293b !important;
                color: #e2e8f0 !important;
                border: 1px solid #4b5563 !important;
                border-radius: 8px !important;
            }
            
            /* Radio buttons */
            .stRadio > div {
                background-color: #1e293b !important;
                color: #e2e8f0 !important;
            }
            
            /* Checkboxes */
            .stCheckbox > label {
                color: #e2e8f0 !important;
            }
            
            /* Progress bars */
            .stProgress > div > div {
                background-color: #6366f1 !important;
            }
            
            /* Charts containers */
            .js-plotly-plot, .plotly, .chart-container {
                background-color: #1e293b !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            /* Apply light theme to entire app */
            html, body, [class*="st-"], .stApp, .main {
                background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
                color: #1e293b !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            }
            
            /* Override Streamlit's default styles */
            .stApp {
                background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
            }
            
            .main .block-container {
                background: transparent !important;
                color: #1e293b !important;
            }
            
            /* Text colors */
            h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stText, .stTitle {
                color: #1e293b !important;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
                border-right: 1px solid #e2e8f0 !important;
            }
            
            [data-testid="stSidebar"] * {
                color: #1e293b !important;
            }
            
            /* Buttons */
            .stButton > button {
                background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 20px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
            }
            
            .stButton > button:active {
                background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%) !important;
            }
            
            button[kind="secondary"] {
                background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%) !important;
                color: #1e293b !important;
            }
            
            button[kind="secondary"]:hover {
                background: linear-gradient(135deg, #d1d5db 0%, #9ca3af 100%) !important;
            }
            
            /* Input fields */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select,
            .stNumberInput > div > div > input,
            .stSlider > div > div > input {
                background-color: white !important;
                color: #1e293b !important;
                border-color: #d1d5db !important;
                border-radius: 6px !important;
            }
            
            /* Metric cards */
            .metric-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
                padding: 20px !important;
                border-radius: 12px !important;
                border-left: 4px solid #3b82f6 !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
                margin-bottom: 10px !important;
                color: #1e293b !important;
            }
            
            /* Dataframes and tables */
            .dataframe {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            table {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            th, td {
                background-color: white !important;
                color: #1e293b !important;
                border-color: #e2e8f0 !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px !important;
                background-color: #f3f4f6 !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #f3f4f6 !important;
                border-radius: 4px 4px 0px 0px !important;
                padding: 10px 16px !important;
                color: #6b7280 !important;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: white !important;
                color: #3b82f6 !important;
                border-bottom: 2px solid #3b82f6 !important;
            }
            
            /* Expanders */
            .streamlit-expanderHeader {
                background-color: white !important;
                color: #1e293b !important;
                border: 1px solid #e2e8f0 !important;
            }
            
            /* Alerts */
            .stAlert {
                background-color: white !important;
                color: #1e293b !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 8px !important;
            }
            
            /* Radio buttons */
            .stRadio > div {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            /* Checkboxes */
            .stCheckbox > label {
                color: #1e293b !important;
            }
            
            /* Progress bars */
            .stProgress > div > div {
                background-color: #3b82f6 !important;
            }
            
            /* Charts containers */
            .js-plotly-plot, .plotly, .chart-container {
                background-color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)