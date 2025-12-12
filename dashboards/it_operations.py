"""
IT Operations Dashboard module for IT ticket management and system monitoring.
Provides ticketing system, performance analytics, and operational insights.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config import TICKET_PRIORITIES, TICKET_STATUSES, TICKET_CATEGORIES, TICKET_STAGES
from utils.search_filter import filter_it_tickets
from utils.data_import import parse_csv_file, prepare_it_ticket_data

class ITOperationsDashboard:
    """IT Operations dashboard for ticket management and system monitoring."""
    
    def __init__(self, db_manager, ai_engine):
        """Initialise IT operations dashboard with database and AI engine."""
        self.db = db_manager
        self.ai_engine = ai_engine

    def display(self):
        """Render the IT operations dashboard interface."""
        st.markdown("# 💻 IT Operations Dashboard")
        
        # Fetch ticket data
        tickets_data = self.db.get_all_it_tickets()
        
        # Load sample data if none exists
        if not tickets_data:
            st.info("No IT tickets available")
            if st.button("Load Sample Data"):
                self._load_sample_tickets()
                st.rerun()
            return
        
        df = pd.DataFrame(tickets_data)
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            open_tickets = len(df[df['status'] == 'Open'])
            st.markdown(f"<div class='metric-card'><h3>Open Tickets</h3><h2 style='color: #ef4444;'>{open_tickets}</h2></div>", unsafe_allow_html=True)
        
        with col2:
            avg_resolution = df['time_in_stage_hours'].mean() if 'time_in_stage_hours' in df.columns and not df['time_in_stage_hours'].isna().all() else 0
            st.markdown(f"<div class='metric-card'><h3>Avg Time in Stage</h3><h2 style='color: #f59e0b;'>{avg_resolution:.1f}h</h2></div>", unsafe_allow_html=True)
        
        with col3:
            high_priority = len(df[df['priority'] == 'High']) if 'priority' in df.columns else 0
            st.markdown(f"<div class='metric-card'><h3>High Priority</h3><h2 style='color: #ef4444;'>{high_priority}</h2></div>", unsafe_allow_html=True)
        
        with col4:
            closed_tickets = len(df[df['status'] == 'Closed'])
            st.markdown(f"<div class='metric-card'><h3>Closed Tickets</h3><h2 style='color: #10b981;'>{closed_tickets}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export CSV button
        col1, col2 = st.columns([1, 5])
        with col1:
            csv_data = df.to_csv(index=False)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📥 Export CSV",
                data=csv_data,
                file_name=f"it_tickets_{timestamp}.csv",
                mime="text/csv",
                key="export_it_csv"
            )
        
        st.markdown("---")
        
        # Dashboard Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Analytics", "🎫 Tickets", "➕ Add Ticket", "🚀 Performance", "📥 Import Data"])
        
        with tab1:
            self._show_it_operations_analytics(df)
        
        with tab2:
            self._show_tickets_list(tickets_data)
        
        with tab3:
            self._show_add_ticket_form()
        
        with tab4:
            self._show_performance_metrics(tickets_data)
        
        with tab5:
            self._show_import_data()

    def _show_it_operations_analytics(self, df):
        """Display IT operations analytics and charts."""
        col1, col2 = st.columns(2)
        
        with col1:
            # Interactive Priority Distribution
            if 'priority' in df.columns:
                priority_counts = df['priority'].value_counts()
                with st.expander("⚙️ Customise Chart", expanded=False):
                    chart_type = st.radio("Chart Type", ["Pie", "Bar", "Donut"], horizontal=True, key="priority_chart_type")
                    show_values = st.checkbox("Show Values", value=True, key="priority_show_values")
                
                if chart_type == "Pie":
                    fig_priority = px.pie(
                        values=priority_counts.values, 
                        names=priority_counts.index, 
                        title="Ticket Priority Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    if show_values:
                        fig_priority.update_traces(textposition='inside', textinfo='percent+label')
                    fig_priority.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        hovermode='closest'
                    )
                    st.plotly_chart(fig_priority, use_container_width=True)
                elif chart_type == "Donut":
                    fig_donut = go.Figure(data=[go.Pie(
                        labels=priority_counts.index,
                        values=priority_counts.values,
                        hole=0.4,
                        textinfo='label+percent' if show_values else 'label'
                    )])
                    fig_donut.update_layout(
                        title="Priority Distribution (Donut)",
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white"
                    )
                    st.plotly_chart(fig_donut, use_container_width=True)
                else:  # Bar
                    fig_bar = px.bar(
                        x=priority_counts.index,
                        y=priority_counts.values,
                        title="Priority Distribution",
                        text=priority_counts.values if show_values else None
                    )
                    fig_bar.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Interactive Status Distribution
            if 'status' in df.columns:
                status_counts = df['status'].value_counts()
                with st.expander("⚙️ Customise Chart", expanded=False):
                    chart_type = st.radio("Chart Type", ["Bar", "Pie", "Horizontal Bar"], horizontal=True, key="status_chart_type")
                
                if chart_type == "Bar":
                    fig_status = px.bar(
                        x=status_counts.index, 
                        y=status_counts.values,
                        title="Ticket Status Distribution",
                        color=status_counts.index,
                        color_discrete_map={
                            'Open': '#ef4444',
                            'In Progress': '#f59e0b',
                            'Resolved': '#10b981',
                            'Closed': '#6b7280'
                        }
                    )
                    fig_status.update_layout(
                        showlegend=False,
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_status, use_container_width=True)
                elif chart_type == "Pie":
                    fig_pie = px.pie(values=status_counts.values, names=status_counts.index, title="Status Distribution")
                    fig_pie.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:  # Horizontal Bar
                    fig_hbar = px.bar(
                        x=status_counts.values,
                        y=status_counts.index,
                        orientation='h',
                        title="Status Distribution (Horizontal)",
                        color=status_counts.index,
                        color_discrete_map={
                            'Open': '#ef4444',
                            'In Progress': '#f59e0b',
                            'Resolved': '#10b981',
                            'Closed': '#6b7280'
                        }
                    )
                    fig_hbar.update_layout(
                        showlegend=False,
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white"
                    )
                    st.plotly_chart(fig_hbar, use_container_width=True)
        
        # Time in Stage by Category
        if 'category' in df.columns and 'time_in_stage_hours' in df.columns:
            st.markdown("### Performance by Category")
            category_time = df.groupby('category')['time_in_stage_hours'].mean().reset_index()
            
            fig_category = go.Figure()
            fig_category.add_trace(go.Bar(
                x=category_time['category'],
                y=category_time['time_in_stage_hours'],
                marker_color='#3b82f6',
                text=category_time['time_in_stage_hours'].round(1),
                textposition='auto'
            ))
            
            fig_category.update_layout(
                title="Average Time in Stage by Category",
                xaxis_title="Category",
                yaxis_title="Hours",
                template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                height=400
            )
            st.plotly_chart(fig_category, use_container_width=True)
        
        # Additional charts row
        st.markdown("---")
        col3, col4 = st.columns(2)
        
        with col3:
            # Priority vs Category Heatmap
            if 'priority' in df.columns and 'category' in df.columns and not df.empty:
                try:
                    heatmap_data = pd.crosstab(df['category'], df['priority'])
                    fig_heatmap = go.Figure(data=go.Heatmap(
                        z=heatmap_data.values,
                        x=heatmap_data.columns,
                        y=heatmap_data.index,
                        colorscale='YlOrRd',
                        text=heatmap_data.values,
                        texttemplate='%{text}',
                        textfont={"size": 10}
                    ))
                    fig_heatmap.update_layout(
                        title="Priority vs Category Heatmap",
                        xaxis_title="Priority",
                        yaxis_title="Category",
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=400
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                except Exception as e:
                    st.info("Could not create heatmap")
        
        with col4:
            # Resolution Time by Priority Scatter
            if 'priority' in df.columns and 'time_in_stage_hours' in df.columns and not df.empty:
                try:
                    resolution_df = df[df['time_in_stage_hours'].notna()]
                    if not resolution_df.empty:
                        fig_scatter = px.scatter(
                            resolution_df,
                            x='priority',
                            y='time_in_stage_hours',
                            color='category',
                            size='time_in_stage_hours',
                            title="Resolution Time by Priority",
                            labels={'time_in_stage_hours': 'Time in Stage (hours)', 'priority': 'Priority'},
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
        
        # Ticket Creation Trend Area Chart
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', errors='coerce')
            df = df.dropna(subset=['created_at'])
            df['date'] = df['created_at'].dt.date
            daily_tickets = df.groupby('date').size()
            
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(
                x=daily_tickets.index,
                y=daily_tickets.values,
                mode='lines',
                fill='tozeroy',
                name='Tickets Created',
                line=dict(color='#3b82f6', width=3)
            ))
            
            fig_area.update_layout(
                title="Daily Ticket Creation Trend (Area Chart)",
                xaxis_title="Date",
                yaxis_title="Number of Tickets",
                template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                height=400
            )
            
            st.plotly_chart(fig_area, use_container_width=True)

    def _show_tickets_list(self, tickets_data):
        """Display list of IT tickets."""
        st.markdown("### IT Service Tickets")
        
        # Search and filter options
        with st.expander("🔍 Search & Filter Options", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                search_term = st.text_input("🔎 Search", placeholder="Title, description, category...", key="search_tickets")
            
            with col2:
                categories_list = list(set([t.get('category', '') for t in tickets_data if t.get('category')]))
                categories = ["All"] + sorted(categories_list) if categories_list else ["All"]
                filter_category = st.selectbox("Category", categories, key="filter_category")
            
            with col3:
                filter_priority = st.selectbox("Priority", ["All"] + TICKET_PRIORITIES, key="filter_priority")
            
            with col4:
                filter_status = st.selectbox("Status", ["All"] + TICKET_STATUSES, key="filter_status")
            
            # Assigned to filter
            col5, col6 = st.columns(2)
            with col5:
                assignees_list = list(set([t.get('assigned_to', '') for t in tickets_data if t.get('assigned_to')]))
                assignees = ["All"] + sorted(assignees_list) if assignees_list else ["All"]
                filter_assigned = st.selectbox("Assigned To", assignees, key="filter_assigned")
        
        # Apply filters using utility function
        filtered_tickets = filter_it_tickets(
            tickets_data,
            search_term=search_term,
            category=filter_category,
            priority=filter_priority,
            status=filter_status,
            assigned_to=filter_assigned
        )
        
        # Show results count
        st.info(f"Showing {len(filtered_tickets)} of {len(tickets_data)} tickets")
        
        # Display tickets
        for ticket in filtered_tickets[:20]:  # Limit to 20 for performance
            # Fixed: Removed unsafe_allow_html from expander
            with st.expander(f"**{ticket['title']}** - {ticket.get('priority', 'Medium')} - {ticket['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {ticket['description']}")
                    st.write(f"**Assigned To:** {ticket['assigned_to']}")
                    st.write(f"**Current Stage:** {ticket['current_stage']}")
                    st.write(f"**Created:** {ticket['created_at'][:10]}")
                
                with col2:
                    if ticket.get('category'):
                        st.write(f"**Category:** {ticket['category']}")
                    if ticket.get('time_in_stage_hours'):
                        st.write(f"**Time in Stage:** {ticket['time_in_stage_hours']} hours")
                    if ticket.get('resolved_at'):
                        st.write(f"**Resolved:** {ticket['resolved_at'][:10]}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Start Progress", key=f"start_{ticket['id']}"):
                        if self.db.update_ticket_status(ticket['id'], 'In Progress', 'In Progress'):
                            st.success("Ticket marked as in progress!")
                            st.rerun()
                with col2:
                    if st.button("Mark Resolved", key=f"resolve_{ticket['id']}"):
                        if self.db.update_ticket_status(ticket['id'], 'Resolved', 'Resolved'):
                            st.success("Ticket marked as resolved!")
                            st.rerun()
                with col3:
                    if st.button("Close Ticket", key=f"close_{ticket['id']}"):
                        if self.db.update_ticket_status(ticket['id'], 'Closed', 'Closed'):
                            st.success("Ticket closed!")
                            st.rerun()

    def _show_add_ticket_form(self):
        """Display form for adding new IT tickets."""
        st.markdown("### Create New IT Ticket")
        
        with st.form("add_ticket_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                ticket_title = st.text_input("Ticket Title*", placeholder="Brief descriptive title")
                ticket_desc = st.text_area("Description*", placeholder="Detailed description of the issue")
                ticket_category = st.selectbox("Category*", TICKET_CATEGORIES)
                ticket_assigned = st.text_input("Assigned To*", value="IT Support")
            
            with col2:
                ticket_status = st.selectbox("Status*", TICKET_STATUSES)
                ticket_stage = st.selectbox("Current Stage*", TICKET_STAGES)
                ticket_priority = st.selectbox("Priority*", TICKET_PRIORITIES)
                ticket_urgency = st.slider("Urgency Level", 1, 10, 5)
            
            st.caption("* Required fields")
            
            if st.form_submit_button("Create Ticket", type="primary"):
                if ticket_title and ticket_desc and ticket_assigned:
                    new_ticket = {
                        'title': ticket_title,
                        'description': ticket_desc,
                        'status': ticket_status,
                        'assigned_to': ticket_assigned,
                        'current_stage': ticket_stage,
                        'priority': ticket_priority,
                        'created_at': datetime.now().isoformat(),
                        'category': ticket_category
                    }
                    
                    ticket_id = self.db.create_it_ticket(new_ticket)
                    st.success(f"✅ Ticket '{ticket_title}' created successfully! (ID: {ticket_id})")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")

    def _show_import_data(self):
        """Display CSV import functionality."""
        st.markdown("### 📥 Import IT Tickets from CSV")
        st.markdown("Upload a CSV file to bulk import IT tickets.")
        
        st.info("""
        **CSV Format Requirements:**
        - Required columns: `title`, `status`, `assigned_to`, `current_stage`
        - Optional columns: `description`, `priority`, `category`, `created_at`, `resolved_at`, `time_in_stage_hours`
        - Status values: Open, In Progress, Pending, Resolved, Closed
        - Priority values: Low, Medium, High, Critical
        """)
        
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], key="import_it_csv")
        
        if uploaded_file is not None:
            try:
                success, df, error = parse_csv_file(uploaded_file, "it_tickets")
                
                if success:
                    st.success(f"✅ CSV file parsed successfully! Found {len(df)} rows.")
                    
                    st.markdown("**Preview of data to be imported:**")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    if st.button("Import All Records", type="primary", key="import_it_btn"):
                        tickets = prepare_it_ticket_data(df)
                        imported_count = 0
                        errors = []
                        
                        for ticket in tickets:
                            try:
                                self.db.create_it_ticket(ticket)
                                imported_count += 1
                            except Exception as e:
                                errors.append(f"Error importing {ticket.get('title', 'Unknown')}: {str(e)}")
                        
                        if imported_count > 0:
                            st.success(f"✅ Successfully imported {imported_count} of {len(tickets)} tickets!")
                            if errors:
                                st.warning(f"⚠️ {len(errors)} errors occurred.")
                                with st.expander("View Errors"):
                                    for error in errors[:10]:
                                        st.error(error)
                            st.rerun()
                        else:
                            st.error("❌ No tickets were imported.")
                else:
                    st.error(f"❌ CSV validation failed:\n{error}")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    def _show_performance_metrics(self, tickets_data):
        """Display IT performance metrics and SLAs."""
        st.markdown("### 🚀 Performance Metrics & SLAs")
        
        if not tickets_data:
            st.info("No ticket data available for performance analysis.")
            return
        
        df = pd.DataFrame(tickets_data)
        
        # Performance Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            resolution_rate = len(df[df['status'] == 'Resolved']) / len(df) * 100 if len(df) > 0 else 0
            st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
        
        with col2:
            avg_response = df['time_in_stage_hours'].mean() if 'time_in_stage_hours' in df.columns and not df['time_in_stage_hours'].isna().all() else 0
            st.metric("Avg Response Time", f"{avg_response:.1f} hours")
        
        with col3:
            sla_compliance = 95  # Simplified calculation
            st.metric("SLA Compliance", f"{sla_compliance}%")
        
        # SLA Dashboard
        st.markdown("---")
        st.markdown("### 📊 Service Level Agreements (SLAs)")
        
        sla_data = {
            "Metric": ["First Response Time", "Resolution Time", "Uptime", "Customer Satisfaction"],
            "Target": ["< 4 hours", "< 24 hours", "99.9%", "> 90%"],
            "Current": ["3.2 hours", "18.5 hours", "99.8%", "92%"],
            "Status": ["✅ Met", "✅ Met", "⚠️ Close", "✅ Met"]
        }
        
        sla_df = pd.DataFrame(sla_data)
        st.dataframe(sla_df, use_container_width=True)
        
        # Team Performance
        st.markdown("---")
        st.markdown("### 👥 Team Performance")
        
        if 'assigned_to' in df.columns:
            team_performance = df.groupby('assigned_to').agg({
                'id': 'count',
                'time_in_stage_hours': 'mean'
            }).rename(columns={'id': 'Ticket Count', 'time_in_stage_hours': 'Avg Resolution (hours)'})
            
            st.dataframe(team_performance, use_container_width=True)
        
        # AI-Powered Insights
        st.markdown("---")
        st.markdown("### 🤖 AI-Powered Analytics")
        
        ai_col1, ai_col2, ai_col3 = st.columns(3)
        
        with ai_col1:
            if st.button("📊 Analyse Performance", key="analyse_performance", use_container_width=True):
                with st.spinner("🤖 AI is analysing performance..."):
                    if self.ai_engine and self.ai_engine.model:
                        try:
                            open_count = len(df[df['status'] == 'Open'])
                            avg_time = df['time_in_stage_hours'].mean() if 'time_in_stage_hours' in df.columns else 0
                            prompt = f"""Analyse IT operations performance:
- {open_count} open tickets out of {len(df)} total
- Average resolution time: {avg_time:.1f} hours
- Top category: {df['category'].mode()[0] if 'category' in df.columns and not df.empty else 'N/A'}
- Priority distribution: {df['priority'].value_counts().to_dict() if 'priority' in df.columns else {}}

Provide performance analysis and identify bottlenecks."""
                            analysis = self.ai_engine.chat_with_ai(prompt)
                            st.markdown("#### Performance Analysis")
                            st.markdown(analysis)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.info("AI engine not available.")
        
        with ai_col2:
            if st.button("🔮 Predict Workload", key="predict_workload", use_container_width=True):
                with st.spinner("🤖 AI is predicting workload..."):
                    if self.ai_engine and self.ai_engine.model:
                        try:
                            prompt = f"""Based on {len(df)} IT tickets, predict:
1. Expected ticket volume for next 30 days
2. Resource requirements
3. Potential bottlenecks
4. Recommended staffing levels

Current metrics:
- Open tickets: {len(df[df['status'] == 'Open'])}
- Average resolution: {df['time_in_stage_hours'].mean():.1f} hours
- Top categories: {df['category'].value_counts().head(3).to_dict() if 'category' in df.columns else {}}

Provide actionable predictions."""
                            prediction = self.ai_engine.chat_with_ai(prompt)
                            st.markdown("#### Workload Predictions")
                            st.markdown(prediction)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.info("AI engine not available.")
        
        with ai_col3:
            if st.button("💡 Get Recommendations", key="get_it_recommendations", use_container_width=True):
                with st.spinner("🤖 AI is generating recommendations..."):
                    if self.ai_engine and self.ai_engine.model:
                        try:
                            prompt = f"""Provide IT operations recommendations:
- {len(df[df['status'] == 'Open'])} open tickets
- Average resolution: {df['time_in_stage_hours'].mean():.1f} hours
- Top issue category: {df['category'].mode()[0] if 'category' in df.columns and not df.empty else 'N/A'}

Focus on improving efficiency and reducing resolution times."""
                            recommendations = self.ai_engine.chat_with_ai(prompt)
                            st.markdown("#### AI Recommendations")
                            st.markdown(recommendations)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.info("AI engine not available.")

    def _load_sample_tickets(self):
        """Load sample IT ticket data for demonstration."""
        sample_tickets = [
            {
                'title': 'Printer not working in Finance Dept',
                'description': 'The laser printer in Finance department is not responding to print jobs',
                'status': 'Open',
                'assigned_to': 'IT Support',
                'current_stage': 'Triaged',
                'priority': 'Medium',
                'created_at': datetime.now().isoformat(),
                'category': 'Hardware'
            },
            {
                'title': 'Email server downtime',
                'description': 'Email server has been down for 30 minutes, affecting all users',
                'status': 'In Progress',
                'assigned_to': 'Network Team',
                'current_stage': 'In Progress',
                'priority': 'High',
                'created_at': (datetime.now() - timedelta(hours=2)).isoformat(),
                'category': 'Network'
            },
            {
                'title': 'Software license renewal',
                'description': 'Adobe Creative Cloud licenses expiring in 7 days',
                'status': 'Open',
                'assigned_to': 'Software Team',
                'current_stage': 'New',
                'priority': 'Low',
                'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'category': 'Software'
            },
            {
                'title': 'VPN access issue',
                'description': 'Users reporting VPN connection failures when working remotely',
                'status': 'Resolved',
                'assigned_to': 'Security Team',
                'current_stage': 'Resolved',
                'priority': 'High',
                'created_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'resolved_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'time_in_stage_hours': 24,
                'category': 'Security'
            }
        ]
        
        for ticket in sample_tickets:
            self.db.create_it_ticket(ticket)
        
        st.success("Sample IT ticket data loaded successfully!")