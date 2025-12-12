"""
Search and filtering utilities for dashboards.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

def filter_cyber_incidents(incidents: List[Dict[str, Any]], search_term: str = "", 
                          threat_type: str = "All", severity: str = "All", 
                          status: str = "All", date_range: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """Filter cyber incidents based on criteria."""
    df = pd.DataFrame(incidents)
    if df.empty:
        return []
    
    # Search term filter
    if search_term:
        mask = (
            df['title'].str.contains(search_term, case=False, na=False) |
            df['description'].str.contains(search_term, case=False, na=False) |
            df['threat_type'].str.contains(search_term, case=False, na=False) |
            df['assigned_to'].str.contains(search_term, case=False, na=False)
        )
        df = df[mask]
    
    # Threat type filter
    if threat_type != "All":
        df = df[df['threat_type'] == threat_type]
    
    # Severity filter
    if severity != "All":
        df = df[df['severity'] == severity]
    
    # Status filter
    if status != "All":
        df = df[df['status'] == status]
    
    # Date range filter
    if date_range and len(date_range) == 2:
        try:
            df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', errors='coerce')
            df = df.dropna(subset=['created_at'])
            start_date, end_date = date_range
            df = df[(df['created_at'] >= start_date) & (df['created_at'] <= end_date)]
        except:
            pass
    
    return df.to_dict('records')

def filter_datasets(datasets: List[Dict[str, Any]], search_term: str = "",
                   department: str = "All", min_quality: float = 0.0,
                   max_quality: float = 10.0, sensitivity: str = "All") -> List[Dict[str, Any]]:
    """Filter datasets based on criteria."""
    df = pd.DataFrame(datasets)
    if df.empty:
        return []
    
    # Search term filter
    if search_term:
        mask = (
            df['name'].str.contains(search_term, case=False, na=False) |
            df['source_department'].str.contains(search_term, case=False, na=False) |
            df['sensitivity'].str.contains(search_term, case=False, na=False)
        )
        df = df[mask]
    
    # Department filter
    if department != "All":
        df = df[df['source_department'] == department]
    
    # Quality score filter
    if 'quality_score' in df.columns:
        df = df[(df['quality_score'] >= min_quality) & (df['quality_score'] <= max_quality)]
    
    # Sensitivity filter
    if sensitivity != "All":
        df = df[df['sensitivity'] == sensitivity]
    
    return df.to_dict('records')

def filter_it_tickets(tickets: List[Dict[str, Any]], search_term: str = "",
                      category: str = "All", priority: str = "All",
                      status: str = "All", assigned_to: str = "All") -> List[Dict[str, Any]]:
    """Filter IT tickets based on criteria."""
    df = pd.DataFrame(tickets)
    if df.empty:
        return []
    
    # Search term filter
    if search_term:
        mask = (
            df['title'].str.contains(search_term, case=False, na=False) |
            df['description'].str.contains(search_term, case=False, na=False) |
            df['category'].str.contains(search_term, case=False, na=False) |
            df['assigned_to'].str.contains(search_term, case=False, na=False)
        )
        df = df[mask]
    
    # Category filter
    if category != "All":
        df = df[df['category'] == category]
    
    # Priority filter
    if priority != "All":
        df = df[df['priority'] == priority]
    
    # Status filter
    if status != "All":
        df = df[df['status'] == status]
    
    # Assigned to filter
    if assigned_to != "All":
        df = df[df['assigned_to'] == assigned_to]
    
    return df.to_dict('records')

