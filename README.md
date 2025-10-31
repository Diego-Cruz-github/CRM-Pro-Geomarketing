# CRM Pro Geomarketing

A comprehensive customer relationship management system with advanced geolocation features and business intelligence integration.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-orange.svg)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel%20Integration-red.svg)
![Power BI](https://img.shields.io/badge/Power%20BI-Integration-yellow.svg)
![Tableau](https://img.shields.io/badge/Tableau-Compatible-orange.svg)
![Google Data Studio](https://img.shields.io/badge/Google%20Data%20Studio-Supported-blue.svg)

## System Overview

<div align="center">

### Geomarketing Intelligence
<img src="SS's/cgif1-geomarketing_2.gif" width="600" alt="Geomarketing Demo">

### CRM Pipeline Management  
<img src="SS's/ccrm1-_1_.gif" width="600" alt="CRM Pipeline Demo">

### Real-time Dashboard
<img src="SS's/ccrmedashboard-_1_.gif" width="600" alt="Dashboard Demo">

### Business Intelligence Export
<img src="SS's/cBiimplementação-_1_.gif" width="600" alt="BI Integration Demo">

</div>

## Features

### Core CRM Functionality
- **Lead Management**: Complete pipeline tracking from initial contact to closure
- **Real-time Status Updates**: Dynamic pipeline status management with instant dashboard synchronization
- **Advanced Filtering**: Multi-criteria search and filtering system
- **Data Validation**: Comprehensive input validation and error handling

### Geomarketing Intelligence
- **Automated Geocoding**: Integration with multiple geocoding services (ViaCEP, Nominatim)
- **Geographic Analysis**: Regional distribution analytics with fallback strategies
- **Interactive Mapping**: Real-time geographic data visualization
- **Location-based Insights**: Territory analysis and geographic performance metrics

### Business Intelligence Integration
- **Power BI Export**: Structured JSON format for enterprise analytics
- **Tableau Compatibility**: Optimized CSV exports with proper formatting
- **Google Data Studio**: Direct integration with cloud-based dashboards
- **Multi-format Export**: Excel, CSV with encoding optimization for international use

### Advanced Data Processing
- **Smart Column Detection**: Automatic mapping of 40+ business field types
- **Multi-format Support**: Excel (.xlsx, .xls) and CSV with encoding detection
- **Data Standardization**: CNPJ, phone, email cleaning and validation pipeline
- **Professional Templates**: HTML email and SMS templates with dynamic substitution
- **Kanban Pipeline**: Drag-and-drop interface with 7-stage lead management

## Technical Stack

### Backend
- **Flask**: RESTful API architecture with modular design
- **Pandas**: Advanced data manipulation and analysis
- **OpenPyXL**: Excel file processing and generation
- **SQLite**: Lightweight database for development (PostgreSQL ready)

### Frontend
- **Vanilla JavaScript**: Custom dashboard with real-time updates
- **Chart.js**: Interactive data visualizations
- **CSS Grid/Flexbox**: Responsive design system
- **Local Storage API**: Cross-tab communication for real-time sync

### Integration Services
- **Email Automation**: SMTP and SparkPost integration
- **SMS Services**: Twilio API integration
- **Geocoding APIs**: Multiple provider fallback system
- **Export Engines**: Multi-platform BI tool compatibility

## Architecture Highlights

### Modular Design
```
src/
├── app.py              # Main Flask application
├── utils/              # Core services
│   ├── data_processor.py    # Data processing engine
│   ├── geocoding.py         # Geographic services
│   ├── email_sender.py      # Communication services
│   └── sms_sender.py        # SMS automation
├── templates/          # Frontend interfaces
└── static/            # Assets and styling
```

### Enterprise Architecture
- **Service Layer Pattern**: Modular design with dedicated services for email, SMS, and geocoding
- **Multi-API Fallback**: Intelligent geocoding with ViaCEP, Nominatim, and regional fallbacks
- **Real-time Synchronization**: Cross-tab communication using localStorage API
- **Batch Processing**: Optimized for datasets of 10,000+ records with progress tracking
- **Undo/Redo System**: Operation history with 10-level rollback capability

### Performance & Scalability
- **Memory Optimization**: Efficient buffer handling for 100MB+ file processing
- **Geocoding Cache**: 15-minute TTL with 90%+ success rate
- **Dashboard Updates**: Sub-100ms real-time synchronization
- **Export Performance**: Latin-1 encoding optimization for Brazilian Excel compatibility

### Security Features
- **Input Sanitization**: Comprehensive data validation
- **File Upload Security**: Type validation and size limits
- **CORS Protection**: Secure cross-origin request handling
- **Error Handling**: Graceful degradation with detailed logging

## API Endpoints

### Data Management
- `POST /api/upload` - File upload and processing
- `GET /api/crm/companies` - Retrieve company data
- `PUT /api/crm/company/{id}/status` - Update pipeline status
- `POST /api/crm/company/add` - Add new company

### Analytics & Export
- `GET /api/dashboard/stats` - Dashboard metrics
- `GET /api/export/excel` - Excel export with full formatting
- `GET /api/export/csv` - CSV export with regional encoding

### Communication
- `POST /api/email/send` - Individual email dispatch
- `POST /api/email/campaign` - Bulk email campaigns
- `POST /api/sms/send` - SMS communication

## Requirements

- Python 3.8+
- Flask 2.0+
- Modern browser with JavaScript ES6+ support

## System Capabilities

- **Data Processing**: Handles 10,000+ records with intelligent validation
- **Geocoding Accuracy**: 90%+ success rate with 77 regional mappings
- **Real-time Performance**: Sub-100ms dashboard synchronization
- **Memory Efficiency**: 100MB+ file processing with optimized buffers
- **Multi-provider APIs**: SparkPost, Twilio, ViaCEP, Nominatim integration

---

**Diego Fonte**  
Full Stack Developer | Cybersecurity & AI Focused  
[Portfolio PT](https://diegofontedev.com.br/) | [EN](https://diegofontedev.com.br/index-en.html) | [ES](https://diegofontedev.com.br/index-es.html)  
Contato: contato@diegofontedev.com.br
