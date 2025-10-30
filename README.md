# CRM Pro Geomarketing

Enterprise CRM platform with automatic geocoding and analytics dashboard for B2B prospecting

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-orange?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript&logoColor=black)](https://javascript.com)

## Overview

CRM Pro Geomarketing is a comprehensive business intelligence platform designed for enterprise B2B lead management and territorial analysis. The system processes large datasets, automatically enriches contact information with geographic coordinates, and provides real-time analytics through interactive dashboards.

## Key Features

### Data Processing Engine
- Multi-format import support (Excel, CSV, JSON)
- Intelligent column mapping and data validation
- Batch processing capabilities for large datasets
- Automated data cleansing and normalization

### Geocoding & Analytics
- Automatic address geocoding using multiple API providers
- Territorial analysis and lead distribution mapping
- Geographic clustering and route optimization
- Performance metrics and conversion tracking

### CRM Pipeline Management
- Lead qualification and scoring system
- Pipeline stage tracking and automation
- Contact history and interaction logging
- Task management and follow-up scheduling

### Business Intelligence Dashboard
- Real-time KPI monitoring and reporting
- Interactive charts and data visualizations
- Export capabilities for external analysis
- Customizable metrics and filters

## Technical Architecture

### Backend Stack
- **Flask** - Web framework and REST API
- **Pandas** - Data processing and manipulation
- **SQLAlchemy** - Database ORM and migrations
- **Celery** - Background task processing

### Frontend Components
- **HTML5/CSS3** - Responsive interface design
- **Vanilla JavaScript** - Client-side functionality
- **Chart.js** - Data visualization library
- **Bootstrap** - UI component framework

### External Integrations
- **ViaCEP API** - Brazilian address validation
- **Nominatim** - OpenStreetMap geocoding service
- **SparkPost** - Email campaign management
- **Twilio** - SMS notification system

## Performance Specifications

- **Processing Speed**: 10,000+ records per minute
- **Geocoding Accuracy**: 95%+ success rate
- **Concurrent Users**: 100+ simultaneous sessions
- **Response Time**: <200ms average API response

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Modern web browser

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Diego-Cruz-github/CRM-Pro-Geomarketing.git
cd CRM-Pro-Geomarketing

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Access the application at `http://localhost:5000`

### Configuration

Create a `.env` file with the following variables:

```env
FLASK_ENV=development
DATABASE_URL=sqlite:///crm_pro.db
SPARKPOST_API_KEY=your_key_here
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
```

## API Documentation

### Core Endpoints

#### Data Management
- `POST /api/upload` - Import lead data from files
- `GET /api/companies` - Retrieve company listings
- `PUT /api/companies/{id}` - Update company information
- `DELETE /api/companies/{id}` - Remove company records

#### Analytics
- `GET /api/dashboard/stats` - Dashboard metrics
- `GET /api/analytics/geographic` - Geographic distribution
- `GET /api/analytics/pipeline` - Sales pipeline data

#### Campaign Management
- `POST /api/campaigns/email` - Launch email campaigns
- `POST /api/campaigns/sms` - Send SMS notifications
- `GET /api/campaigns/{id}/metrics` - Campaign performance

## Production Deployment

### Docker Support

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

### Environment Configuration
- PostgreSQL for production database
- Redis for session management
- Nginx for reverse proxy
- SSL/TLS encryption enabled

## Security Features

- Input validation and sanitization
- SQL injection prevention
- Rate limiting and request throttling
- Secure session management
- CORS policy enforcement

## License

This project is proprietary software developed for enterprise B2B applications.

---

**Diego Fonte**  
Full Stack Developer | Cybersecurity & AI Focused  
[Portfolio PT](https://diegofontedev.com.br/) | [EN](https://diegofontedev.com.br/index-en.html) | [ES](https://diegofontedev.com.br/index-es.html)  
Contact: contato@diegofontedev.com.br