"""
Authentication module for the Intelligence Platform.
"""

import bcrypt
import streamlit as st
from typing import Optional, Dict
from database.db_manager import DatabaseManager

class AuthenticationSystem:
    """Handles user authentication."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False

    def register_user(self, username: str, password: str, role: str) -> bool:
        try:
            existing_user = self.db.get_user(username)
            if existing_user:
                st.error(f"❌ Username '{username}' already exists!")
                return False
            
            hashed_pw = self.hash_password(password)
            success = self.db.create_user(username, hashed_pw, role)
            
            if success:
                st.success(f"✅ Account created for {username}!")
                return True
            return False
        except Exception as e:
            st.error(f"❌ Registration error: {str(e)}")
            return False

    def login_user(self, username: str, password: str) -> Optional[dict]:
        try:
            user = self.db.get_user(username)
            if user and self.verify_password(password, user['password_hash']):
                return user
            return None
        except Exception as e:
            st.error(f"❌ Login error: {str(e)}")
            return None