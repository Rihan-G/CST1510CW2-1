"""
Data import utilities for CSV file uploads.
"""

import pandas as pd
import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import datetime

def validate_cyber_incident_row(row: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate a single cyber incident row."""
    required_fields = ['title', 'threat_type', 'severity', 'status']
    for field in required_fields:
        if field not in row or pd.isna(row.get(field)) or str(row[field]).strip() == '':
            return False, f"Missing required field: {field}"
    
    valid_severities = ['Low', 'Medium', 'High', 'Critical']
    if row['severity'] not in valid_severities:
        return False, f"Invalid severity: {row['severity']}. Must be one of {valid_severities}"
    
    valid_statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
    if row['status'] not in valid_statuses:
        return False, f"Invalid status: {row['status']}. Must be one of {valid_statuses}"
    
    return True, None

def validate_dataset_row(row: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate a single dataset row."""
    required_fields = ['name', 'source_department', 'size_mb', 'row_count', 'column_count']
    for field in required_fields:
        if field not in row or pd.isna(row.get(field)):
            return False, f"Missing required field: {field}"
    
    # Validate numeric fields
    try:
        float(row['size_mb'])
        int(row['row_count'])
        int(row['column_count'])
    except (ValueError, TypeError):
        return False, "Invalid numeric values for size_mb, row_count, or column_count"
    
    # Validate quality score if present
    if 'quality_score' in row and not pd.isna(row.get('quality_score')):
        try:
            score = float(row['quality_score'])
            if score < 0 or score > 10:
                return False, "Quality score must be between 0 and 10"
        except (ValueError, TypeError):
            return False, "Invalid quality_score value"
    
    return True, None

def validate_it_ticket_row(row: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate a single IT ticket row."""
    required_fields = ['title', 'status', 'assigned_to', 'current_stage']
    for field in required_fields:
        if field not in row or pd.isna(row.get(field)) or str(row[field]).strip() == '':
            return False, f"Missing required field: {field}"
    
    valid_statuses = ['Open', 'In Progress', 'Pending', 'Resolved', 'Closed']
    if row['status'] not in valid_statuses:
        return False, f"Invalid status: {row['status']}. Must be one of {valid_statuses}"
    
    return True, None

def parse_csv_file(uploaded_file, data_type: str) -> tuple[bool, Optional[pd.DataFrame], Optional[str]]:
    """Parse and validate CSV file."""
    try:
        df = pd.read_csv(uploaded_file)
        
        if df.empty:
            return False, None, "CSV file is empty"
        
        # Validate based on data type
        if data_type == "cyber_incidents":
            errors = []
            for idx, row in df.iterrows():
                valid, error = validate_cyber_incident_row(row.to_dict())
                if not valid:
                    errors.append(f"Row {idx + 2}: {error}")
            if errors:
                return False, None, "\n".join(errors[:10])  # Show first 10 errors
        
        elif data_type == "datasets":
            errors = []
            for idx, row in df.iterrows():
                valid, error = validate_dataset_row(row.to_dict())
                if not valid:
                    errors.append(f"Row {idx + 2}: {error}")
            if errors:
                return False, None, "\n".join(errors[:10])
        
        elif data_type == "it_tickets":
            errors = []
            for idx, row in df.iterrows():
                valid, error = validate_it_ticket_row(row.to_dict())
                if not valid:
                    errors.append(f"Row {idx + 2}: {error}")
            if errors:
                return False, None, "\n".join(errors[:10])
        
        return True, df, None
        
    except Exception as e:
        return False, None, f"Error parsing CSV: {str(e)}"

def prepare_cyber_incident_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Prepare cyber incident data for database insertion."""
    incidents = []
    for _, row in df.iterrows():
        incident = {
            'title': str(row.get('title', '')),
            'description': str(row.get('description', '')),
            'threat_type': str(row.get('threat_type', '')),
            'severity': str(row.get('severity', 'Medium')),
            'status': str(row.get('status', 'Open')),
            'created_at': row.get('created_at', datetime.now().isoformat()),
            'resolved_at': row.get('resolved_at') if not pd.isna(row.get('resolved_at')) else None,
            'resolution_time_hours': float(row.get('resolution_time_hours', 0)) if not pd.isna(row.get('resolution_time_hours')) else None,
            'assigned_to': str(row.get('assigned_to', '')) if not pd.isna(row.get('assigned_to')) else None
        }
        incidents.append(incident)
    return incidents

def prepare_dataset_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Prepare dataset data for database insertion."""
    datasets = []
    for _, row in df.iterrows():
        dataset = {
            'name': str(row.get('name', '')),
            'source_department': str(row.get('source_department', '')),
            'size_mb': float(row.get('size_mb', 0)),
            'row_count': int(row.get('row_count', 0)),
            'column_count': int(row.get('column_count', 0)),
            'quality_score': float(row.get('quality_score', 5.0)) if not pd.isna(row.get('quality_score')) else None,
            'last_accessed': row.get('last_accessed', datetime.now().isoformat()) if not pd.isna(row.get('last_accessed')) else None,
            'created_at': row.get('created_at', datetime.now().isoformat()),
            'sensitivity': str(row.get('sensitivity', 'Internal')) if not pd.isna(row.get('sensitivity')) else None
        }
        datasets.append(dataset)
    return datasets

def prepare_it_ticket_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Prepare IT ticket data for database insertion."""
    tickets = []
    for _, row in df.iterrows():
        ticket = {
            'title': str(row.get('title', '')),
            'description': str(row.get('description', '')),
            'status': str(row.get('status', 'Open')),
            'assigned_to': str(row.get('assigned_to', '')),
            'current_stage': str(row.get('current_stage', 'New')),
            'priority': str(row.get('priority', 'Medium')),
            'created_at': row.get('created_at', datetime.now().isoformat()),
            'resolved_at': row.get('resolved_at') if not pd.isna(row.get('resolved_at')) else None,
            'time_in_stage_hours': float(row.get('time_in_stage_hours', 0)) if not pd.isna(row.get('time_in_stage_hours')) else None,
            'category': str(row.get('category', '')) if not pd.isna(row.get('category')) else None
        }
        tickets.append(ticket)
    return tickets

