"""
Executive Dashboard module for high-level overview across all departments.
Provides cross-functional insights and key performance indicators.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

class ExecutiveDashboard:
    """Executive dashboard showing cross-department overview and key metrics."""
    
    def __init__(self, db_manager, ai_engine):
        """Initialise dashboard with database and AI engine."""
        self.db = db_manager
        self.ai_engine = ai_engine

    def display(self):
        """Render the executive dashboard interface."""
        st.markdown("# 🏢 Executive Intelligence Dashboard")
        
        # Fetch data from all departments
        incidents = self.db.get_cyber_incidents()
        datasets = self.db.get_all_datasets()
        tickets = self.db.get_all_it_tickets()
        
        # Export options
        st.markdown("### 📥 Export Data")
        export_col1, export_col2, export_col3, export_col4 = st.columns(4)
        
        with export_col1:
            if incidents:
                incidents_df = pd.DataFrame(incidents)
                csv_incidents = incidents_df.to_csv(index=False)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 Cyber Incidents",
                    data=csv_incidents,
                    file_name=f"cyber_incidents_{timestamp}.csv",
                    mime="text/csv",
                    key="export_exec_cyber"
                )
        
        with export_col2:
            if datasets:
                datasets_df = pd.DataFrame(datasets)
                csv_datasets = datasets_df.to_csv(index=False)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 Datasets",
                    data=csv_datasets,
                    file_name=f"datasets_{timestamp}.csv",
                    mime="text/csv",
                    key="export_exec_data"
                )
        
        with export_col3:
            if tickets:
                tickets_df = pd.DataFrame(tickets)
                csv_tickets = tickets_df.to_csv(index=False)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 IT Tickets",
                    data=csv_tickets,
                    file_name=f"it_tickets_{timestamp}.csv",
                    mime="text/csv",
                    key="export_exec_it"
                )
        
        with export_col4:
            if incidents or datasets or tickets:
                # Combined export
                all_data = {
                    'cyber_incidents': pd.DataFrame(incidents) if incidents else pd.DataFrame(),
                    'datasets': pd.DataFrame(datasets) if datasets else pd.DataFrame(),
                    'it_tickets': pd.DataFrame(tickets) if tickets else pd.DataFrame()
                }
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Create a combined summary CSV
                summary_data = {
                    'Category': ['Cyber Incidents', 'Datasets', 'IT Tickets'],
                    'Count': [len(incidents), len(datasets), len(tickets)],
                    'Export_Date': [timestamp, timestamp, timestamp]
                }
                summary_df = pd.DataFrame(summary_data)
                csv_summary = summary_df.to_csv(index=False)
                
                st.download_button(
                    label="📥 Summary",
                    data=csv_summary,
                    file_name=f"platform_summary_{timestamp}.csv",
                    mime="text/csv",
                    key="export_exec_summary"
                )
        
        st.markdown("---")
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            security_score = self._calculate_security_score(incidents)
            st.markdown(f"""
            <div class='metric-card'>
                <h3>🔒 Security Posture</h3>
                <h2 style='color: #10b981;'>{security_score}/100</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            system_health = self._calculate_system_health(tickets)
            st.markdown(f"""
            <div class='metric-card'>
                <h3>💻 System Health</h3>
                <h2 style='color: #10b981;'>{system_health}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            data_quality = self._calculate_data_quality(datasets)
            st.markdown(f"""
            <div class='metric-card'>
                <h3>📊 Data Quality</h3>
                <h2 style='color: #10b981;'>{data_quality:.1%}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            critical_incidents = len([i for i in incidents if i['severity'] in ['High', 'Critical']])
            st.markdown(f"""
            <div class='metric-card'>
                <h3>🚨 Critical Incidents</h3>
                <h2 style='color: #ef4444;'>{critical_incidents}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Cross-Department Overview Chart
        st.markdown("### 📈 Cross-Department Overview")
        self._display_department_overview(incidents, tickets, datasets)
        
        st.markdown("---")
        
        # Interactive Analytics Section
        st.markdown("### 📊 Interactive Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            self._display_security_trends(incidents)
        
        with col2:
            self._display_system_health_metrics(tickets)
        
        # Data Quality Section
        st.markdown("---")
        st.markdown("### 📋 Data Quality Dashboard")
        col1, col2 = st.columns(2)
        
        with col1:
            self._display_data_quality_metrics(datasets)
        
        with col2:
            self._display_sensitivity_distribution(datasets)

    def _calculate_security_score(self, incidents):
        """Calculate overall security posture score."""
        if not incidents:
            return 85  # Default score
        
        df = pd.DataFrame(incidents)
        resolved = len(df[df['status'] == 'Resolved'])
        total = len(df)
        resolution_rate = resolved / total if total > 0 else 1
        
        critical = len(df[df['severity'] == 'Critical'])
        penalty = critical * 5
        
        score = 85 + (resolution_rate * 10) - penalty
        return max(0, min(100, int(score)))

    def _calculate_system_health(self, tickets):
        """Calculate system health based on ticket resolution."""
        if not tickets:
            return 92  # Default health
        
        df = pd.DataFrame(tickets)
        resolved = len(df[df['status'] == 'Resolved'])
        total = len(df)
        resolution_rate = resolved / total if total > 0 else 1
        
        return int(resolution_rate * 100)

    def _calculate_data_quality(self, datasets):
        """Calculate average data quality score."""
        if not datasets:
            return 0.87  # Default quality
        
        df = pd.DataFrame(datasets)
        if 'quality_score' in df.columns:
            return df['quality_score'].mean() / 10
        return 0.87

    def _display_department_overview(self, incidents, tickets, datasets):
        """Display department activity overview chart."""
        departments = ['Cybersecurity', 'IT Operations', 'Data Science']
        active_items = [len(incidents), len(tickets), len(datasets)]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Active Items',
            x=departments,
            y=active_items,
            marker_color=['#ef4444', '#3b82f6', '#10b981']
        ))
        
        fig.update_layout(
            title="Department Activity Overview",
            xaxis_title="Department",
            yaxis_title="Number of Items",
            template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _display_security_trends(self, incidents):
        """Display security incident trends over time."""
        if incidents:
            df = pd.DataFrame(incidents)
            df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', errors='coerce')
            df = df.dropna(subset=['created_at'])  # Remove rows with invalid dates
            daily_incidents = df.groupby(df['created_at'].dt.date).size()
            
            fig = px.line(
                x=daily_incidents.index,
                y=daily_incidents.values,
                title="🛡️ Security Incidents Trend",
                labels={'x': 'Date', 'y': 'Incidents'}
            )
            
            fig.update_layout(
                template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No security incident data available.")

    def _display_system_health_metrics(self, tickets):
        """Display IT ticket status distribution."""
        if tickets:
            df = pd.DataFrame(tickets)
            status_counts = df['status'].value_counts()
            
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="💻 Ticket Status Distribution"
            )
            
            fig.update_layout(
                template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No IT ticket data available.")

    def _display_data_quality_metrics(self, datasets):
        """Display data quality metrics."""
        if datasets:
            df = pd.DataFrame(datasets)
            if 'quality_score' in df.columns:
                fig = px.histogram(
                    df, 
                    x='quality_score',
                    title="📊 Data Quality Score Distribution",
                    labels={'quality_score': 'Quality Score (1-10)'}
                )
                fig.update_layout(
                    template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No quality score data available.")
        else:
            st.info("No dataset data available.")

    def _display_sensitivity_distribution(self, datasets):
        """Display data sensitivity distribution."""
        if datasets:
            df = pd.DataFrame(datasets)
            if 'sensitivity' in df.columns:
                sens_counts = df['sensitivity'].value_counts()
                
                fig = px.pie(
                    values=sens_counts.values,
                    names=sens_counts.index,
                    title="🔐 Data Sensitivity Distribution"
                )
                
                fig.update_layout(
                    template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No sensitivity data available.")
        else:
            st.info("No dataset data available.")