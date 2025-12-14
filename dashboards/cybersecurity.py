"""
Cybersecurity Dashboard module for security incident management and analysis.
Provides threat monitoring, incident tracking, and security analytics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config import INCIDENT_SEVERITIES, INCIDENT_STATUSES, THREAT_TYPES
from utils.search_filter import filter_cyber_incidents
from utils.data_import import parse_csv_file, prepare_cyber_incident_data

class CyberSecurityDashboard:
    """Cybersecurity dashboard for incident management and threat analysis."""
    
    def __init__(self, db_manager, ai_engine):
        """Initialise cybersecurity dashboard with database and AI engine."""
        self.db = db_manager
        self.ai_engine = ai_engine

    def display(self):
        """Render the cybersecurity dashboard interface."""
        st.markdown("# 🛡️ Cybersecurity Dashboard")
        
        # Fetch incident data
        incidents_data = self.db.get_cyber_incidents()
        
        # Load sample data if none exists
        if not incidents_data:
            st.info("No security incidents data available")
            if st.button("Load Sample Data"):
                self._load_sample_cyber_data()
                st.rerun()
            return
        
        df = pd.DataFrame(incidents_data)
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"<div class='metric-card'><h3>Total Incidents</h3><h2 style='color: #6366f1;'>{len(df)}</h2></div>", unsafe_allow_html=True)
        
        with col2:
            open_incidents = len(df[df['status'] == 'Open'])
            st.markdown(f"<div class='metric-card'><h3>Open Incidents</h3><h2 style='color: #ef4444;'>{open_incidents}</h2></div>", unsafe_allow_html=True)
        
        with col3:
            critical = len(df[df['severity'] == 'Critical'])
            st.markdown(f"<div class='metric-card'><h3>Critical</h3><h2 style='color: #f59e0b;'>{critical}</h2></div>", unsafe_allow_html=True)
        
        with col4:
            avg_res = df['resolution_time_hours'].mean() if 'resolution_time_hours' in df.columns and not df['resolution_time_hours'].isna().all() else 0
            st.markdown(f"<div class='metric-card'><h3>Avg Resolution</h3><h2 style='color: #10b981;'>{avg_res:.1f}h</h2></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export CSV button
        col1, col2 = st.columns([1, 5])
        with col1:
            csv_data = df.to_csv(index=False)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📥 Export CSV",
                data=csv_data,
                file_name=f"cyber_incidents_{timestamp}.csv",
                mime="text/csv",
                key="export_cyber_csv"
            )
        
        st.markdown("---")
        
        # Dashboard Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "🛡️ Incidents", "➕ Add Incident", "📥 Import Data"])
        
        with tab1:
            self._show_cybersecurity_analytics(df)
        
        with tab2:
            self._show_incidents_list(incidents_data)
        
        with tab3:
            self._show_add_incident_form()
        
        with tab4:
            self._show_import_data()

    def _show_cybersecurity_analytics(self, df):
        """Display cybersecurity analytics and charts."""
        col1, col2 = st.columns(2)
        
        with col1:
            # Interactive Threat Type Distribution with customization
            if 'threat_type' in df.columns and not df.empty:
                threat_counts = df['threat_type'].value_counts()
                if not threat_counts.empty:
                    # Chart customization options
                    with st.expander("⚙️ Customise Chart", expanded=False):
                        chart_type = st.radio("Chart Type", ["Pie", "Bar", "Donut"], horizontal=True, key="threat_chart_type")
                        show_values = st.checkbox("Show Values", value=True, key="threat_show_values")
                    
                    if chart_type == "Pie":
                        fig_pie = px.pie(
                            values=threat_counts.values, 
                            names=threat_counts.index, 
                            title="Threat Type Distribution",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        if show_values:
                            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                        fig_pie.update_layout(
                            template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                            hovermode='closest'
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    elif chart_type == "Donut":
                        fig_donut = go.Figure(data=[go.Pie(
                            labels=threat_counts.index,
                            values=threat_counts.values,
                            hole=0.4,
                            textinfo='label+percent' if show_values else 'label'
                        )])
                        fig_donut.update_layout(
                            title="Threat Type Distribution (Donut)",
                            template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white"
                        )
                        st.plotly_chart(fig_donut, use_container_width=True)
                    else:  # Bar
                        fig_bar = px.bar(
                            x=threat_counts.index,
                            y=threat_counts.values,
                            title="Threat Type Distribution",
                            labels={'x': 'Threat Type', 'y': 'Count'},
                            text=threat_counts.values if show_values else None
                        )
                        fig_bar.update_layout(
                            template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                            xaxis_tickangle=-45
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No threat type data available")
            else:
                st.info("No threat type data available")
        
        with col2:
            # Severity Breakdown
            if 'severity' in df.columns and not df.empty:
                severity_counts = df['severity'].value_counts()
                if not severity_counts.empty:
                    fig_bar = px.bar(
                        x=severity_counts.index, 
                        y=severity_counts.values,
                        title="Severity Breakdown",
                        color=severity_counts.index,
                        color_discrete_map={
                            'Low': '#10b981',
                            'Medium': '#f59e0b',
                            'High': '#ef4444',
                            'Critical': '#dc2626'
                        }
                    )
                    fig_bar.update_layout(
                        showlegend=False,
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No severity data available")
            else:
                st.info("No severity data available")
        
        # Additional charts row
        st.markdown("---")
        col3, col4 = st.columns(2)
        
        with col3:
            # Threat Type vs Severity Heatmap
            if 'threat_type' in df.columns and 'severity' in df.columns and not df.empty:
                try:
                    heatmap_data = pd.crosstab(df['threat_type'], df['severity'])
                    fig_heatmap = go.Figure(data=go.Heatmap(
                        z=heatmap_data.values,
                        x=heatmap_data.columns,
                        y=heatmap_data.index,
                        colorscale='RdYlGn_r',
                        text=heatmap_data.values,
                        texttemplate='%{text}',
                        textfont={"size": 10}
                    ))
                    fig_heatmap.update_layout(
                        title="Threat Type vs Severity Heatmap",
                        xaxis_title="Severity",
                        yaxis_title="Threat Type",
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=400
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                except Exception as e:
                    st.info("Could not create heatmap")
        
        with col4:
            # Resolution Time by Threat Type
            if 'threat_type' in df.columns and 'resolution_time_hours' in df.columns and not df.empty:
                try:
                    resolution_df = df[df['resolution_time_hours'].notna()]
                    if not resolution_df.empty:
                        fig_scatter = px.scatter(
                            resolution_df,
                            x='threat_type',
                            y='resolution_time_hours',
                            color='severity',
                            size='resolution_time_hours',
                            title="Resolution Time by Threat Type",
                            labels={'resolution_time_hours': 'Resolution Time (hours)', 'threat_type': 'Threat Type'},
                            hover_data=['title']
                        )
                        fig_scatter.update_layout(
                            template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                            height=400
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    else:
                        st.info("No resolution time data available")
                except Exception as e:
                    st.info("Could not create scatter plot")
        
        # Status Over Time Area Chart
        if 'created_at' in df.columns and len(df) > 0:
            try:
                df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', errors='coerce')
                df = df.dropna(subset=['created_at'])
                df['date'] = df['created_at'].dt.date
                daily_status = df.groupby(['date', 'status']).size().unstack(fill_value=0)
                
                fig_area = go.Figure()
                for status in daily_status.columns:
                    fig_area.add_trace(go.Scatter(
                        x=daily_status.index,
                        y=daily_status[status],
                        mode='lines',
                        name=status,
                        stackgroup='one',
                        fill='tonexty' if status != daily_status.columns[0] else 'tozeroy'
                    ))
                
                fig_area.update_layout(
                    title="Incident Status Over Time (Area Chart)",
                    xaxis_title="Date",
                    yaxis_title="Number of Incidents",
                    template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                    height=400
                )
                st.plotly_chart(fig_area, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not create time chart: {str(e)}")
        
        # AI Analytics Section
        st.markdown("---")
        st.markdown("### 🤖 AI-Powered Analytics")
        
        ai_col1, ai_col2, ai_col3 = st.columns(3)
        
        with ai_col1:
            if st.button("📊 Analyse Patterns", key="analyse_patterns", use_container_width=True):
                with st.spinner("🤖 AI is analysing incident patterns..."):
                    if self.ai_engine and hasattr(self.ai_engine, 'analyse_incident_patterns'):
                        analysis = self.ai_engine.analyse_incident_patterns(df.to_dict('records'))
                        st.markdown("#### Analysis Results")
                        st.markdown(analysis)
                    else:
                        st.info("AI engine not available. Using basic analysis.")
        
        with ai_col2:
            if st.button("🔮 Predict Trends", key="predict_trends", use_container_width=True):
                with st.spinner("🤖 AI is predicting future trends..."):
                    if self.ai_engine and self.ai_engine.model:
                        try:
                            prompt = f"""Based on these {len(df)} security incidents, predict:
1. Likely future threat types
2. Expected incident volume trends
3. Areas requiring immediate attention
4. Risk assessment for next 30 days

Incident summary:
- Threat types: {df['threat_type'].value_counts().to_dict()}
- Severity distribution: {df['severity'].value_counts().to_dict()}
- Status: {df['status'].value_counts().to_dict()}
- Average resolution: {df['resolution_time_hours'].mean():.1f} hours

Provide actionable predictions and recommendations."""
                            prediction = self.ai_engine.chat_with_ai(prompt)
                            st.markdown("#### Trend Predictions")
                            st.markdown(prediction)
                        except Exception as e:
                            st.error(f"Error generating predictions: {str(e)}")
                    else:
                        st.info("AI engine not available.")
        
        with ai_col3:
            if st.button("💡 Get Recommendations", key="get_recommendations", use_container_width=True):
                with st.spinner("🤖 AI is generating recommendations..."):
                    if self.ai_engine and self.ai_engine.model:
                        try:
                            critical_count = len(df[df['severity'] == 'Critical'])
                            open_count = len(df[df['status'] == 'Open'])
                            prompt = f"""Provide specific, actionable security recommendations based on:
- {critical_count} critical incidents
- {open_count} open incidents
- Top threat: {df['threat_type'].mode()[0] if not df.empty else 'N/A'}
- Average resolution time: {df['resolution_time_hours'].mean():.1f} hours

Focus on immediate actions and long-term improvements."""
                            recommendations = self.ai_engine.chat_with_ai(prompt)
                            st.markdown("#### AI Recommendations")
                            st.markdown(recommendations)
                        except Exception as e:
                            st.error(f"Error generating recommendations: {str(e)}")
                    else:
                        st.info("AI engine not available.")

    def _show_incidents_list(self, incidents_data):
        """Display list of recent security incidents."""
        st.markdown("### Recent Security Incidents")
        
        # Search and filter options
        with st.expander("🔍 Search & Filter Options", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                search_term = st.text_input("🔎 Search", placeholder="Title, description, threat type...", key="search_incidents")
            
            with col2:
                threat_types_list = list(set([inc.get('threat_type', '') for inc in incidents_data if inc.get('threat_type')]))
                threat_types = ["All"] + sorted(threat_types_list) if threat_types_list else ["All"]
                filter_threat = st.selectbox("Threat Type", threat_types, key="filter_threat")
            
            with col3:
                filter_status = st.selectbox("Status", ["All"] + INCIDENT_STATUSES, key="filter_status")
            
            with col4:
                filter_severity = st.selectbox("Severity", ["All"] + INCIDENT_SEVERITIES, key="filter_severity")
            
            # Date range filter
            col5, col6 = st.columns(2)
            with col5:
                date_from = st.date_input("From Date", value=None, key="date_from")
            with col6:
                date_to = st.date_input("To Date", value=None, key="date_to")
        
        # Apply filters using utility function
        date_range = None
        if date_from and date_to:
            date_range = (datetime.combine(date_from, datetime.min.time()), 
                         datetime.combine(date_to, datetime.max.time()))
        
        filtered_incidents = filter_cyber_incidents(
            incidents_data,
            search_term=search_term,
            threat_type=filter_threat,
            severity=filter_severity,
            status=filter_status,
            date_range=date_range
        )
        
        # Show results count
        st.info(f"Showing {len(filtered_incidents)} of {len(incidents_data)} incidents")
        
        # Display incidents
        if not filtered_incidents:
            st.info("No incidents found matching your criteria.")
            return
            
        for incident in filtered_incidents[:20]:  # Limit to 20 for performance
            severity_color = {
                'Low': '#10b981',
                'Medium': '#f59e0b',
                'High': '#ef4444',
                'Critical': '#dc2626'
            }.get(incident['severity'], '#6b7280')
            
            status_color = {
                'Open': '#ef4444',
                'In Progress': '#f59e0b',
                'Resolved': '#10b981'
            }.get(incident['status'], '#6b7280')
            
            # FIXED: Removed unsafe_allow_html from expander
            with st.expander(f"**{incident['title']}** - {incident['severity']} - {incident['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {incident['description']}")
                    st.write(f"**Threat Type:** {incident['threat_type']}")
                    st.write(f"**Created:** {incident['created_at'][:10] if incident['created_at'] else 'N/A'}")
                    st.markdown(f"**Severity:** <span style='color:{severity_color}'>{incident['severity']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Status:** <span style='color:{status_color}'>{incident['status']}</span>", unsafe_allow_html=True)
                
                with col2:
                    st.write(f"**Assigned To:** {incident.get('assigned_to', 'Unassigned')}")
                    if incident.get('resolved_at'):
                        st.write(f"**Resolved:** {incident['resolved_at'][:10]}")
                    if incident.get('resolution_time_hours'):
                        st.write(f"**Resolution Time:** {incident['resolution_time_hours']} hours")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if incident['status'] != 'In Progress' and st.button("Start Progress", key=f"start_{incident['id']}"):
                        if self.db.update_incident_status(incident['id'], 'In Progress'):
                            st.success(f"Incident {incident['id']} marked as in progress!")
                            st.rerun()
                with col2:
                    if incident['status'] != 'Resolved' and st.button("Mark Resolved", key=f"resolve_{incident['id']}"):
                        if self.db.update_incident_status(incident['id'], 'Resolved'):
                            st.success(f"Incident {incident['id']} marked as resolved!")
                            st.rerun()
                with col3:
                    if st.button("Delete", key=f"delete_{incident['id']}"):
                        if self.db.delete_incident(incident['id']):
                            st.success(f"Incident {incident['id']} deleted!")
                            st.rerun()
                with col4:
                    if st.button("Refresh", key=f"refresh_{incident['id']}"):
                        st.rerun()

    def _show_add_incident_form(self):
        """Display form for adding new security incidents."""
        st.markdown("### Add New Security Incident")
        
        with st.form("add_incident_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                inc_title = st.text_input("Incident Title*", placeholder="Brief descriptive title", key="inc_title")
                inc_desc = st.text_area("Description*", placeholder="Detailed description of the incident", key="inc_desc")
                inc_threat = st.selectbox("Threat Type*", THREAT_TYPES, key="inc_threat")
            
            with col2:
                inc_severity = st.selectbox("Severity*", INCIDENT_SEVERITIES, key="inc_severity")
                inc_status = st.selectbox("Status*", INCIDENT_STATUSES, key="inc_status")
                inc_assigned = st.text_input("Assigned To", value="Security Team", key="inc_assigned")
            
            st.caption("* Required fields")
            
            submitted = st.form_submit_button("Add Incident", type="primary")
            
            if submitted:
                if inc_title and inc_desc:
                    new_incident = {
                        'title': inc_title,
                        'description': inc_desc,
                        'threat_type': inc_threat,
                        'severity': inc_severity,
                        'status': inc_status,
                        'created_at': datetime.now().isoformat(),
                        'assigned_to': inc_assigned
                    }
                    try:
                        incident_id = self.db.create_cyber_incident(new_incident)
                        st.success(f"✅ Incident '{inc_title}' added successfully! (ID: {incident_id})")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding incident: {str(e)}")
                else:
                    st.error("Please fill in all required fields.")

    def _show_import_data(self):
        """Display CSV import functionality."""
        st.markdown("### 📥 Import Cyber Incidents from CSV")
        st.markdown("Upload a CSV file to bulk import security incidents.")
        
        st.info("""
        **CSV Format Requirements:**
        - Required columns: `title`, `threat_type`, `severity`, `status`
        - Optional columns: `description`, `assigned_to`, `created_at`, `resolved_at`, `resolution_time_hours`
        - Severity values: Low, Medium, High, Critical
        - Status values: Open, In Progress, Resolved, Closed
        """)
        
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], key="import_cyber_csv")
        
        if uploaded_file is not None:
            try:
                success, df, error = parse_csv_file(uploaded_file, "cyber_incidents")
                
                if success:
                    st.success(f"✅ CSV file parsed successfully! Found {len(df)} rows.")
                    
                    # Preview data
                    st.markdown("**Preview of data to be imported:**")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    if st.button("Import All Records", type="primary", key="import_cyber_btn"):
                        incidents = prepare_cyber_incident_data(df)
                        imported_count = 0
                        errors = []
                        
                        for incident in incidents:
                            try:
                                self.db.create_cyber_incident(incident)
                                imported_count += 1
                            except Exception as e:
                                errors.append(f"Error importing {incident.get('title', 'Unknown')}: {str(e)}")
                        
                        if imported_count > 0:
                            st.success(f"✅ Successfully imported {imported_count} of {len(incidents)} incidents!")
                            if errors:
                                st.warning(f"⚠️ {len(errors)} errors occurred. Check details below.")
                                with st.expander("View Errors"):
                                    for error in errors[:10]:
                                        st.error(error)
                            st.rerun()
                        else:
                            st.error("❌ No incidents were imported. Please check the errors above.")
                else:
                    st.error(f"❌ CSV validation failed:\n{error}")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    def _load_sample_cyber_data(self):
        """Load sample cybersecurity data for demonstration."""
        sample_incidents = [
            {
                'title': 'Phishing Campaign Detected',
                'description': 'Multiple phishing emails targeting employees with fake login pages',
                'threat_type': 'Phishing',
                'severity': 'High',
                'status': 'Open',
                'created_at': datetime.now().isoformat(),
                'assigned_to': 'Security Team'
            },
            {
                'title': 'Malware Infection on Server',
                'description': 'Ransomware detected on production server, data encrypted',
                'threat_type': 'Malware',
                'severity': 'Critical',
                'status': 'In Progress',
                'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'assigned_to': 'Incident Response Team'
            },
            {
                'title': 'DDoS Attack Attempt',
                'description': 'Distributed Denial of Service attack on web servers',
                'threat_type': 'DDoS',
                'severity': 'Medium',
                'status': 'Resolved',
                'created_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'resolved_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'resolution_time_hours': 24,
                'assigned_to': 'Network Team'
            },
            {
                'title': 'Brute Force Attack on Admin Account',
                'description': 'Multiple failed login attempts detected on administrator account',
                'threat_type': 'Brute Force',
                'severity': 'High',
                'status': 'Open',
                'created_at': (datetime.now() - timedelta(hours=6)).isoformat(),
                'assigned_to': 'Security Team'
            },
            {
                'title': 'Suspicious Data Export Activity',
                'description': 'Unusual large data export detected from HR database',
                'threat_type': 'Data Breach',
                'severity': 'Critical',
                'status': 'In Progress',
                'created_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'assigned_to': 'Data Protection Team'
            }
        ]
        
        try:
            for incident in sample_incidents:
                self.db.create_cyber_incident(incident)
            
            st.success("✅ Sample cybersecurity data loaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading sample data: {str(e)}")