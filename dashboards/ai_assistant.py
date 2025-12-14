"""
AI Assistant Dashboard module for intelligent chat and analysis.
Provides AI-powered assistance across all platform functions.
"""

import streamlit as st
from ai.gemini_integration import AIIntegration
from database.db_manager import DatabaseManager

class AIAssistantDashboard:
    """AI Assistant dashboard for intelligent chat and analysis."""
    
    def __init__(self, ai_engine, db_manager=None):
        """Initialise AI assistant dashboard with AI engine and database."""
        self.ai_engine = ai_engine
        self.db_manager = db_manager

    def display(self):
        """Render the AI assistant interface."""
        st.markdown("# 🤖 AI Assistant")
        
        # Introduction
        st.markdown("""
        Welcome to your AI Assistant! I can help you with:
        
        - **Cybersecurity:** Incident analysis, threat detection, security recommendations
        - **Data Science:** Data quality assessment, analytics insights, dataset recommendations
        - **IT Operations:** Ticket analysis, performance insights, operational recommendations
        - **General:** Platform navigation, report generation, best practices
        
        Ask me anything about the Intelligence Platform!
        """)
        
        # Initialise chat history in session state
        if 'ai_chat_messages' not in st.session_state:
            st.session_state.ai_chat_messages = []
        
        # Display chat messages
        st.markdown("### 💬 Conversation")
        
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.ai_chat_messages:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style='text-align: right; margin-bottom: 10px;'>
                        <div class='user-message'>
                            <strong>You:</strong><br>
                            {message['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: left; margin-bottom: 10px;'>
                        <div class='ai-message'>
                            <strong>AI Assistant:</strong><br>
                            {message['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Get dashboard-specific questions based on user role
        user_role = st.session_state.get('user_role', 'admin')
        
        # Dashboard-specific questions
        st.markdown("### 💡 Quick Questions")
        
        # Initialize selected question in session state
        if 'selected_question' not in st.session_state:
            st.session_state.selected_question = ""
        
        # Cybersecurity questions
        if user_role in ["admin", "cybersecurity"]:
            st.markdown("#### 🛡️ Cybersecurity")
            cyber_cols = st.columns(3)
            cyber_questions = [
                "What are the most critical security incidents?",
                "Which threat types are most common?",
                "Analyse security incident patterns",
                "What security recommendations do you have?",
                "How many incidents are still open?",
                "What's the average resolution time?"
            ]
            for idx, question in enumerate(cyber_questions):
                with cyber_cols[idx % 3]:
                    if st.button(question, key=f"cyber_{idx}", use_container_width=True):
                        # Auto-submit the question
                        st.session_state.ai_chat_messages.append({
                            'role': 'user', 
                            'content': question
                        })
                        with st.spinner("🤖 Thinking..."):
                            response = self._get_ai_response_with_context(question)
                        st.session_state.ai_chat_messages.append({
                            'role': 'assistant', 
                            'content': response
                        })
                        st.rerun()
        
        # Data Science questions
        if user_role in ["admin", "data_science"]:
            st.markdown("#### 📊 Data Science")
            data_cols = st.columns(3)
            data_questions = [
                "What's the overall data quality score?",
                "Which datasets need improvement?",
                "Analyse data quality trends",
                "What data governance recommendations?",
                "Which departments have best data quality?",
                "What's the total data size?"
            ]
            for idx, question in enumerate(data_questions):
                with data_cols[idx % 3]:
                    if st.button(question, key=f"data_{idx}", use_container_width=True):
                        # Auto-submit the question
                        st.session_state.ai_chat_messages.append({
                            'role': 'user', 
                            'content': question
                        })
                        with st.spinner("🤖 Thinking..."):
                            response = self._get_ai_response_with_context(question)
                        st.session_state.ai_chat_messages.append({
                            'role': 'assistant', 
                            'content': response
                        })
                        st.rerun()
        
        # IT Operations questions
        if user_role in ["admin", "it_operations"]:
            st.markdown("#### 💻 IT Operations")
            it_cols = st.columns(3)
            it_questions = [
                "What IT tickets need attention?",
                "What's the average ticket resolution time?",
                "Analyse IT ticket patterns",
                "Which categories have most tickets?",
                "What IT recommendations do you have?",
                "How many tickets are still open?"
            ]
            for idx, question in enumerate(it_questions):
                with it_cols[idx % 3]:
                    if st.button(question, key=f"it_{idx}", use_container_width=True):
                        # Auto-submit the question
                        st.session_state.ai_chat_messages.append({
                            'role': 'user', 
                            'content': question
                        })
                        with st.spinner("🤖 Thinking..."):
                            response = self._get_ai_response_with_context(question)
                        st.session_state.ai_chat_messages.append({
                            'role': 'assistant', 
                            'content': response
                        })
                        st.rerun()
        
        # General questions
        st.markdown("#### 🌐 General")
        general_cols = st.columns(3)
        general_questions = [
            "Give me a system health summary",
            "What are the top priorities?",
            "Any overall recommendations?"
        ]
        for idx, question in enumerate(general_questions):
            with general_cols[idx % 3]:
                if st.button(question, key=f"general_{idx}", use_container_width=True):
                    # Auto-submit the question
                    st.session_state.ai_chat_messages.append({
                        'role': 'user', 
                        'content': question
                    })
                    with st.spinner("🤖 Thinking..."):
                        response = self._get_ai_response_with_context(question)
                    st.session_state.ai_chat_messages.append({
                        'role': 'assistant', 
                        'content': response
                    })
                    st.rerun()
        
        # Chat input
        st.markdown("---")
        st.markdown("### ✍️ Ask a Question")
        
        # Use a form for the chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Type your question here:",
                placeholder="E.g., 'What are the current security threats?' or 'How can I improve data quality?'",
                height=100,
                key="user_input"
            )
            
            col1, col2 = st.columns([4, 1])
            with col1:
                send_button = st.form_submit_button("Send", type="primary", use_container_width=True)
        
        # Handle form submission
        if send_button and user_input:
            # Add user message to chat history
            st.session_state.ai_chat_messages.append({
                'role': 'user', 
                'content': user_input
            })
            
            # Get AI response with dashboard data context
            with st.spinner("🤖 Thinking..."):
                response = self._get_ai_response_with_context(user_input)
            
            # Add AI response to chat history
            st.session_state.ai_chat_messages.append({
                'role': 'assistant', 
                'content': response
            })
            
            # Clear selected question
            st.session_state.selected_question = ""
            st.rerun()
        
        # Chat management
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Clear Chat", key="clear_chat"):
                st.session_state.ai_chat_messages = []
                st.rerun()
        
        with col2:
            if st.button("Export Chat", key="export_chat"):
                self._export_chat_history()
        
        with col3:
            chat_length = len(st.session_state.ai_chat_messages)
            st.metric("Messages", chat_length)

    def _get_dashboard_questions(self, user_role):
        """Get dashboard-specific questions based on user role."""
        questions = {
            "admin": {
                "cybersecurity": ["What are the most critical security incidents?", "Analyse security patterns"],
                "data_science": ["What's the overall data quality?", "Which datasets need improvement?"],
                "it_operations": ["What IT tickets need attention?", "Analyse ticket patterns"]
            },
            "cybersecurity": ["What are the most critical security incidents?", "Which threat types are most common?"],
            "data_science": ["What's the overall data quality?", "Which datasets need improvement?"],
            "it_operations": ["What IT tickets need attention?", "What's the average resolution time?"]
        }
        return questions.get(user_role, {})
    
    def _get_ai_response_with_context(self, user_message):
        """Get AI response with dashboard data context."""
        if not self.db_manager:
            return self.ai_engine.chat_with_ai(user_message)
        
        # Get relevant data based on question context
        context = ""
        
        # Check if question is about cybersecurity
        if any(word in user_message.lower() for word in ['security', 'incident', 'threat', 'cyber', 'breach', 'malware', 'phishing']):
            incidents = self.db_manager.get_cyber_incidents()
            if incidents:
                context = f"\n\nCurrent Security Incidents Data:\n"
                context += f"Total incidents: {len(incidents)}\n"
                open_count = len([i for i in incidents if i.get('status') == 'Open'])
                context += f"Open incidents: {open_count}\n"
                critical_count = len([i for i in incidents if i.get('severity') == 'Critical'])
                context += f"Critical incidents: {critical_count}\n"
                # Get top threat types
                from collections import Counter
                threat_types = Counter([i.get('threat_type', 'Unknown') for i in incidents])
                context += f"Top threat types: {', '.join([f'{k}({v})' for k, v in threat_types.most_common(3)])}\n"
                # Include recent incidents
                context += "\nRecent incidents:\n"
                for inc in incidents[:5]:
                    context += f"- {inc.get('title', 'N/A')}: {inc.get('severity', 'N/A')} - {inc.get('status', 'N/A')}\n"
        
        # Check if question is about data science
        elif any(word in user_message.lower() for word in ['data', 'dataset', 'quality', 'analytics', 'database']):
            datasets = self.db_manager.get_all_datasets()
            if datasets:
                context = f"\n\nCurrent Datasets Data:\n"
                context += f"Total datasets: {len(datasets)}\n"
                import statistics
                quality_scores = [d.get('quality_score', 0) for d in datasets if d.get('quality_score')]
                if quality_scores:
                    avg_quality = statistics.mean(quality_scores)
                    context += f"Average quality score: {avg_quality:.1f}/10\n"
                total_size = sum([d.get('size_mb', 0) for d in datasets])
                context += f"Total data size: {total_size:.1f} MB\n"
                # Get departments
                from collections import Counter
                departments = Counter([d.get('source_department', 'Unknown') for d in datasets])
                context += f"Top departments: {', '.join([f'{k}({v})' for k, v in departments.most_common(3)])}\n"
                # Include recent datasets
                context += "\nRecent datasets:\n"
                for ds in datasets[:5]:
                    context += f"- {ds.get('name', 'N/A')}: Quality {ds.get('quality_score', 'N/A')}/10\n"
        
        # Check if question is about IT operations
        elif any(word in user_message.lower() for word in ['ticket', 'it', 'support', 'server', 'network', 'system']):
            tickets = self.db_manager.get_all_it_tickets()
            if tickets:
                context = f"\n\nCurrent IT Tickets Data:\n"
                context += f"Total tickets: {len(tickets)}\n"
                open_count = len([t for t in tickets if t.get('status') == 'Open'])
                context += f"Open tickets: {open_count}\n"
                # Get priorities
                from collections import Counter
                priorities = Counter([t.get('priority', 'Unknown') for t in tickets])
                context += f"Priority distribution: {', '.join([f'{k}({v})' for k, v in priorities.most_common(3)])}\n"
                categories = Counter([t.get('category', 'Unknown') for t in tickets])
                context += f"Top categories: {', '.join([f'{k}({v})' for k, v in categories.most_common(3)])}\n"
                # Include recent tickets
                context += "\nRecent tickets:\n"
                for ticket in tickets[:5]:
                    context += f"- {ticket.get('title', 'N/A')}: {ticket.get('priority', 'N/A')} - {ticket.get('status', 'N/A')}\n"
        
        # Combine user message with context
        full_message = user_message + context
        
        # Use appropriate AI method
        if 'analyse' in user_message.lower() or 'pattern' in user_message.lower():
            if 'incident' in user_message.lower() or 'security' in user_message.lower():
                incidents = self.db_manager.get_cyber_incidents()
                return self.ai_engine.analyse_incident_patterns(incidents)
            elif 'data' in user_message.lower() or 'dataset' in user_message.lower():
                datasets = self.db_manager.get_all_datasets()
                return self.ai_engine.analyse_data_quality(datasets)
        
        return self.ai_engine.chat_with_ai(full_message)
    
    def _export_chat_history(self):
        """Export chat history as a text file."""
        if not st.session_state.ai_chat_messages:
            st.warning("No chat history to export.")
            return
        
        chat_text = "Intelligence Platform - AI Assistant Chat History\n"
        chat_text += "=" * 50 + "\n\n"
        
        for message in st.session_state.ai_chat_messages:
            if message['role'] == 'user':
                chat_text += f"You: {message['content']}\n\n"
            else:
                chat_text += f"AI Assistant: {message['content']}\n\n"
        
        # Create download link
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_chat_history_{timestamp}.txt"
        
        st.download_button(
            label="Download Chat History",
            data=chat_text,
            file_name=filename,
            mime="text/plain"
        )