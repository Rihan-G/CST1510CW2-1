"""
Data Science Dashboard module for dataset management and analytics.
Provides data quality monitoring, dataset tracking, and analytics insights.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config import DATA_DEPARTMENTS, SENSITIVITY_LEVELS, QUALITY_SCORE_RANGE
from utils.search_filter import filter_datasets
from utils.data_import import parse_csv_file, prepare_dataset_data

class DataScienceDashboard:
    """Data Science dashboard for dataset management and analytics."""
    
    def __init__(self, db_manager, ai_engine):
        """Initialise data science dashboard with database and AI engine."""
        self.db = db_manager
        self.ai_engine = ai_engine

    def display(self):
        """Render the data science dashboard interface."""
        st.markdown("# 📊 Data Science Dashboard")
        
        # Fetch dataset data
        datasets_data = self.db.get_all_datasets()
        
        # Load sample data if none exists
        if not datasets_data:
            st.info("No datasets available")
            if st.button("Load Sample Data"):
                self._load_sample_datasets()
                st.rerun()
            return
        
        df = pd.DataFrame(datasets_data)
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_size = df['size_mb'].sum()
            st.markdown(f"<div class='metric-card'><h3>Total Data Size</h3><h2 style='color: #6366f1;'>{total_size:.1f} MB</h2></div>", unsafe_allow_html=True)
        
        with col2:
            avg_quality = df['quality_score'].mean() if 'quality_score' in df.columns and not df['quality_score'].isna().all() else 0
            st.markdown(f"<div class='metric-card'><h3>Avg Quality Score</h3><h2 style='color: #10b981;'>{avg_quality:.1f}/10</h2></div>", unsafe_allow_html=True)
        
        with col3:
            total_rows = df['row_count'].sum()
            st.markdown(f"<div class='metric-card'><h3>Total Rows</h3><h2 style='color: #f59e0b;'>{total_rows:,}</h2></div>", unsafe_allow_html=True)
        
        with col4:
            high_sensitivity = len(df[df['sensitivity'] == 'High']) if 'sensitivity' in df.columns else 0
            st.markdown(f"<div class='metric-card'><h3>High Sensitivity</h3><h2 style='color: #ef4444;'>{high_sensitivity}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export CSV button
        col1, col2 = st.columns([1, 5])
        with col1:
            csv_data = df.to_csv(index=False)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📥 Export CSV",
                data=csv_data,
                file_name=f"datasets_{timestamp}.csv",
                mime="text/csv",
                key="export_data_csv"
            )
        
        st.markdown("---")
        
        # Dashboard Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Analytics", "📁 Datasets", "➕ Add Dataset", "🔍 Data Quality", "📥 Import Data"])
        
        with tab1:
            self._show_data_science_analytics(df)
        
        with tab2:
            self._show_datasets_list(datasets_data)
        
        with tab3:
            self._show_add_dataset_form()
        
        with tab4:
            self._show_data_quality_analysis(datasets_data)
        
        with tab5:
            self._show_import_data()

    def _show_data_science_analytics(self, df):
        """Display data science analytics and charts."""
        col1, col2 = st.columns(2)
        
        with col1:
            # Interactive Dataset Size Distribution
            if 'size_mb' in df.columns and len(df) > 0:
                with st.expander("⚙️ Customise Chart", expanded=False):
                    chart_type = st.radio("Chart Type", ["Histogram", "Box Plot", "Violin"], horizontal=True, key="size_chart_type")
                    bins = st.slider("Number of Bins", 5, 50, 20, key="size_bins")
                
                if chart_type == "Histogram":
                    fig_size = px.histogram(
                        df, 
                        x='size_mb', 
                        title="Dataset Size Distribution (MB)",
                        labels={'size_mb': 'Size (MB)'},
                        color_discrete_sequence=['#6366f1'],
                        nbins=bins
                    )
                    fig_size.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=300,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_size, use_container_width=True)
                elif chart_type == "Box Plot":
                    fig_box = px.box(df, y='size_mb', title="Dataset Size Distribution (Box Plot)")
                    fig_box.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=300
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                else:  # Violin
                    fig_violin = px.violin(df, y='size_mb', title="Dataset Size Distribution (Violin Plot)", box=True)
                    fig_violin.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=300
                    )
                    st.plotly_chart(fig_violin, use_container_width=True)
            else:
                st.info("No size data available")
        
        with col2:
            # Interactive Quality Score Distribution
            if 'quality_score' in df.columns and len(df) > 0:
                with st.expander("⚙️ Customise Chart", expanded=False):
                    chart_type = st.radio("Chart Type", ["Box Plot", "Histogram", "Violin"], horizontal=True, key="quality_chart_type")
                
                if chart_type == "Box Plot":
                    fig_quality = px.box(
                        df, 
                        y='quality_score', 
                        title="Data Quality Score Distribution",
                        labels={'quality_score': 'Quality Score (1-10)'},
                        color_discrete_sequence=['#10b981']
                    )
                    fig_quality.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=300,
                        hovermode='y unified'
                    )
                    st.plotly_chart(fig_quality, use_container_width=True)
                elif chart_type == "Histogram":
                    fig_hist = px.histogram(df, x='quality_score', title="Quality Score Distribution", nbins=20)
                    fig_hist.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=300
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:  # Violin
                    fig_violin = px.violin(df, y='quality_score', title="Quality Score Distribution (Violin)", box=True)
                    fig_violin.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=300
                    )
                    st.plotly_chart(fig_violin, use_container_width=True)
            else:
                st.info("No quality score data available")
        
        # Department-wise Data Volume
        if 'source_department' in df.columns and 'size_mb' in df.columns and len(df) > 0:
            st.markdown("### Department Data Volume")
            dept_data = df.groupby('source_department').agg({
                'size_mb': 'sum',
                'row_count': 'sum',
                'quality_score': 'mean'
            }).reset_index()
            
            fig_dept = go.Figure()
            fig_dept.add_trace(go.Bar(
                x=dept_data['source_department'],
                y=dept_data['size_mb'],
                name='Total Size (MB)',
                marker_color='#6366f1'
            ))
            
            fig_dept.update_layout(
                title="Data Volume by Department",
                xaxis_title="Department",
                yaxis_title="Size (MB)",
                template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                height=400
            )
            st.plotly_chart(fig_dept, use_container_width=True)
        
        # Additional charts row
        st.markdown("---")
        col3, col4 = st.columns(2)
        
        with col3:
            # Quality Score Distribution by Department
            if 'source_department' in df.columns and 'quality_score' in df.columns and not df.empty:
                try:
                    fig_violin = px.violin(
                        df,
                        x='source_department',
                        y='quality_score',
                        title="Quality Score Distribution by Department",
                        labels={'source_department': 'Department', 'quality_score': 'Quality Score'},
                        box=True
                    )
                    fig_violin.update_layout(
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=400
                    )
                    st.plotly_chart(fig_violin, use_container_width=True)
                except Exception as e:
                    st.info("Could not create violin plot")
        
        with col4:
            # Sensitivity vs Quality Heatmap
            if 'sensitivity' in df.columns and 'quality_score' in df.columns and not df.empty:
                try:
                    sensitivity_bins = pd.cut(df['quality_score'], bins=[0, 5, 7, 9, 10], labels=['Low', 'Medium', 'High', 'Excellent'])
                    heatmap_data = pd.crosstab(df['sensitivity'], sensitivity_bins)
                    fig_heatmap = go.Figure(data=go.Heatmap(
                        z=heatmap_data.values,
                        x=heatmap_data.columns,
                        y=heatmap_data.index,
                        colorscale='Viridis',
                        text=heatmap_data.values,
                        texttemplate='%{text}',
                        textfont={"size": 10}
                    ))
                    fig_heatmap.update_layout(
                        title="Sensitivity vs Quality Score Heatmap",
                        xaxis_title="Quality Level",
                        yaxis_title="Sensitivity",
                        template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                        height=400
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                except Exception as e:
                    st.info("Could not create heatmap")
        
        # Interactive Row Count vs Quality Score Scatter
        if 'row_count' in df.columns and 'quality_score' in df.columns and len(df) > 0:
            st.markdown("### Data Size vs Quality Analysis")
            with st.expander("⚙️ Customise Chart", expanded=False):
                x_axis = st.selectbox("X-Axis", ['row_count', 'size_mb', 'column_count'], key="scatter_x")
                y_axis = st.selectbox("Y-Axis", ['quality_score', 'row_count', 'size_mb'], key="scatter_y")
                color_by = st.selectbox("Color By", ['source_department', 'sensitivity', 'quality_score'], key="scatter_color")
                size_by = st.selectbox("Size By", ['size_mb', 'row_count', 'quality_score'], key="scatter_size")
            
            fig_scatter = px.scatter(
                df,
                x=x_axis,
                y=y_axis,
                size=size_by,
                color=color_by,
                title=f"{y_axis.replace('_', ' ').title()} vs {x_axis.replace('_', ' ').title()}",
                labels={
                    x_axis: x_axis.replace('_', ' ').title(),
                    y_axis: y_axis.replace('_', ' ').title(),
                    size_by: size_by.replace('_', ' ').title(),
                    color_by: color_by.replace('_', ' ').title()
                },
                hover_data=['name']
            )
            fig_scatter.update_layout(
                template="plotly_dark" if st.session_state.get('dark_mode', True) else "plotly_white",
                height=400,
                hovermode='closest'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    def _show_datasets_list(self, datasets_data):
        """Display list of available datasets."""
        st.markdown("### Available Datasets")
        
        # Search and filter options
        with st.expander("🔍 Search & Filter Options", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                search_term = st.text_input("🔎 Search", placeholder="Name, department, sensitivity...", key="search_datasets")
            
            with col2:
                departments_list = list(set([ds.get('source_department', '') for ds in datasets_data if ds.get('source_department')]))
                departments = ["All"] + sorted(departments_list) if departments_list else ["All"]
                filter_dept = st.selectbox("Department", departments, key="filter_dept")
            
            with col3:
                filter_sensitivity = st.selectbox("Sensitivity", ["All"] + SENSITIVITY_LEVELS, key="filter_sensitivity")
            
            with col4:
                quality_range = st.slider("Quality Score Range", 0.0, 10.0, (0.0, 10.0), 0.1, key="quality_range")
        
        # Apply filters using utility function
        filtered_datasets = filter_datasets(
            datasets_data,
            search_term=search_term,
            department=filter_dept,
            min_quality=quality_range[0],
            max_quality=quality_range[1],
            sensitivity=filter_sensitivity
        )
        
        # Show results count
        st.info(f"Showing {len(filtered_datasets)} of {len(datasets_data)} datasets")
        
        # Display datasets
        if not filtered_datasets:
            st.info("No datasets found matching your criteria.")
            return
            
        for dataset in filtered_datasets[:20]:  # Limit to 20 for performance
            sensitivity_color = {
                'Low': '#10b981',
                'Medium': '#f59e0b',
                'High': '#ef4444',
                'Confidential': '#dc2626'
            }.get(dataset.get('sensitivity'), '#6b7280')
            
            # Fixed: Removed unsafe_allow_html from expander
            with st.expander(f"**{dataset['name']}** - {dataset['source_department']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Size:** {dataset['size_mb']} MB")
                    st.write(f"**Rows:** {dataset['row_count']:,}")
                    st.write(f"**Columns:** {dataset['column_count']}")
                    st.write(f"**Created:** {dataset['created_at'][:10] if dataset['created_at'] else 'N/A'}")
                
                with col2:
                    if dataset.get('quality_score'):
                        quality_color = '#10b981' if dataset['quality_score'] >= 7 else '#f59e0b' if dataset['quality_score'] >= 5 else '#ef4444'
                        st.markdown(f"**Quality Score:** <span style='color:{quality_color}'>{dataset['quality_score']}/10</span>", unsafe_allow_html=True)
                    if dataset.get('sensitivity'):
                        st.markdown(f"**Sensitivity:** <span style='color:{sensitivity_color}'>{dataset['sensitivity']}</span>", unsafe_allow_html=True)
                    
                    if dataset.get('last_accessed'):
                        st.write(f"**Last Accessed:** {dataset['last_accessed'][:10]}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("View Details", key=f"view_{dataset['id']}"):
                        st.info(f"Showing details for {dataset['name']}")
                with col2:
                    if st.button("Update Quality", key=f"update_{dataset['id']}"):
                        with st.form(key=f"update_form_{dataset['id']}"):
                            new_score = st.slider(
                                "New Quality Score", 
                                min_value=QUALITY_SCORE_RANGE[0], 
                                max_value=QUALITY_SCORE_RANGE[1], 
                                value=float(dataset.get('quality_score', 5)),
                                key=f"score_{dataset['id']}"
                            )
                            if st.form_submit_button("Save"):
                                if self.db.update_dataset_quality(dataset['id'], new_score):
                                    st.success("Quality score updated!")
                                    st.rerun()
                with col3:
                    if st.button("Delete", key=f"delete_{dataset['id']}"):
                        if self.db.delete_dataset(dataset['id']):
                            st.success("Dataset deleted!")
                            st.rerun()

    def _show_add_dataset_form(self):
        """Display form for adding new datasets."""
        st.markdown("### Add New Dataset")
        
        with st.form("add_dataset_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                ds_name = st.text_input("Dataset Name*", placeholder="Descriptive name for the dataset", key="ds_name")
                ds_dept = st.selectbox("Source Department*", DATA_DEPARTMENTS, key="ds_dept")
                ds_size = st.number_input("Size (MB)*", min_value=0.1, value=10.0, step=0.1, key="ds_size")
                ds_rows = st.number_input("Number of Rows*", min_value=1, value=1000, step=100, key="ds_rows")
            
            with col2:
                ds_cols = st.number_input("Number of Columns*", min_value=1, value=10, key="ds_cols")
                ds_quality = st.slider(
                    "Quality Score (1-10)*", 
                    QUALITY_SCORE_RANGE[0], 
                    QUALITY_SCORE_RANGE[1], 
                    value=7,
                    key="ds_quality"
                )
                ds_sensitivity = st.selectbox("Sensitivity Level*", SENSITIVITY_LEVELS, key="ds_sensitivity")
                ds_description = st.text_area("Description", placeholder="Optional description of the dataset", key="ds_description")
            
            st.caption("* Required fields")
            
            submitted = st.form_submit_button("Add Dataset", type="primary")
            
            if submitted:
                if ds_name and ds_dept:
                    new_dataset = {
                        'name': ds_name,
                        'source_department': ds_dept,
                        'size_mb': ds_size,
                        'row_count': ds_rows,
                        'column_count': ds_cols,
                        'quality_score': ds_quality,
                        'sensitivity': ds_sensitivity
                    }
                    
                    # Add description if provided
                    if ds_description:
                        new_dataset['description'] = ds_description
                    
                    try:
                        dataset_id = self.db.create_dataset(new_dataset)
                        st.success(f"✅ Dataset '{ds_name}' added successfully! (ID: {dataset_id})")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding dataset: {str(e)}")
                else:
                    st.error("Please fill in all required fields.")

    def _show_import_data(self):
        """Display CSV import functionality."""
        st.markdown("### 📥 Import Datasets from CSV")
        st.markdown("Upload a CSV file to bulk import datasets.")
        
        st.info("""
        **CSV Format Requirements:**
        - Required columns: `name`, `source_department`, `size_mb`, `row_count`, `column_count`
        - Optional columns: `quality_score`, `sensitivity`, `last_accessed`, `created_at`
        - Quality score must be between 0 and 10
        - Size, row_count, and column_count must be numeric
        """)
        
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], key="import_data_csv")
        
        if uploaded_file is not None:
            try:
                success, df, error = parse_csv_file(uploaded_file, "datasets")
                
                if success:
                    st.success(f"✅ CSV file parsed successfully! Found {len(df)} rows.")
                    
                    st.markdown("**Preview of data to be imported:**")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    if st.button("Import All Records", type="primary", key="import_data_btn"):
                        datasets = prepare_dataset_data(df)
                        imported_count = 0
                        errors = []
                        
                        for dataset in datasets:
                            try:
                                self.db.create_dataset(dataset)
                                imported_count += 1
                            except Exception as e:
                                errors.append(f"Error importing {dataset.get('name', 'Unknown')}: {str(e)}")
                        
                        if imported_count > 0:
                            st.success(f"✅ Successfully imported {imported_count} of {len(datasets)} datasets!")
                            if errors:
                                st.warning(f"⚠️ {len(errors)} errors occurred.")
                                with st.expander("View Errors"):
                                    for error in errors[:10]:
                                        st.error(error)
                            st.rerun()
                        else:
                            st.error("❌ No datasets were imported.")
                else:
                    st.error(f"❌ CSV validation failed:\n{error}")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    def _show_data_quality_analysis(self, datasets_data):
        """Display data quality analysis and insights."""
        st.markdown("### 🔍 Data Quality Analysis")
        
        if not datasets_data:
            st.info("No dataset data available for analysis.")
            return
        
        # Calculate quality metrics
        df = pd.DataFrame(datasets_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            quality_avg = df['quality_score'].mean() if 'quality_score' in df.columns else 0
            st.metric("Average Quality Score", f"{quality_avg:.1f}/10")
        
        with col2:
            low_quality = len(df[df['quality_score'] < 5]) if 'quality_score' in df.columns else 0
            st.metric("Datasets Needing Improvement", low_quality)
        
        with col3:
            high_quality = len(df[df['quality_score'] >= 8]) if 'quality_score' in df.columns else 0
            st.metric("High Quality Datasets", high_quality)
        
        # AI-Powered Quality Analysis
        st.markdown("---")
        st.markdown("### 🤖 AI-Powered Analytics")
        
        ai_col1, ai_col2, ai_col3 = st.columns(3)
        
        with ai_col1:
            if st.button("📊 Analyse Quality", key="analyse_quality", use_container_width=True):
                with st.spinner("🤖 AI is analysing data quality..."):
                    if self.ai_engine and hasattr(self.ai_engine, 'analyze_data_quality'):
                        analysis = self.ai_engine.analyze_data_quality(datasets_data)
                        st.markdown("#### Quality Analysis")
                        st.markdown(analysis)
                    else:
                        st.info("AI engine not available.")
        
        with ai_col2:
            if st.button("🔮 Predict Trends", key="predict_data_trends", use_container_width=True):
                with st.spinner("🤖 AI is predicting data trends..."):
                    if self.ai_engine and self.ai_engine.model:
                        try:
                            df_analysis = pd.DataFrame(datasets_data)
                            prompt = f"""Based on {len(df_analysis)} datasets, predict:
1. Expected data growth trends
2. Quality score improvements needed
3. Department-specific recommendations
4. Data governance priorities

Current state:
- Average quality: {df_analysis['quality_score'].mean():.1f}/10
- Total size: {df_analysis['size_mb'].sum():.1f} MB
- Departments: {df_analysis['source_department'].nunique()}
- Low quality datasets: {len(df_analysis[df_analysis['quality_score'] < 5])}

Provide actionable predictions."""
                            prediction = self.ai_engine.chat_with_ai(prompt)
                            st.markdown("#### Trend Predictions")
                            st.markdown(prediction)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.info("AI engine not available.")
        
        with ai_col3:
            if st.button("💡 Get Recommendations", key="get_data_recommendations", use_container_width=True):
                with st.spinner("🤖 AI is generating recommendations..."):
                    if self.ai_engine and self.ai_engine.model:
                        try:
                            df_analysis = pd.DataFrame(datasets_data)
                            low_quality = len(df_analysis[df_analysis['quality_score'] < 5])
                            prompt = f"""Provide specific data governance recommendations:
- {low_quality} datasets need quality improvement
- Average quality: {df_analysis['quality_score'].mean():.1f}/10
- Top department: {df_analysis['source_department'].mode()[0] if not df_analysis.empty else 'N/A'}

Focus on immediate actions and long-term data strategy."""
                            recommendations = self.ai_engine.chat_with_ai(prompt)
                            st.markdown("#### AI Recommendations")
                            st.markdown(recommendations)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.info("AI engine not available.")
        
        # Quality Improvement Recommendations
        st.markdown("---")
        st.markdown("### 📋 Quality Improvement Checklist")
        
        checklist_items = [
            "✅ Data validation rules implemented",
            "✅ Missing values properly handled",
            "✅ Data format consistency checked",
            "✅ Outlier detection in place",
            "✅ Data lineage documented",
            "✅ Access controls properly configured",
            "✅ Regular data quality audits scheduled"
        ]
        
        for item in checklist_items:
            st.write(item)

    def _load_sample_datasets(self):
        """Load sample dataset data for demonstration."""
        sample_datasets = [
            {
                'name': 'Sales Transactions 2024',
                'source_department': 'Sales',
                'size_mb': 150.5,
                'row_count': 500000,
                'column_count': 15,
                'quality_score': 8,
                'sensitivity': 'Medium',
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Customer Feedback Q1',
                'source_department': 'Marketing',
                'size_mb': 45.2,
                'row_count': 120000,
                'column_count': 8,
                'quality_score': 6,
                'sensitivity': 'Low',
                'created_at': (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                'name': 'Server Performance Logs',
                'source_department': 'Engineering',
                'size_mb': 320.8,
                'row_count': 850000,
                'column_count': 12,
                'quality_score': 9,
                'sensitivity': 'High',
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Financial Transactions',
                'source_department': 'Finance',
                'size_mb': 210.3,
                'row_count': 350000,
                'column_count': 20,
                'quality_score': 7,
                'sensitivity': 'Confidential',
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Employee Records',
                'source_department': 'HR',
                'size_mb': 85.7,
                'row_count': 2500,
                'column_count': 25,
                'quality_score': 8.5,
                'sensitivity': 'Confidential',
                'created_at': datetime.now().isoformat()
            }
        ]
        
        try:
            for dataset in sample_datasets:
                self.db.create_dataset(dataset)
            
            st.success("✅ Sample dataset data loaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading sample data: {str(e)}")