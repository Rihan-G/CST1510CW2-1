# 🛡️ Intelligence Platform

A comprehensive, unified platform for managing Cybersecurity, Data Science, and IT Operations with AI-powered analytics and insights.

## Overview

The Intelligence Platform is a web-based application built with Streamlit that provides a centralised dashboard for managing and analysing data across multiple departments. It features role-based access control, AI-powered analytics, and interactive visualisations to help organisations make data-driven decisions.

## Key Features

### 🔐 Authentication & Security
- Secure user authentication with bcrypt password hashing
- Role-based access control (Admin, Cybersecurity, Data Science, IT Operations)
- Session management and secure login system

### 🏠 Executive Dashboard
- Cross-departmental overview and key performance indicators
- Real-time metrics for security posture, system health, and data quality
- Interactive analytics and trend visualisations
- AI-powered performance analysis and strategic recommendations

### 🛡️ Cybersecurity Dashboard
- Incident management and threat tracking
- Security incident analysis with severity classification
- Threat pattern detection and trend analysis
- AI-powered incident pattern analysis and threat predictions
- Export capabilities for incident reports

### 📊 Data Science Dashboard
- Dataset metadata management
- Data quality scoring and assessment
- Department-wise data distribution analysis
- Data sensitivity classification
- AI-powered quality analysis and recommendations
- CSV import functionality for bulk data management

### 💻 IT Operations Dashboard
- IT ticket management system
- Ticket lifecycle tracking (Open, In Progress, Resolved)
- Performance metrics and SLA monitoring
- Team performance analytics
- AI-powered workload predictions and recommendations
- Category and priority-based ticket organisation

### 🤖 AI Assistant
- Intelligent chat interface powered by Google Gemini AI
- Context-aware assistance across all platform functions
- Automated analysis and recommendations
- Quick question templates for common queries
- Support for cybersecurity, data science, and IT operations queries

## Technologies Used

- **Frontend Framework:** Streamlit 1.28.0+
- **Data Processing:** Pandas 2.0.0+, NumPy 1.24.0+
- **Visualisation:** Plotly 5.17.0+
- **Database:** SQLite3
- **Security:** bcrypt 4.0.0+
- **AI Integration:** Google Generative AI (Gemini)

## Installation


### Step 1: Clone the Repository

```bash
git clone https://github.com/Rihan-G/CST1510CW2-1.git
cd CST1510CW2-1
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys (Optional)

For AI features to work, create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

**Note:** The application will work without an API key, but AI-powered features will be unavailable.

### Step 4: Run the Application

```bash
streamlit run main.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

## Default User Credentials

The platform comes with default user accounts for testing:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator (full access) |
| cyber | cyber123 | Cybersecurity |
| data | data123 | Data Science |
| it | it123 | IT Operations |

**⚠️ Important:** Change these default passwords in a production environment.

## Project Structure

```
CST1510CW2-1/
├── ai/
│   ├── __init__.py
│   └── gemini_integration.py      # AI integration with Google Gemini
├── auth/
│   ├── __init__.py
│   └── authentication.py          # User authentication system
├── dashboards/
│   ├── __init__.py
│   ├── executive.py               # Executive dashboard
│   ├── cybersecurity.py          # Cybersecurity dashboard
│   ├── data_science.py            # Data Science dashboard
│   ├── it_operations.py          # IT Operations dashboard
│   └── ai_assistant.py            # AI Assistant interface
├── database/
│   ├── __init__.py
│   ├── db_manager.py              # Database management
│   └── seed_database.py          # Database seeding utility
├── utils/
│   ├── __init__.py
│   ├── data_import.py             # CSV import functionality
│   ├── search_filter.py          # Search and filter utilities
│   └── theme.py                  # UI theme management
├── .streamlit/
│   └── secrets.toml              # API keys (not in git)
├── main.py                       # Application entry point
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Features in Detail

### Role-Based Access Control

- **Administrator:** Full access to all dashboards and features
- **Cybersecurity:** Access to Executive, Cybersecurity, and AI Assistant dashboards
- **Data Science:** Access to Executive, Data Science, and AI Assistant dashboards
- **IT Operations:** Access to Executive, IT Operations, and AI Assistant dashboards

### AI Integration

The platform uses Google Gemini AI for:
- Incident pattern analysis
- Data quality assessment
- Trend predictions
- Strategic recommendations
- Natural language queries

The AI integration automatically discovers compatible models and handles API version differences .

### Data Management

- **Import:** CSV file import for bulk data entry
- **Export:** CSV export functionality for all data types
- **Validation:** Automatic data validation on import
- **Quality Scoring:** Automated data quality assessment

### Visualisations

Interactive charts and graphs using Plotly:
- Line charts for trends
- Bar charts for comparisons
- Pie charts for distributions
- Heatmaps for correlation analysis
- Scatter plots for relationships

## Configuration

### Database

The application uses SQLite3 and automatically creates the database file (`intelligence_platform.db`) on first run. The database schema includes:

- Users table (authentication)
- Cyber incidents table
- Datasets metadata table
- IT tickets table


## Troubleshooting

### AI Features Not Working

If AI features are unavailable:
1. Check that `GEMINI_API_KEY` is set in `.streamlit/secrets.toml`
2. Verify your API key is valid
3. Check the AI status indicator in the application

### Database Issues

If you encounter database errors:
1. Delete `intelligence_platform.db` to reset the database
2. Restart the application (it will recreate the database)
3. Re-register users if needed

### Import Errors

If CSV imports fail:
1. Verify the CSV format matches the expected structure
2. Check for required columns
3. Review error messages in the import interface

## Development

### Adding New Features

The codebase is modular and organised by functionality:
- Dashboard modules are in `dashboards/`
- Database operations in `database/`
- Utility functions in `utils/`
- AI integration in `ai/`

### Database Seeding

To populate the database with sample data:

```bash
python database/seed_database.py
```

## Security Considerations

- Passwords are hashed using bcrypt
- API keys are stored in `.streamlit/secrets.toml` (excluded from git)
- Database files are excluded from version control
- Session-based authentication


---

**Built with  using Streamlit and Python**

