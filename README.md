# CRM Pro Geomarketing

A comprehensive customer relationship management system with advanced geolocation features and business intelligence integration.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-orange.svg)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel%20Integration-red.svg)

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

### Data Processing Architecture
- **Multi-source Import**: Excel (.xlsx, .xls) and CSV file processing
- **Intelligent Column Mapping**: Automatic field detection and standardization
- **Batch Processing**: Efficient handling of large datasets with progress tracking
- **Data Integrity**: Built-in validation and error recovery mechanisms

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

### Performance Optimizations
- **Lazy Loading**: Progressive data loading for large datasets
- **Caching Strategy**: Intelligent geocoding cache with 15-minute TTL
- **Background Processing**: Non-blocking operations for file uploads
- **Memory Management**: Efficient data structures for real-time operations

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

## Installation

```bash
# Clone repository
git clone <repository-url>
cd crm-pro-geomarketing

# Install dependencies
pip install -r requirements.txt

# Run application
python src/app.py
```

Access the application at `http://localhost:5000`

## Performance Metrics

- **File Processing**: Handles 10,000+ records with 2-second processing time
- **Geocoding**: 90%+ success rate with multi-provider fallback
- **Real-time Sync**: Sub-100ms dashboard updates across multiple tabs
- **Export Speed**: Excel generation optimized for enterprise datasets

---

**Diego Fonte**  
Full Stack Developer | Cybersecurity & AI Focused  
[Portfolio PT](https://diegofontedev.com.br/) | [EN](https://diegofontedev.com.br/index-en.html) | [ES](https://diegofontedev.com.br/index-es.html)  
Contato: contato@diegofontedev.com.br
