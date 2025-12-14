"""
Gemini AI Integration module.
"""

import google.generativeai as genai
import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional


class AIIntegration:
    """Gemini AI Assistant."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize."""
        # Get API key
        if api_key:
            self.api_key = api_key
        else:
            try:
                self.api_key = st.secrets["GEMINI_API_KEY"]
            except:
                self.api_key = ""
        
        self.model = None
        self.model_name = None
        self.status = "Not initialized"
        
        # Initialize
        self._init()

    def _init(self):
        """Initialize Gemini."""
        if not self.api_key:
            self.status = "❌ No API key"
            return
        
        try:
            # Configure
            genai.configure(api_key=self.api_key)
            
            # Try listing available models first - this ensures we only use models
            # that are actually available for the current API version (v1beta)
            models_to_try = []
            try:
                all_models = genai.list_models()
                print(f"Found {len(all_models)} total models")
                for m in all_models:
                    name = m.name.replace('models/', '')
                    # Skip models that require computer use
                    # Allow 2.0 models (including experimental like 2.0-flash-exp which user said worked)
                    # Skip 2.5 and other experimental models that aren't 2.0
                    if ('computer' in name.lower() or 
                        ('exp' in name.lower() and '2.0' not in name) or 
                        '2.5' in name):
                        continue
                    
                    # Only add models that support generateContent
                    if ('gemini' in name.lower() and 
                        'generateContent' in m.supported_generation_methods):
                        models_to_try.append(name)
                        print(f"  Added model: {name}")
            except Exception as e:
                print(f"Could not list models: {e}")
            
            # Fallback models - try 2.0-flash variants first (user mentioned they worked), then gemini-pro
            if not models_to_try:
                print("No models found from list_models(), trying fallback models")
                models_to_try = ["gemini-2.0-flash-exp", "gemini-2.0-flash", "gemini-pro"]
            
            if not models_to_try:
                self.status = "❌ No compatible models found"
                print("❌ No models to try")
                return
            
            # Try each model - only use models that actually work
            print(f"Trying {len(models_to_try)} model(s): {models_to_try}")
            for model_name in models_to_try:
                try:
                    print(f"Attempting to initialize: {model_name}")
                    # Use positional argument, not keyword
                    self.model = genai.GenerativeModel(model_name)
                    
                    # Test with a simple call to verify it works
                    test_response = self.model.generate_content("Hi")
                    if test_response:
                        self.model_name = model_name
                        self.status = f"✅ Ready ({model_name})"
                        print(f"✅ Gemini initialized successfully: {model_name}")
                        return
                except Exception as e:
                    error_str = str(e)
                    # Skip models that don't exist (404) or require special config
                    if ("404" in error_str or 
                        "not found" in error_str.lower() or
                        "not supported" in error_str.lower() or
                        "v1beta" in error_str.lower() or
                        "computer use" in error_str.lower() or 
                        "400" in error_str):
                        print(f"   ❌ {model_name}: Skipped - {error_str[:80]}")
                        continue
                    # For other errors, still skip but log differently
                    print(f"   ⚠️ {model_name}: Error - {error_str[:80]}")
                    continue
            
            self.status = "❌ Failed to initialize"
            print("❌ Failed to initialize any Gemini model")
            
        except Exception as e:
            self.status = f"❌ Error: {str(e)[:50]}"
            print(f"❌ Initialization error: {e}")

    def get_ai_status(self) -> str:
        """Get status."""
        return self.status

    def chat_with_ai(self, user_message: str, stream: bool = False) -> str:
        """Chat with AI."""
        if not self.model:
            return f"AI unavailable. Status: {self.status}"
        
        try:
            response = self.model.generate_content(user_message)
            
            # Get text from response
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].content.parts[0].text
            else:
                return str(response)
                
        except Exception as e:
            return f"Error: {str(e)}"

    def analyse_incident_patterns(self, incidents: List[Dict[str, Any]]) -> str:
        """Analyse incidents."""
        if not self.model:
            # Fallback
            if incidents:
                df = pd.DataFrame(incidents)
                return f"Found {len(df)} incidents. Top threats: {df['threat_type'].value_counts().head(2).index.tolist() if 'threat_type' in df.columns else 'N/A'}"
            return "No incidents"
        
        try:
            summary = "\n".join([f"{i.get('title', 'N/A')}: {i.get('severity', 'N/A')}" for i in incidents[:5]])
            prompt = f"Analyse these incidents:\n{summary}"
            response = self.model.generate_content(prompt)
            
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].content.parts[0].text
            else:
                return str(response)
        except Exception as e:
            return f"Analysis error: {str(e)[:100]}"

    def analyse_data_quality(self, datasets: List[Dict[str, Any]]) -> str:
        """Analyse data quality."""
        if not self.model:
            # Fallback
            if datasets:
                df = pd.DataFrame(datasets)
                avg = df['quality_score'].mean() if 'quality_score' in df.columns else 0
                return f"Found {len(df)} datasets. Avg quality: {avg:.1f}/10"
            return "No datasets"
        
        try:
            summary = "\n".join([f"{d.get('name', 'N/A')}: {d.get('quality_score', 'N/A')}/10" for d in datasets[:5]])
            prompt = f"Analyse data quality:\n{summary}"
            response = self.model.generate_content(prompt)
            
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].content.parts[0].text
            else:
                return str(response)
        except Exception as e:
            return f"Analysis error: {str(e)[:100]}"

    def clear_history(self):
        """Clear history."""
        pass
