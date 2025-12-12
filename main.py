"""
Main entry point for the Intelligence Platform application.
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth.authentication import AuthenticationSystem
from database.db_manager import DatabaseManager
from ai.gemini_integration import AIIntegration
from utils.theme import apply_modern_theme

# Import dashboard modules from dashboards package
from dashboards.cybersecurity import CyberSecurityDashboard
from dashboards.data_science import DataScienceDashboard
from dashboards.it_operations import ITOperationsDashboard
from dashboards.executive import ExecutiveDashboard
from dashboards.ai_assistant import AIAssistantDashboard

def main():
    """Main application entry point."""
    
    # Configure page FIRST
    st.set_page_config(
        page_title="Intelligence Platform",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Hide Streamlit menu and footer
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.username = None
        st.session_state.dark_mode = True
    
    # Apply theme
    apply_modern_theme(st.session_state.dark_mode)
    
    # Initialize core components
    db_manager = DatabaseManager()
    auth_system = AuthenticationSystem(db_manager)
    ai_engine = AIIntegration()
    
    # Login/Signup page
    if not st.session_state.authenticated:
        show_login_page(auth_system)
        return
    
    # Main application after login
    show_main_application(db_manager, ai_engine)

def show_login_page(auth_system):
    """Display login and registration interface."""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🛡️ Intelligence Platform</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-bottom: 40px;'>Unified platform for Cybersecurity, Data Science, and IT Operations</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.markdown("### Login to Your Account")
            
            with st.form("login_form"):
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                submit = st.form_submit_button("Login", type="primary")
                if submit:
                    if username and password:
                        user = auth_system.login_user(username, password)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user_role = user['role']
                            st.session_state.username = username
                            st.success(f"✅ Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
                    else:
                        st.error("Please enter both username and password")
        
        with tab2:
            st.markdown("### Create New Account")
            
            with st.form("register_form"):
                new_username = st.text_input("Choose Username", key="reg_username")
                new_password = st.text_input("Choose Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
                role = st.selectbox("Select Role", ["admin", "cybersecurity", "data_science", "it_operations"], key="reg_role")
                
                submit = st.form_submit_button("Register", type="primary")
                if submit:
                    if new_username and new_password:
                        if new_password == confirm_password:
                            if auth_system.register_user(new_username, new_password, role):
                                st.success("✅ Account created successfully! Please login.")
                            else:
                                st.error("❌ Registration failed. Username might already exist.")
                        else:
                            st.error("Passwords do not match!")
                    else:
                        st.error("Please fill in all fields")

def show_main_application(db_manager, ai_engine):
    """Display the main application with navigation."""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### 👤 Welcome, {st.session_state.username}")
        st.markdown(f"**Role:** {st.session_state.user_role.replace('_', ' ').title()}")
        
        st.markdown("---")
        
        # Navigation options based on role
        dashboard_options = ["🏠 Executive Dashboard"]
        
        # Admin has access to all dashboards
        if st.session_state.user_role == "admin":
            dashboard_options.extend([
                "🛡️ Cybersecurity",
                "📊 Data Science",
                "💻 IT Operations"
            ])
        else:
            if st.session_state.user_role == "cybersecurity":
                dashboard_options.append("🛡️ Cybersecurity")
            if st.session_state.user_role == "data_science":
                dashboard_options.append("📊 Data Science")
            if st.session_state.user_role == "it_operations":
                dashboard_options.append("💻 IT Operations")
        
        dashboard_options.append("🤖 AI Assistant")
        
        selected_dashboard = st.radio(
            "Navigate to:",
            dashboard_options,
            index=0,
            key="nav_radio"
        )
        
        st.markdown("---")
        
        # Platform Statistics
        try:
            stats = db_manager.get_statistics()
            st.markdown("### 📊 Platform Stats")
            st.markdown(f"**Users:** {stats.get('user_count', 0)}")
            st.markdown(f"**Incidents:** {stats.get('total_incidents', 0)} ({stats.get('open_incidents', 0)} open)")
            st.markdown(f"**Datasets:** {stats.get('total_datasets', 0)} (Avg quality: {stats.get('avg_quality', 0):.1f}/10)")
            st.markdown(f"**Tickets:** {stats.get('total_tickets', 0)} ({stats.get('open_tickets', 0)} open)")
        except Exception as e:
            st.warning("Could not load platform statistics")
        
        st.markdown("---")
        
        # Theme toggle
        dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="theme_toggle")
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        # Logout button
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.username = None
            st.rerun()
    
    # Main content area
    main_container = st.container()
    
    with main_container:
        # Display selected dashboard
        try:
            if selected_dashboard == "🏠 Executive Dashboard":
                dashboard = ExecutiveDashboard(db_manager, ai_engine)
                dashboard.display()
            
            elif selected_dashboard == "🛡️ Cybersecurity":
                if st.session_state.user_role in ["admin", "cybersecurity"]:
                    dashboard = CyberSecurityDashboard(db_manager, ai_engine)
                    dashboard.display()
                else:
                    st.error("⛔ You don't have permission to access the Cybersecurity dashboard.")
            
            elif selected_dashboard == "📊 Data Science":
                if st.session_state.user_role in ["admin", "data_science"]:
                    dashboard = DataScienceDashboard(db_manager, ai_engine)
                    dashboard.display()
                else:
                    st.error("⛔ You don't have permission to access the Data Science dashboard.")
            
            elif selected_dashboard == "💻 IT Operations":
                if st.session_state.user_role in ["admin", "it_operations"]:
                    dashboard = ITOperationsDashboard(db_manager, ai_engine)
                    dashboard.display()
                else:
                    st.error("⛔ You don't have permission to access the IT Operations dashboard.")
            
            elif selected_dashboard == "🤖 AI Assistant":
                dashboard = AIAssistantDashboard(ai_engine, db_manager)
                dashboard.display()
        
        except Exception as e:
            st.error(f"Error loading dashboard: {str(e)}")
            st.info("Please try refreshing the page or contact support.")

if __name__ == "__main__":
    main()