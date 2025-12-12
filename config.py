"""Configuration settings and constants for the Intelligence Platform."""

import streamlit as st

# Get API key from Streamlit secrets (like okok folder)
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    GEMINI_MODEL_NAME = st.secrets.get("GEMINI_MODEL_NAME", "gemini-1.5-flash")
except:
    # Fallback if secrets not available
    GEMINI_API_KEY = ""
    GEMINI_MODEL_NAME = "gemini-1.5-flash"

# Dashboard Permissions
DASHBOARD_PERMISSIONS = {
    "admin": ["executive", "cybersecurity", "data_science", "it_operations", "ai_assistant"],
    "cybersecurity": ["executive", "cybersecurity", "ai_assistant"],
    "data_science": ["executive", "data_science", "ai_assistant"],
    "it_operations": ["executive", "it_operations", "ai_assistant"]
}

# Application Settings
APP_TITLE = "Intelligence Platform"
APP_ICON = "🛡️"
DEFAULT_THEME = "dark"

# Database Configuration
DATABASE_PATH = "intelligence_platform.db"

# Default User Credentials
DEFAULT_USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "cyber": {"password": "cyber123", "role": "cybersecurity"},
    "data": {"password": "data123", "role": "data_science"},
    "it": {"password": "it123", "role": "it_operations"}
}

# Chart Colors
CHART_COLOURS = {
    "primary": "#6366f1",
    "secondary": "#8b5cf6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#3b82f6"
}

# Incident Configuration
INCIDENT_SEVERITIES = ["Low", "Medium", "High", "Critical"]
INCIDENT_STATUSES = ["Open", "In Progress", "Resolved"]
THREAT_TYPES = ["Phishing", "Malware", "DDoS", "Brute Force", "Data Breach", "Insider Threat"]

# Dataset Configuration
DATA_DEPARTMENTS = ["Sales", "Marketing", "Engineering", "Finance", "HR", "Operations"]
SENSITIVITY_LEVELS = ["Low", "Medium", "High", "Confidential"]
QUALITY_SCORE_RANGE = (1, 10)

# IT Operations Configuration
TICKET_PRIORITIES = ["Low", "Medium", "High", "Critical"]
TICKET_STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
TICKET_CATEGORIES = ["Hardware", "Software", "Network", "Security", "Database", "Other"]
TICKET_STAGES = ["New", "Triaged", "In Progress", "Pending Review", "Resolved"]